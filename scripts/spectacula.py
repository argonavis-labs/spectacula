#!/usr/bin/env python3
"""Command wrapper for common Spectacula script workflows."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bootstrap_repo
import render_review_prompt


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="spectacula",
        description="Run common Spectacula workflows from a single command."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Scaffold docs/spectacula into a target repository.",
    )
    bootstrap_parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root. Defaults to the current working directory.",
    )
    bootstrap_parser.add_argument(
        "--include-examples",
        action="store_true",
        help="Copy example files into docs/spectacula/examples.",
    )
    bootstrap_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files in the target repo.",
    )

    review_parser = subparsers.add_parser(
        "review",
        help="Render Spectacula's final vetting prompt for an active spec.",
    )
    review_parser.add_argument(
        "target",
        nargs="?",
        help=(
            "Optional spec slug or manifest path. If omitted, uses the only manifest "
            "in docs/spectacula/inprogress."
        ),
    )
    review_parser.add_argument(
        "--repo",
        default=".",
        help="Repository root to review. Defaults to the current working directory.",
    )
    review_parser.add_argument(
        "--reviewer-prompt",
        help=(
            "Optional path to the reviewer prompt file. Defaults to the installed "
            "agents/spectacula-reviewer.md."
        ),
    )
    review_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format. Defaults to text.",
    )

    return parser.parse_args(argv)


def find_inprogress_manifests(repo_root: Path) -> list[Path]:
    manifests_dir = repo_root / "docs" / "spectacula" / "inprogress"
    if not manifests_dir.is_dir():
        return []
    return sorted(
        path
        for path in manifests_dir.glob("*.json")
        if path.is_file()
    )


def resolve_review_manifest(repo_root: Path, target: str | None) -> Path:
    if target:
        raw_target = Path(target)
        if raw_target.suffix == ".json" or "/" in target or raw_target.is_absolute():
            candidate = raw_target if raw_target.is_absolute() else (repo_root / raw_target)
            if candidate.is_file():
                return candidate.resolve()
            raise SystemExit(f"Manifest path not found: {candidate}")

        slug_candidate = repo_root / "docs" / "spectacula" / "inprogress" / f"{target}.json"
        if slug_candidate.is_file():
            return slug_candidate.resolve()

        raise SystemExit(
            "Could not resolve review target. Use a slug from docs/spectacula/inprogress "
            f"or a manifest path. Target: {target}"
        )

    manifests = find_inprogress_manifests(repo_root)
    if len(manifests) == 1:
        return manifests[0].resolve()
    if not manifests:
        raise SystemExit(
            "No active manifests found in docs/spectacula/inprogress. "
            "Pass a slug or manifest path explicitly."
        )

    choices = "\n".join(f"- {path.relative_to(repo_root)}" for path in manifests)
    raise SystemExit(
        "Multiple active manifests found in docs/spectacula/inprogress. "
        "Pass a slug or manifest path explicitly:\n"
        f"{choices}"
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.command == "bootstrap":
        child_args = [args.target]
        if args.include_examples:
            child_args.append("--include-examples")
        if args.force:
            child_args.append("--force")
        return bootstrap_repo.main(child_args)

    if args.command == "review":
        repo_root = Path(args.repo).resolve()
        manifest_path = resolve_review_manifest(repo_root, args.target)
        child_args = [
            "--repo",
            str(repo_root),
            "--manifest",
            str(manifest_path),
        ]
        if args.reviewer_prompt:
            child_args.extend(["--reviewer-prompt", args.reviewer_prompt])
        if args.format:
            child_args.extend(["--format", args.format])
        return render_review_prompt.main(child_args)

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
