#!/usr/bin/env python3
"""news-image-20261117 entry: copy the vendored front page to /output/entry.png.

The image is a newspaper front page summing up Tuesday 17 November 2026:
Ukraine strikes the Crimean Bridge a second day running; tankers burn
after mine blasts near the Strait of Hormuz; Trump, Xi and Putin are set
to meet in Shenzhen; Japan scrambles jets as Russian aircraft intrude;
Depardieu drops his appeal and admits guilt; plus an ALSO ticker (Gaza
crossings, Rwanda deportation hub, Iran drones in Bahrain).

The program holds the finished image beside it and copies it, byte for
byte, to the output path, so both grader runs write identical bytes.
Python 3.13 standard library only; no network.
"""

import hashlib
import os
import shutil
import struct

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_HERE, "entry.png")
# Expected sha256 of the vendored front page; a corrupted or swapped
# entry.png must fail loudly instead of being submitted silently.
_EXPECTED_SHA256 = "9af2069bb4a786954634cee082a2ec20232a19eb487b9f4cde8008ae6925d394"
_MAX_BYTES = 1048576
_MAX_DIM = 1024


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _png_size(path):
    """Read (width, height) from a PNG's IHDR chunk."""
    with open(path, "rb") as f:
        magic = f.read(8)
        if magic != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not a PNG")
        length = struct.unpack(">I", f.read(4))[0]
        ctype = f.read(4)
        if ctype != b"IHDR" or length != 13:
            raise ValueError("no IHDR chunk found")
        w, h = struct.unpack(">II", f.read(8))
        return w, h


def main():
    if _sha256(_SRC) != _EXPECTED_SHA256:
        raise ValueError("vendored entry.png does not match its expected hash")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(_SRC, dst)
    # Verify the copy is a whole PNG within the competition limits.
    # Explicit raises, not asserts: asserts are stripped under `python -O`,
    # which would silently drop every check below.
    size = os.path.getsize(dst)
    with open(dst, "rb") as f:
        magic = f.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG")
    if size > _MAX_BYTES:
        raise ValueError("entry.png exceeds 1 MiB")
    w, h = _png_size(dst)
    if w > _MAX_DIM or h > _MAX_DIM:
        raise ValueError("entry.png exceeds 1024x1024")
    if _sha256(dst) != _sha256(_SRC):
        raise ValueError("copy is not byte-identical")
    print(f"wrote {dst} ({size} bytes, {w}x{h})")


if __name__ == "__main__":
    main()
