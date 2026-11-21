#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered poster to the grader's output dir.
Standard library only; deterministic (same bytes on every run)."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "poster.png"),
                    os.path.join(out, "entry.png"))


if __name__ == "__main__":
    main()
