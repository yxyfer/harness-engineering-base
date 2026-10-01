"""Native test-result adapters and validation of the shipped JSON schema subset."""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET


def validate_schema(value, schema: dict, location: str = "report") -> None:
    if "anyOf" in schema:
        for option in schema["anyOf"]:
            try:
                validate_schema(value, option, location)
                return
            except ValueError:
                pass
        raise ValueError(f"{location}: no matching schema variant")
    types = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "boolean": bool,
        "number": (int, float),
        "null": type(None),
    }
    kind = schema.get("type")
    if kind and (
        not isinstance(value, types[kind])
        or (kind in {"integer", "number"} and isinstance(value, bool))
    ):
        raise ValueError(f"{location}: invalid {kind}")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{location}: invalid enum")
    if "minimum" in schema and value < schema["minimum"]:
        raise ValueError(f"{location}: below minimum")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if set(schema.get("required", [])) - set(value):
            raise ValueError(f"{location}: missing keys")
        if schema.get("additionalProperties") is False and set(value) - set(
            properties
        ):
            raise ValueError(f"{location}: unknown keys")
        for key, item in value.items():
            if key in properties:
                validate_schema(item, properties[key], f"{location}.{key}")
    if isinstance(value, list):
        for item in value:
            validate_schema(item, schema.get("items", {}), location + "[]")


def native_report(path: Path, adapter: str) -> dict:
    if not path.is_file() or path.is_symlink():
        raise ValueError("missing required native report")
    if path.stat().st_size > 4 * 1024 * 1024:
        raise ValueError("native report exceeds 4 MiB bound")
    if adapter == "unittest":
        result = json.loads(path.read_text())
        keys = {
            "collected",
            "executed",
            "failures",
            "errors",
            "skipped",
            "expected_failures",
            "unexpected_successes",
            "retries",
        }
        if (
            type(result) is not dict
            or set(result) != keys
            or any(type(v) is not int or v < 0 for v in result.values())
        ):
            raise ValueError("malformed unittest native result")
        if result["executed"] > result["collected"]:
            raise ValueError("unittest execution exceeds collection")
        return result
    if adapter != "junit":
        raise ValueError("unsupported evidence adapter")
    try:
        tree = ET.fromstring(path.read_bytes())
    except ET.ParseError as error:
        raise ValueError(f"malformed JUnit: {error}") from error
    if tree.tag not in {"testsuite", "testsuites"}:
        raise ValueError("malformed JUnit root")
    cases = list(tree.iter("testcase"))
    suites = [s for s in tree.iter("testsuite") if not s.findall("testsuite")]
    # Node emits native testcase records directly, without suite counters.
    direct_node = (
        tree.tag == "testsuites"
        and not suites
        and len(tree.findall("testcase")) == len(cases)
    )
    if not direct_node and (
        not suites or sum(int(s.attrib["tests"]) for s in suites) != len(cases)
    ):
        raise ValueError("JUnit collection does not match native cases")
    result = {
        "collected": len(cases),
        "executed": len(cases),
        "failures": sum(c.find("failure") is not None for c in cases),
        "errors": sum(c.find("error") is not None for c in cases),
        "skipped": sum(c.find("skipped") is not None for c in cases),
        "retries": sum(
            len(c.findall(tag))
            for c in cases
            for tag in (
                "rerunFailure",
                "rerunError",
                "flakyFailure",
                "flakyError",
            )
        ),
        "expected_failures": 0,
        "unexpected_successes": 0,
    }
    for field in ("failures", "errors", "skipped"):
        if (
            suites
            and all(field in s.attrib for s in suites)
            and sum(int(s.attrib[field]) for s in suites) != result[field]
        ):
            raise ValueError(f"JUnit {field} does not match native cases")
    return result


def result_problem(result: dict) -> str:
    if result["collected"] == 0:
        return "zero required tests collected"
    if result["executed"] != result["collected"]:
        return "incomplete native execution"
    if any(
        result[k]
        for k in (
            "failures",
            "errors",
            "skipped",
            "retries",
            "expected_failures",
            "unexpected_successes",
        )
    ):
        return "native failures, skips, expected failures or retries require review"
    return ""


def validate_evidence(report: dict, schema: dict) -> None:
    validate_schema(report, schema)
    complete = (
        report["stable"]
        and report["scope"] == "full"
        and all(
            not c["required"] or c["state"] == "passed"
            for c in report["controls"]
        )
    )
    if report["complete"] != complete:
        raise ValueError("report completeness contradicts required controls")
    for item in report["controls"]:
        if item["state"] == "passed" and item["exit"] != 0:
            raise ValueError("passed control lacks native successful exit")
        if item["state"] == "passed" and item["name"] in {"tests", "self-test"}:
            if item["counts"] is None or result_problem(item["counts"]):
                raise ValueError("passed tests lack successful native evidence")
