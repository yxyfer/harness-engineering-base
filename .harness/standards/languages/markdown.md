# Markdown profile

- Format prose for source readability at 80 characters. Do not manually wrap
  tables, URLs, code blocks, badges, or other content that becomes less usable.
- Lint with markdownlint using project configuration and run the harness link
  check for local links.
- Use one level-one heading per document, sentence-case headings, fenced code
  blocks with a language where applicable, and descriptive link text.
- Use canonical uppercase filenames for the root project context documents;
  otherwise prefer `kebab-case.md`.
- Treat generated reports and imported source material as explicit exceptions;
  do not reflow them if doing so damages provenance or reproducibility.
- Markdownlint is a required standards tool when this profile applies; missing
  tools fail. It runs check-only. Use an existing project formatter script or
  configure commands.format for Markdown-only projects; no lint autofix is
  implied by the harness format command.
