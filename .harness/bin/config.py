#!/usr/bin/env python3
"""Validate and inspect the harness TOML configuration contract."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import re
import sys
import tomllib
from typing import Any, Callable


CONFIG_EXIT = 4
SUPPORTED_SCHEMA_VERSIONS = {1, 2}
SECTIONS: dict[str, set[str]] = {
    "project": {"profiles"},
    "commands": {"setup", "start", "check", "test", "smoke"},
    "checks": {"required"},
    "standards": {
        "line_length",
        "file_lines_warning",
        "function_lines_warning",
    },
    "readiness": {"required_documents", "fail_on_needs_input"},
    "security": {"mode"},
    "analysis": {"exclude"},
}
PROFILE_NAMES = {"auto", "python", "typescript", "shell", "markdown"}
SECURITY_MODES = {"off", "local", "ci"}
COMMAND_NAMES = ("setup", "start", "check", "test", "smoke")


class ConfigError(Exception):
    def __init__(
        self, path: Path, key: str, expected: str, actual: str
    ) -> None:
        self.path = path
        self.key = key
        self.expected = expected
        self.actual = actual
        super().__init__(f"{path}: {key}: expected {expected}; got {actual}")


def actual(value: Any) -> str:
    if value is None:
        return "missing value"
    return f"{type(value).__name__} {value!r}"


def require(
    condition: bool, path: Path, key: str, expected: str, value: Any
) -> None:
    if not condition:
        raise ConfigError(path, key, expected, actual(value))


def require_exact_keys(
    path: Path, prefix: str, value: Any, expected_keys: set[str]
) -> dict[str, Any]:
    require(type(value) is dict, path, prefix, "a TOML table", value)
    unknown = set(value) - expected_keys
    if unknown:
        key = sorted(unknown)[0]
        choices = ", ".join(sorted(expected_keys))
        raise ConfigError(
            path,
            f"{prefix}.{key}",
            f"one of: {choices}",
            actual(value[key]),
        )
    missing = expected_keys - set(value)
    if missing:
        key = sorted(missing)[0]
        raise ConfigError(
            path, f"{prefix}.{key}", "a configured value", "missing key"
        )
    return value


def require_string_list(
    path: Path,
    key: str,
    value: Any,
    *,
    allow_empty: bool = False,
    item_check: Callable[[str], bool] | None = None,
    item_expectation: str = "a non-empty string",
) -> list[str]:
    valid_list = type(value) is list and (allow_empty or len(value) > 0)
    require(valid_list, path, key, "a list of strings", value)
    for item in value:
        valid_item = type(item) is str and bool(item)
        if valid_item and item_check is not None:
            valid_item = item_check(item)
        require(valid_item, path, key, item_expectation, item)
    require(len(value) == len(set(value)), path, key, "unique values", value)
    return value


def validate(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigError(path, "file", "an existing TOML file", "missing file")
    try:
        with path.open("rb") as stream:
            config = tomllib.load(stream)
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(
            path, "TOML", "valid TOML syntax", str(error)
        ) from error

    expected_top_level = {"schema_version", *SECTIONS}
    unknown_sections = set(config) - expected_top_level
    if unknown_sections:
        key = sorted(unknown_sections)[0]
        choices = ", ".join(sorted(expected_top_level))
        raise ConfigError(path, key, f"one of: {choices}", actual(config[key]))
    missing_sections = expected_top_level - set(config)
    if missing_sections:
        key = sorted(missing_sections)[0]
        raise ConfigError(
            path, key, "a configured value or table", "missing key"
        )

    require(
        type(config["schema_version"]) is int
        and config["schema_version"] in SUPPORTED_SCHEMA_VERSIONS,
        path,
        "schema_version",
        "integer 1 or 2",
        config["schema_version"],
    )

    expected_sections = {name: set(keys) for name, keys in SECTIONS.items()}
    # Additive optional command: legacy complete configs remain valid unchanged.
    if type(config.get("commands")) is dict and "format" in config["commands"]:
        expected_sections["commands"].add("format")
    if config["schema_version"] == 2:
        expected_sections["project"] |= {"frameworks", "capabilities", "roots"}
    sections = {
        name: require_exact_keys(path, name, config[name], keys)
        for name, keys in expected_sections.items()
    }

    profiles = require_string_list(
        path,
        "project.profiles",
        sections["project"]["profiles"],
        item_check=lambda item: item in PROFILE_NAMES,
        item_expectation=f"one of: {', '.join(sorted(PROFILE_NAMES))}",
    )
    require(
        "auto" not in profiles or profiles == ["auto"],
        path,
        "project.profiles",
        "either ['auto'] or explicit profiles without 'auto'",
        profiles,
    )

    if config["schema_version"] == 2:
        validate_selection(path, sections["project"])

    for name in (*COMMAND_NAMES, "format"):
        if name == "format" and name not in sections["commands"]:
            sections["commands"][name] = ""
        value = sections["commands"][name]
        require(type(value) is str, path, f"commands.{name}", "a string", value)

    require_string_list(
        path,
        "checks.required",
        sections["checks"]["required"],
        item_check=lambda item: re.fullmatch(r"[a-z0-9][a-z0-9-]*", item)
        is not None,
        item_expectation="a lowercase check identifier",
    )

    for name, value in sections["standards"].items():
        require(
            type(value) is int and value > 0,
            path,
            f"standards.{name}",
            "a positive integer",
            value,
        )

    require_string_list(
        path,
        "readiness.required_documents",
        sections["readiness"]["required_documents"],
        allow_empty=config["schema_version"] == 2,
        item_check=lambda item: (
            config["schema_version"] == 2 and item == "auto"
        )
        or (Path(item).name == item and item.endswith(".md")),
        item_expectation="a Markdown filename without directory components",
    )
    documents = sections["readiness"]["required_documents"]
    require(
        "auto" not in documents or documents == ["auto"],
        path,
        "readiness.required_documents",
        "['auto'] or explicit documents",
        documents,
    )
    readiness_flag = sections["readiness"]["fail_on_needs_input"]
    require(
        type(readiness_flag) is bool,
        path,
        "readiness.fail_on_needs_input",
        "a boolean",
        readiness_flag,
    )

    security_mode = sections["security"]["mode"]
    require(
        type(security_mode) is str and security_mode in SECURITY_MODES,
        path,
        "security.mode",
        f"one of: {', '.join(sorted(SECURITY_MODES))}",
        security_mode,
    )

    require_string_list(
        path,
        "analysis.exclude",
        sections["analysis"]["exclude"],
        allow_empty=True,
        item_check=lambda item: not PurePosixPath(item).is_absolute()
        and ".." not in PurePosixPath(item).parts,
        item_expectation="a relative path without '..'",
    )
    return config


def validate_selection(path: Path, project: dict[str, Any]) -> None:
    frameworks = require_string_list(
        path,
        "project.frameworks",
        project["frameworks"],
        allow_empty=True,
        item_check=lambda name: name in {"auto", "nextjs"},
        item_expectation="auto or nextjs",
    )
    require(
        "auto" not in frameworks or frameworks == ["auto"],
        path,
        "project.frameworks",
        "['auto'] or explicit frameworks",
        frameworks,
    )
    require_string_list(
        path,
        "project.capabilities",
        project["capabilities"],
        allow_empty=True,
        item_check=lambda name: re.fullmatch(r"[a-z][a-z0-9-]*", name)
        is not None,
        item_expectation="a lowercase capability identifier",
    )
    roots = require_string_list(
        path,
        "project.roots",
        project["roots"],
        item_check=lambda name: name == "."
        or (
            not PurePosixPath(name).is_absolute()
            and PurePosixPath(name).as_posix() == name
            and not any(part in {".", "..", ""} for part in name.split("/"))
            and not any(c in name for c in "\\:\n\r\t")
        ),
        item_expectation="a canonical relative directory without '..'",
    )
    require(
        len({name.casefold() for name in roots}) == len(roots),
        path,
        "project.roots",
        "non-colliding roots",
        roots,
    )


def get_value(config: dict[str, Any], key: str, path: Path) -> Any:
    value: Any = config
    for part in key.split("."):
        if type(value) is not dict or part not in value:
            raise ConfigError(
                path, key, "a known configuration key", "unknown key"
            )
        value = value[part]
    return value


def print_value(value: Any) -> None:
    if type(value) is bool:
        print("true" if value else "false")
    elif type(value) is list:
        print(json.dumps(value, separators=(",", ":")))
    else:
        print(value)


def print_summary(config: dict[str, Any], source: str) -> None:
    print(f"source={source}")
    print(f"schema_version={config['schema_version']}")
    print(f"project.profiles={json.dumps(config['project']['profiles'])}")
    if config["schema_version"] == 2:
        for name in ("frameworks", "capabilities", "roots"):
            print(f"project.{name}={json.dumps(config['project'][name])}")
    print(f"checks.required={json.dumps(config['checks']['required'])}")
    for key, value in config["standards"].items():
        print(f"standards.{key}={value}")
    documents = json.dumps(config["readiness"]["required_documents"])
    print(f"readiness.required_documents={documents}")
    readiness_flag = config["readiness"]["fail_on_needs_input"]
    print(f"readiness.fail_on_needs_input={str(readiness_flag).lower()}")
    print(f"security.mode={config['security']['mode']}")
    print(f"analysis.exclude={json.dumps(config['analysis']['exclude'])}")
    for name in (*COMMAND_NAMES, "format"):
        state = "configured" if config["commands"][name] else "automatic"
        print(f"commands.{name}=<{state}>")


def usage() -> None:
    print(
        "usage: config.py validate PATH | get PATH KEY | list PATH KEY | summary PATH SOURCE",
        file=sys.stderr,
    )


def main(arguments: list[str]) -> int:
    if len(arguments) < 2:
        usage()
        return 2
    command = arguments[0]
    path = Path(arguments[1]).expanduser()
    try:
        config = validate(path)
        if command == "validate" and len(arguments) == 2:
            return 0
        if command == "get" and len(arguments) == 3:
            print_value(get_value(config, arguments[2], path))
            return 0
        if command == "list" and len(arguments) == 3:
            value = get_value(config, arguments[2], path)
            if type(value) is not list:
                raise ConfigError(path, arguments[2], "a list", actual(value))
            for item in value:
                print(item)
            return 0
        if command == "summary" and len(arguments) == 3:
            print_summary(config, arguments[2])
            return 0
        usage()
        return 2
    except ConfigError as error:
        print(f"config: {error}", file=sys.stderr)
        return CONFIG_EXIT


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
