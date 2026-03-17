#!/usr/bin/env python3
"""Scaffold docs/spectacula into a target repository."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create docs/spectacula in a target repository from the Spectacula template."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--include-examples",
        action="store_true",
        help="Copy example files into docs/spectacula/examples.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files in the target repo.",
    )
    return parser.parse_args(argv)


def copy_tree(src: Path, dest: Path, force: bool) -> list[str]:
    written: list[str] = []
    if src.is_file():
        if dest.exists() and not force:
            return written
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        written.append(str(dest))
        return written

    dest.mkdir(parents=True, exist_ok=True)
    for source_path in sorted(src.rglob("*")):
        relative = source_path.relative_to(src)
        target_path = dest / relative
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue
        if target_path.exists() and not force:
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        written.append(str(target_path))
    return written


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    skill_root = Path(__file__).resolve().parent.parent
    source_root = skill_root / "assets" / "repo-template" / "docs" / "spectacula"
    if not source_root.is_dir():
        print(f"Template source not found: {source_root}", file=sys.stderr)
        return 1

    target_repo = Path(args.target).resolve()
    if not target_repo.exists() or not target_repo.is_dir():
        print(f"Target repo path does not exist or is not a directory: {target_repo}", file=sys.stderr)
        return 1

    target_root = target_repo / "docs" / "spectacula"
    written = []

    base_paths = ["README.md", "specs", "ready", "inprogress", "done", "templates"]
    for path_name in base_paths:
        written.extend(copy_tree(source_root / path_name, target_root / path_name, args.force))

    if args.include_examples:
        written.extend(copy_tree(source_root / "examples", target_root / "examples", args.force))

    print(f"Bootstrapped Spectacula into {target_root}")
    if written:
        print("Written files:")
        for path in written:
            print(f"- {path}")
    else:
        print("No files were written. Existing files were left unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
