# Shell profile

- Target POSIX `sh` by default. Use Bash or zsh only when a required feature is
  named in the shebang and documented.
- Format with shfmt using two-space indentation and an 80-character target where
  wrapping remains readable. Validate with ShellCheck.
- Use `snake_case` for local variables/functions and `UPPER_SNAKE_CASE` for
  exported environment variables and constants.
- Quote expansions unless intentional splitting is required. Prefer explicit
  argument arrays in shells that support them.
- Test observable command behaviour, exit codes, and failure messages. Include
  paths containing spaces for filesystem commands.
- Scope ShellCheck directives to the relevant line and record why the warning is
  safe to suppress.
- The standards policy requires ShellCheck and shfmt for maintained shell files;
  missing tools fail. Check uses shfmt diff mode, never writes. Configure a
  project format command using shfmt write mode for shell-only formatting.
