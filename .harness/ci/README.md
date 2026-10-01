# Core CI

GitHub Actions is the default because this repository had no CI provider.
`.github/workflows/core.yml` uses one bounded `macos-15` Apple Silicon job,
read-only repository permissions, SHA-pinned actions and retained failure logs.
The runner image can change; the language runtimes and tools are exact pins.
The shell downloader also supports Intel macOS, but that branch is not locally
executed by the Apple Silicon verification run.

## Tools and scope

| Component | Pin | Scope |
| --- | --- | --- |
| Python / Node / npm | 3.14.0 / 24.10.0 / 11.6.0 | CI runtimes |
| ShellCheck / shfmt | 0.11.0 / 3.12.0 | Dispatcher, managed shell, CI setup |
| Markdownlint CLI2 | 0.23.3 | Maintained Markdown; native configs |
| Ruff / Pyright | 0.14.0 / 1.1.407 | Harness Python and Python fixture |
| Pytest | 8.4.2 | Required pytest contract cases |
| Prettier / ESLint / TypeScript | 3.9.6 / 10.10.0 / 7.0.2 | Existing Node fixture |

Ruff checks executable extensionless policy scripts as well as `.py` sources.
Pyright uses the root configuration for bin modules, contract tests and CI;
the Python fixture keeps its own strict configuration. Native tests and
fixture smoke run through the public dispatcher. The Node fixture is still a
minimal synthetic fixture, not a real Next.js application foundation.

CI sources and workflow settings are repository-owned authoring inputs, not
consumer release files. Only the two new native fixture Markdown configs are
added to the explicit release inventory. Dependency directories, environments,
caches and CI logs are never release inputs.

## Reproduce in a fresh checkout

Python 3.14.0, Node 24.10.0 and npm 11.6.0 must already be available. Dependency
downloads are setup work; checks use temporary local data and loopback servers.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: \
  -r .harness/ci/requirements.lock
npm ci --ignore-scripts --prefix .harness/ci
npm ci --ignore-scripts --prefix .harness/tests/fixtures/nextjs-project
sh .harness/ci/setup-shell.sh .harness/tmp/ci-bin
export PATH="$PWD/.venv/bin:$PWD/.harness/ci/node_modules/.bin:$PATH"
export PATH="$PWD/.harness/tmp/ci-bin:$PATH"
python3 .harness/ci/run.py static
python3 .harness/ci/run.py contracts
python3 .harness/ci/run.py fixtures
python3 .harness/ci/run.py negatives
```

`run.py` fails when required tools are missing. Commands have a 180-second
limit; the job has a 20-minute limit. Completed commands record their exit,
duration, arguments, working directory and a unique full-output log in
`.harness/tmp/ci-logs/`. Expected negative exits must include the intended
diagnostic. Source fingerprints check that negative controls leave the checkout
unchanged. Logs are retained for seven days on GitHub, including failed jobs.

Python dependency upgrades are explicit release-authoring work. Regenerate
`requirements.lock` with pip-tools 7.5.0 using `requirements.in`, review changes,
then prove a fresh `pip install --require-hashes` succeeds. Node upgrades use
reviewed exact pins and lockfiles; CI only runs `npm ci`, never `npm update`.
Shell downloads validate committed SHA-256 digests before executing tools.

This workflow does not install the harness into another project, configure
branch protection or provide future profile/doctor/verification interfaces.
Local developer commands still allow explicit degraded optional-tool coverage;
the CI static phase requires actual tools. Remote execution must be separately
evidenced; a workflow file or local pass is not a GitHub run.
