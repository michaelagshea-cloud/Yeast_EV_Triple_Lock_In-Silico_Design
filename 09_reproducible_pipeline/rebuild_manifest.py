#!/usr/bin/env python3
"""
Rebuild a machine-readable file manifest with size, SHA-256, extension, and role.

Typical usage:
    python 09_reproducible_pipeline/rebuild_manifest.py --repo-root .
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import mimetypes
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

IGNORE_DIRS = {".git", "__pycache__", ".pytest_cache"}


@dataclass
class ManifestRow:
    path: str
    folder: str
    filename: str
    extension: str
    size_bytes: int
    sha256: str
    inferred_role: str
    mime_type: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def infer_role(path: Path) -> str:
    lower = path.as_posix().lower()
    suffix = path.suffix.lower()
    if lower.endswith("readme.md"):
        return "readme/documentation"
    if "metadata" in lower or "manifest" in lower:
        return "metadata/manifest"
    if suffix in {".fa", ".fasta", ".fna", ".ffn", ".fas"}:
        return "sequence_fasta"
    if suffix in {".gb", ".gbk", ".genbank"}:
        return "annotated_sequence_record"
    if suffix == ".csv":
        return "tabular_metadata_or_results"
    if suffix == ".py":
        return "reproducible_code"
    if suffix in {".md", ".txt"}:
        return "plain_text_documentation"
    if suffix == ".pdf":
        return "visual_or_report_pdf"
    if suffix in {".json", ".yml", ".yaml"}:
        return "machine_readable_configuration"
    return "other"


def build_manifest(repo_root: Path) -> List[ManifestRow]:
    rows: List[ManifestRow] = []
    for path in sorted(repo_root.rglob("*")):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        mime, _ = mimetypes.guess_type(path.name)
        rows.append(
            ManifestRow(
                path=rel,
                folder=str(Path(rel).parent) if str(Path(rel).parent) != "." else "root",
                filename=path.name,
                extension=path.suffix.lower(),
                size_bytes=path.stat().st_size,
                sha256=sha256_file(path),
                inferred_role=infer_role(path),
                mime_type=mime or "unknown",
            )
        )
    return rows


def write_manifest(rows: List[ManifestRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [field.name for field in ManifestRow.__dataclass_fields__.values()]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild canonical repository file manifest.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--output", default="00_metadata/rebuilt_file_manifest.csv", help="Manifest output path relative to repo root.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    rows = build_manifest(repo_root)
    output_path = repo_root / args.output
    write_manifest(rows, output_path)
    print(f"Manifest complete: {len(rows)} file(s).")
    print(f"Wrote: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
