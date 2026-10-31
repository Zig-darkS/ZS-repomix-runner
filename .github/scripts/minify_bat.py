#!/usr/bin/env python3
"""Release-time minifier for _run-repomix.bat.

Strips: full-line `::` comments, full-line `rem` comments, blank lines,
trailing whitespace.

Keeps byte-for-byte: labels, gotos, cyrillic key mappings in :ASK, the
banner, the embedded JSON template (its indentation matters!), and the
`set RUNNER_VERSION=` line that the self-update check greps for.

Note: `::` is a label, not a comment, so it must NOT appear inside `(...)`
blocks in the source. This repo has none, so stripping them is safe.
"""
import re
import sys
from pathlib import Path

REM_RE = re.compile(r'(?i)^rem(?:[.\s]|$)')


def minify(text: str) -> str:
    out = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()

        if not stripped:
            continue
        if stripped.startswith('::'):
            continue
        if REM_RE.match(stripped):
            continue

        rstripped = raw.rstrip()
        # `echo` + only whitespace prints a blank line; bare `echo` prints
        # "ECHO is on." Normalize to `echo.` so rstrip can't break it.
        if rstripped == 'echo' and raw != 'echo':
            out.append('echo.')
            continue
        out.append(rstripped)

    return '\r\n'.join(out) + '\r\n'


def main(argv):
    if len(argv) != 3:
        print(f"usage: {argv[0]} <input.bat> <output.bat>", file=sys.stderr)
        return 2
    src, dst = Path(argv[1]), Path(argv[2])
    with open(src, 'r', encoding='utf-8-sig', newline='') as f:
        text = f.read()
    with open(dst, 'w', encoding='utf-8', newline='') as f:
        f.write(minify(text))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
