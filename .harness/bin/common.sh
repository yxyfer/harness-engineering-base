#!/bin/sh

set -eu

command_name=${HARNESS_COMMAND_NAME:-harness}

fail() {
  printf '%s: %s\n' "$command_name" "$*" >&2
  exit 1
}

note() {
  printf '%s: %s\n' "$command_name" "$*"
}

warn() {
  printf '%s: warning: %s\n' "$command_name" "$*" >&2
}

resolve_target() {
  target_input=${1:-.}
  [ -d "$target_input" ] || fail "target directory does not exist: $target_input"
  TARGET=$(CDPATH= cd "$target_input" && pwd -P)
  export TARGET
}

has_command() {
  command -v "$1" >/dev/null 2>&1
}

has_npm_script() {
  script_name=$1
  [ -f "$TARGET/package.json" ] || return 1
  has_command node || return 1
  node -e '
    const p = require(process.argv[1]);
    process.exit(p.scripts && p.scripts[process.argv[2]] ? 0 : 1);
  ' "$TARGET/package.json" "$script_name" >/dev/null 2>&1
}

node_runner() {
  if [ -f "$TARGET/pnpm-lock.yaml" ]; then
    printf '%s\n' pnpm
  elif [ -f "$TARGET/yarn.lock" ]; then
    printf '%s\n' yarn
  else
    printf '%s\n' npm
  fi
}

run_node_script() {
  script_name=$1
  runner=$(node_runner)
  has_command "$runner" || fail "$runner is required to run the '$script_name' script"
  note "running package script '$script_name' with $runner"
  case "$runner" in
    npm) (cd "$TARGET" && npm run --silent "$script_name") ;;
    *) (cd "$TARGET" && "$runner" run "$script_name") ;;
  esac
}

python_command() {
  if [ -x "$TARGET/.venv/bin/python" ]; then
    printf '%s\n' "$TARGET/.venv/bin/python"
  elif has_command python3; then
    command -v python3
  elif has_command python; then
    command -v python
  else
    return 1
  fi
}

run_override() {
  override_name=$1
  override_value=$2
  note "running command from $override_name"
  (cd "$TARGET" && sh -c "$override_value")
}

find_kit_root() {
  if [ -n "${HARNESS_KIT_ROOT:-}" ]; then
    if [ -d "$HARNESS_KIT_ROOT/checks" ]; then
      printf '%s\n' "$HARNESS_KIT_ROOT"
    elif [ -d "$HARNESS_KIT_ROOT/.harness/checks" ]; then
      printf '%s\n' "$HARNESS_KIT_ROOT/.harness"
    else
      printf '%s\n' "$HARNESS_KIT_ROOT"
    fi
    return
  fi

  common_dir=$(CDPATH= cd "$(dirname "$0")" && pwd -P)
  candidate=$(CDPATH= cd "$common_dir/../.." && pwd -P)
  if [ -d "$candidate/.harness/checks" ]; then
    printf '%s\n' "$candidate/.harness"
    return
  fi

  if [ -d "$TARGET/.harness/checks" ]; then
    printf '%s\n' "$TARGET/.harness"
    return
  fi

  printf '%s\n' ''
}
