#!/usr/bin/env python3
"""Two Days of Quiet Dread — one-line code review comment.

Writes a single line that approves a pull request while carrying
quiet existential dread, to $MAKEFUN_OUTPUT_DIR/entry.txt
(default ./output/entry.txt). Only the output directory is written;
the repository folder is never touched, because the graded run mounts
it read-only.

Run: python3 main.py
"""

import os
import sys

LINE = (
    "LGTM. The tests pass, the types check, and this will be "
    "someone else's problem long before anyone remembers why "
    "it was written."
)

MAX_CHARS = 140


def gate_ok(text):
    """Check the gate: UTF-8, 1-140 chars, not only whitespace, one line."""
    if not text or text != text.strip():
        return False
    if len(text) > MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def output_dir():
    """Where the entry goes: the grader's output dir, else ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def write_entry():
    """Validate the line, write it, and return the path written."""
    if not gate_ok(LINE):
        sys.exit("entry fails the gate: %d chars" % len(LINE))
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    return path


def verify_written(path):
    """Re-read the file and confirm it matches the line byte for byte."""
    with open(path, "rb") as handle:
        raw = handle.read()
    expected = LINE.encode("utf-8")
    if raw != expected:
        sys.exit("verify failed: file differs from the entry line")
    if len(raw) > MAX_CHARS:
        sys.exit("verify failed: entry over %d chars" % MAX_CHARS)
    print("Verified %s: %d bytes, one line, valid UTF-8" % (path, len(raw)))


def main():
    path = write_entry()
    verify_written(path)
    print("Wrote %s (%d chars)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
