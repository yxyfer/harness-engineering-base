#!/bin/sh

set -eu

command_name=${HARNESS_COMMAND_NAME:-harness}

fail() {
  printf '%s: %s\n' "${command_name}" "$*" >&2
  exit 1
}

usage_error() {
  printf '%s: %s\n' "${command_name}" "$*" >&2
  exit 2
}

installation_error() {
  printf '%s: installation error: %s\n' "${command_name}" "$*" >&2
  exit 5
}

note() {
  printf '%s: %s\n' "${command_name}" "$*"
}

warn() {
  printf '%s: warning: %s\n' "${command_name}" "$*" >&2
}

resolve_target() {
  target_input=${1:-.}
  [ -d "${target_input}" ] || fail "target directory does not exist: ${target_input}"
  TARGET=$(CDPATH='' cd "${target_input}" && pwd -P)
  export TARGET
  resolve_harness_contract
}

has_command() {
  command -v "$1" >/dev/null 2>&1
}

has_npm_script() {
  script_name=$1
  [ -f "${TARGET}/package.json" ] || return 1
  # Status selector; a non-zero result is expected and handled.
  # shellcheck disable=SC2310
  has_command node || return 1
  node -e '
    const p = require(process.argv[1]);
    process.exit(p.scripts && p.scripts[process.argv[2]] ? 0 : 1);
  ' "${TARGET}/package.json" "${script_name}" >/dev/null 2>&1
}

node_runner() {
  if [ -f "${TARGET}/pnpm-lock.yaml" ]; then
    printf '%s\n' pnpm
  elif [ -f "${TARGET}/yarn.lock" ]; then
    printf '%s\n' yarn
  else
    printf '%s\n' npm
  fi
}

run_node_script() {
  script_name=$1
  runner=$(node_runner)
  # Status selector; a non-zero result is expected and handled.
  # shellcheck disable=SC2310
  has_command "${runner}" || fail "${runner} is required to run the '${script_name}' script"
  note "running package script '${script_name}' with ${runner}"
  case "${runner}" in
  npm) run_project_command npm run --silent "${script_name}" ;;
  *) run_project_command "${runner}" run "${script_name}" ;;
  esac
}

python_command() {
  python_target=${1:-${TARGET}}
  # Status selectors below deliberately report missing runtimes.
  # shellcheck disable=SC2310
  if [ -x "${python_target}/.venv/bin/python" ]; then
    printf '%s\n' "${python_target}/.venv/bin/python"
  elif has_command python3; then
    command -v python3
  elif has_command python; then
    command -v python
  else
    return 1
  fi
}

use_project_python_environment() {
  if [ -x "${TARGET}/.venv/bin/python" ]; then
    PATH="${TARGET}/.venv/bin:${PATH}"
    VIRTUAL_ENV="${TARGET}/.venv"
    export PATH VIRTUAL_ENV
  fi
}

run_override() {
  override_name=$1
  override_value=$2
  note "running command from ${override_name}"
  run_project_command sh -c "${override_value}"
}

run_project_command() {
  if (cd "${TARGET}" && "$@"); then
    return 0
  else
    project_status=$?
    fail "project command failed with exit ${project_status}"
  fi
}

find_kit_root() {
  if [ -n "${HARNESS_KIT_ROOT:-}" ]; then
    if [ -d "${HARNESS_KIT_ROOT}/checks" ]; then
      printf '%s\n' "${HARNESS_KIT_ROOT}"
    elif [ -d "${HARNESS_KIT_ROOT}/.harness/checks" ]; then
      printf '%s\n' "${HARNESS_KIT_ROOT}/.harness"
    else
      printf '%s\n' "${HARNESS_KIT_ROOT}"
    fi
    return
  fi

  common_dir=$(CDPATH='' cd "$(dirname "$0")" && pwd -P)
  candidate=$(CDPATH='' cd "${common_dir}/../.." && pwd -P)
  if [ -d "${candidate}/.harness/checks" ]; then
    printf '%s\n' "${candidate}/.harness"
    return
  fi

  if [ -d "${TARGET}/.harness/checks" ]; then
    printf '%s\n' "${TARGET}/.harness"
    return
  fi

  printf '%s\n' ''
}

resolve_harness_contract() {
  KIT_ROOT=$(find_kit_root)
  [ -n "${KIT_ROOT}" ] || installation_error 'managed .harness directory not found'
  CONFIG_TOOL="${KIT_ROOT}/bin/config.py"
  MANIFEST_TOOL="${KIT_ROOT}/bin/manifest.py"
  [ -f "${CONFIG_TOOL}" ] || installation_error 'config validator is missing'
  [ -f "${MANIFEST_TOOL}" ] || installation_error 'manifest validator is missing'
  # Status selector; a non-zero result is expected and handled.
  # shellcheck disable=SC2310
  has_command python3 || installation_error 'Python 3.11 or newer is required'
  python3 -c 'import tomllib' >/dev/null 2>&1 ||
    installation_error 'Python 3.11 or newer with tomllib is required'

  if [ -n "${HARNESS_CONFIG:-}" ]; then
    CONFIG_PATH=${HARNESS_CONFIG}
    CONFIG_SOURCE=${HARNESS_CONFIG_SOURCE:-environment}
  elif [ -f "${TARGET}/.harness/config.toml" ]; then
    CONFIG_PATH="${TARGET}/.harness/config.toml"
    CONFIG_SOURCE=project
  elif [ -f "${KIT_ROOT}/default-config.toml" ]; then
    CONFIG_PATH="${KIT_ROOT}/default-config.toml"
    CONFIG_SOURCE=harness-default
  else
    installation_error 'config.toml is missing'
  fi
  export KIT_ROOT CONFIG_TOOL MANIFEST_TOOL CONFIG_PATH CONFIG_SOURCE
  python3 "${CONFIG_TOOL}" validate "${CONFIG_PATH}"
}

config_value() {
  python3 "${CONFIG_TOOL}" get "${CONFIG_PATH}" "$1"
}

config_list() {
  python3 "${CONFIG_TOOL}" list "${CONFIG_PATH}" "$1"
}

environment_command() {
  case "$1" in
  setup) printf '%s\n' "${HARNESS_SETUP_COMMAND:-}" ;;
  start) printf '%s\n' "${HARNESS_START_COMMAND:-}" ;;
  check) printf '%s\n' "${HARNESS_CHECK_COMMAND:-}" ;;
  test) printf '%s\n' "${HARNESS_TEST_COMMAND:-}" ;;
  smoke) printf '%s\n' "${HARNESS_SMOKE_COMMAND:-}" ;;
  *) usage_error "unknown command override: $1" ;;
  esac
}

command_override() {
  action=$1
  if [ -n "${HARNESS_CLI_COMMAND:-}" ]; then
    printf '%s\n' "${HARNESS_CLI_COMMAND}"
    return 0
  fi
  # Propagate helper failure explicitly; do not rely on conditional errexit.
  # shellcheck disable=SC2310
  environment_value=$(environment_command "${action}") || return "$?"
  if [ -n "${environment_value}" ]; then
    printf '%s\n' "${environment_value}"
    return 0
  fi
  # Propagate validator failure explicitly; absence remains a selector result.
  # shellcheck disable=SC2310
  configured_value=$(config_value "commands.${action}") || return "$?"
  if [ -n "${configured_value}" ]; then
    printf '%s\n' "${configured_value}"
    return 0
  fi
  return 1
}

command_override_source() {
  action=$1
  if [ -n "${HARNESS_CLI_COMMAND:-}" ]; then
    printf '%s\n' cli
    return 0
  fi
  environment_value=$(environment_command "${action}")
  if [ -n "${environment_value}" ]; then
    environment_name=$(printf '%s' "${action}" | tr '[:lower:]' '[:upper:]')
    printf 'environment HARNESS_%s_COMMAND\n' "${environment_name}"
    return 0
  fi
  configured_value=$(config_value "commands.${action}")
  if [ -n "${configured_value}" ]; then
    printf '%s config\n' "${CONFIG_SOURCE}"
    return 0
  fi
  return 1
}
