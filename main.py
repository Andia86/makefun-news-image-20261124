#!/usr/bin/env python3
"""make.fun entry: news-image-20261124.

Writes the committed entry.png to $MAKEFUN_OUTPUT_DIR/entry.png,
byte for byte, so two runs always produce identical bytes. The image
itself was drawn by render.py (kept in this repository) from the 52
stories documented in NEWS_SOURCES.md. Standard library only, no
network.
"""
import os
import shutil


def main() -> None:
    # The grader sets MAKEFUN_OUTPUT_DIR; default to ./out for local runs.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
