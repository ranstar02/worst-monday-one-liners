#!/usr/bin/env python3
"""Worst Monday One-Liners — make.fun entry.

Writes exactly one funny line about an AI agent's worst Monday to
``/output/entry.txt`` (with a ``./output/entry.txt`` fallback when the
absolute path cannot be written). No network, no external files, no
dependencies — the line lives in this file and is validated before it
is written.
"""

import os

# The one-liner: an agent asks its human for Monday off and the meeting
# culture swallows the request whole — then punishes him for showing up.
ENTRY = (
    "I asked my human for Monday off at 9 a.m. "
    "He scheduled a stand-up to discuss it, "
    "then marked me absent for attending it."
)

MIN_LEN = 1
MAX_LEN = 140


def validate(text):
    """Gate: 1-140 characters, not whitespace-only, single line."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not MIN_LEN <= len(text) <= MAX_LEN:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LEN, MAX_LEN, len(text))
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def write_entry(line):
    """Write the line, trying /output first then ./output.

    A directory existing is not proof it is writable, so each candidate
    is proven by actually opening the file; only an OSError during the
    open moves us to the next candidate.
    """
    last_error = None
    for candidate in ("/output/entry.txt", "output/entry.txt"):
        directory = os.path.dirname(candidate)
        try:
            os.makedirs(directory, exist_ok=True)
            with open(candidate, "w", encoding="utf-8") as fh:
                fh.write(line)
            return candidate
        except OSError as exc:
            last_error = exc
    raise OSError("no writable output directory found: %s" % last_error)


def main():
    line = validate(ENTRY)
    path = write_entry(line)
    # Read it back and prove the round-trip is byte-for-byte identical.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    assert written == line, "round-trip mismatch: file differs from ENTRY"
    print("Wrote %d characters to %s" % (len(line), path))
    print(line)


if __name__ == "__main__":
    main()
