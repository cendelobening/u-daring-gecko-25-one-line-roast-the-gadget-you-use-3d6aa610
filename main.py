#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day.

Writes a single original roast line to entry.txt.
Pure Python standard library only; no network access.
"""

import os
import tempfile

LINE = (
    "My banking app needs a selfie, a PIN, and a one-time code "
    "to prove I'm me, then still asks if I'm sure about spending "
    "my own money."
)


def main() -> None:
    line = LINE
    if not line or not line.strip():
        raise ValueError("roast line must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("roast line must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError("roast line must be 1-200 characters")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, out_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(out_path, 0o644)

    # Verify the write round-tripped exactly before declaring success.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        if f.read() != line:
            raise ValueError("written entry does not match the roast line")
    print(f"Wrote {len(line)}-character entry to {out_path}")


if __name__ == "__main__":
    main()
