## Design decisions (settled)

- [X]  Release = **one required file**: `_run-repomix.bat`. Templates for `repomix.config.json` and `AGENTS.md` are embedded in the .bat
- [X]  Names stay as they are: `repomix.config.json`, `AGENTS.md`, `_repomix-output.xml` (the `_` prefix is only for sorting runner/output to the top)
- [X]  Never overwrite or modify an existing `repomix.config.json` / `AGENTS.md` / `.gitignore` content (only append one line to an existing `.gitignore`)
- [X]  No download branch `d`, no pinned config URL - the only network use is the self-update check
- [X]  `AGENTS.md` is the single place for AI instructions (used as Repomix `instructionFilePath`, and ignored in the dump to avoid a duplicate)

## `_run-repomix.bat` — implemented (needs testing on real Windows)

- [X]  `cd /d "%~dp0"` so it works from double-click
- [X]  `where node` before `where npm`, separate error for "node found but npm missing"
- [X]  Dead `endlocal` removed
- [X]  Config missing -> `[y]` create / `[s]` run once without config / `[n]` abort
- [X]  Unity detected (`ProjectSettings\ProjectVersion.txt`) -> ask whether to add Unity ignore patterns **to the config** (only when creating it)
- [X]  Config exists -> use as is, read `output.filePath` from it (for the banner and `.gitignore`)
- [X]  `AGENTS.md` missing -> ask, create stub with the "Zig darkS™ is cool UwU BTW" easter egg (only if the config uses `AGENTS.md`)
- [X]  Print `Created: <file name>` for every created file
- [X]  `.gitignore` exists and lacks the output name -> append it; no `.gitignore` -> do nothing
- [X]  Self-update: compares `RUNNER_VERSION` with the latest GitHub release asset, asks `[Y/N]`, skips silently offline / without `curl` / with `--no-update`

## Testing checklist

- [ ]  Clean folder, no config, no AGENTS.md, answer `y` + `y`
- [ ]  Clean folder, answer `s` (flags `--instruction-file-path`, `--ignore`, `-o`, `--output-show-line-numbers` — verify with `repomix --help`)
- [ ]  Folder with existing `repomix.config.json` that has a different `output.filePath`
- [ ]  Folder with existing `AGENTS.md`
- [ ]  `.gitignore` without trailing newline / with / absent
- [ ]  Unity project (config gets the extra patterns, JSON stays valid)
- [ ]  Self-update: older local version -> update -> rerun; offline run does not hang
- [ ]  Path with spaces and with parentheses, e.g. `C:\Program Files (x86)\Proj`
- [ ]  .bat must have **CRLF** line endings (otherwise labels/goto can break) — add `.gitattributes`: `*.bat text eol=crlf`

## Release

- [ ]  Bump `set RUNNER_VERSION=` before every release (the update check relies on it)
- [ ]  Keep the release asset named exactly `_run-repomix.bat` (URL: `https://github.com/Zig-darkS/ZS-repomix-runner/releases/latest/download/_run-repomix.bat`)
- [ ]  Confirm `LICENSE` and `.gitignore` stay **out** of release assets (repo-only)
- [X]  Release asset is minified (`dist/_run-repomix.bat` built by `.github/scripts/minify_bat.py`); repo keeps full source

## Docs

- [ ]  Short `README.md`: what it does, how to use, the `y/s/n` prompt, `AGENTS.md` behavior, self-update and `--no-update`
- [ ]  `CHANGELOG.md` or a release notes template
