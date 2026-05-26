#!/usr/bin/env python3
"""
Rebuild or audit derived sequence outputs from a component build plan.

This script is intentionally conservative. It does not invent sequences. It can:
  1. Audit existing sequence files and write a sequence inventory.
  2. Rebuild derived FASTA records only when a CSV build plan explicitly lists
     the exact component files to concatenate.

Recommended workflow:
  - First run in audit mode to inventory current sequence files.
  - Then create a reviewed sequence_build_plan.csv based on actual source files.
  - Run build mode to regenerate derived donor candidates from components.

Build-plan columns:
  output_record_id,output_path,component_paths,expected_length_bp,notes

component_paths should be a semicolon-separated list of paths relative to the
repository root. Each component file must contain one FASTA/plain DNA sequence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

DNA_RE = re.compile(r"^[ACGTNacgtn\-\.]+$")
FASTA_EXTS = {".fa", ".fasta", ".fna", ".ffn", ".fas"}


@dataclass
class InventoryRow:
    path: str
    record_id: str
    length_bp: int
    sha256: str
    notes: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def wrap_fasta(seq: str, width: int = 80) -> str:
    return "\n".join(seq[i:i + width] for i in range(0, len(seq), width))


def read_first_sequence(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if any(line.strip().startswith(">") for line in text.splitlines()):
        header = None
        parts: List[str] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is None:
                    header = line[1:].strip()
                elif parts:
                    break
            elif header is not None:
                parts.append(line.replace(" ", ""))
        if header is None:
            raise ValueError(f"No FASTA header found in {path}")
        seq = "".join(parts).upper()
        return header.split()[0], seq
    seq = "".join(line.strip() for line in text.splitlines() if not line.strip().startswith("#")).upper()
    seq = re.sub(r"\s+", "", seq)
    if not seq or not DNA_RE.match(seq):
        raise ValueError(f"Plain sequence file does not look like DNA: {path}")
    return path.stem, seq


def find_sequence_files(repo_root: Path) -> List[Path]:
    ignore = {".git", "__pycache__", ".pytest_cache"}
    files: List[Path] = []
    for path in repo_root.rglob("*"):
        if any(part in ignore for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in FASTA_EXTS.union({".txt"}):
            files.append(path)
    return sorted(files)


def audit_sequences(repo_root: Path, output_csv: Path) -> int:
    rows: List[InventoryRow] = []
    for path in find_sequence_files(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        try:
            record_id, seq = read_first_sequence(path)
            rows.append(InventoryRow(rel, record_id, len(seq.replace("-", "").replace(".", "")), sha256_file(path), "first_sequence_read"))
        except Exception as exc:  # noqa: BLE001
            rows.append(InventoryRow(rel, "READ_ERROR", 0, sha256_file(path), str(exc)))
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[field.name for field in InventoryRow.__dataclass_fields__.values()])
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    print(f"Sequence inventory complete: {len(rows)} file(s).")
    print(f"Wrote: {output_csv.as_posix()}")
    return 0


def build_from_plan(repo_root: Path, plan_csv: Path, output_manifest: Path) -> int:
    manifest_rows = []
    if not plan_csv.exists():
        raise FileNotFoundError(f"Build plan not found: {plan_csv}")
    with plan_csv.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"output_record_id", "output_path", "component_paths", "expected_length_bp"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Build plan missing required columns: {sorted(missing)}")
        for row in reader:
            output_record_id = row["output_record_id"].strip()
            output_path = repo_root / row["output_path"].strip()
            component_paths = [p.strip() for p in row["component_paths"].split(";") if p.strip()]
            expected = int(row["expected_length_bp"]) if row.get("expected_length_bp", "").strip() else None
            seq_parts = []
            component_ids = []
            for component in component_paths:
                record_id, seq = read_first_sequence(repo_root / component)
                component_ids.append(record_id)
                seq_parts.append(seq)
            sequence = "".join(seq_parts).upper()
            if not DNA_RE.match(sequence):
                raise ValueError(f"Non-DNA character detected while building {output_record_id}")
            if expected is not None and len(sequence.replace("-", "").replace(".", "")) != expected:
                raise ValueError(f"Length mismatch for {output_record_id}: expected {expected}, observed {len(sequence)}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fasta_text = f">{output_record_id} rebuilt_from_component_plan components={','.join(component_ids)}\n{wrap_fasta(sequence)}\n"
            output_path.write_text(fasta_text, encoding="utf-8")
            manifest_rows.append({
                "output_record_id": output_record_id,
                "output_path": output_path.relative_to(repo_root).as_posix(),
                "component_paths": ";".join(component_paths),
                "length_bp": len(sequence.replace("-", "").replace(".", "")),
                "sha256_sequence_text": sha256_text(sequence),
                "notes": row.get("notes", ""),
            })
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    with output_manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["output_record_id", "output_path", "component_paths", "length_bp", "sha256_sequence_text", "notes"])
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"Built {len(manifest_rows)} sequence output(s).")
    print(f"Wrote: {output_manifest.as_posix()}")
    return 0


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "output_record_id": "OCH1_ISC1alpha_full_donor_candidate",
            "output_path": "derived_sequences/OCH1_ISC1alpha_full_donor_candidate.fasta",
            "component_paths": "PATH_TO_OCH1_5P_ARM.fasta;PATH_TO_LINKER.fasta;PATH_TO_ISC1alpha_PAYLOAD.fasta;PATH_TO_OCH1_3P_ARM.fasta",
            "expected_length_bp": "2299",
            "notes": "Replace placeholder component paths with reviewed source files before build mode.",
        },
        {
            "output_record_id": "MNN2_ISC1beta_full_donor_candidate",
            "output_path": "derived_sequences/MNN2_ISC1beta_full_donor_candidate.fasta",
            "component_paths": "PATH_TO_MNN2_5P_ARM.fasta;PATH_TO_LINKER.fasta;PATH_TO_ISC1beta_PAYLOAD.fasta;PATH_TO_MNN2_3P_ARM.fasta",
            "expected_length_bp": "2299",
            "notes": "Replace placeholder component paths with reviewed source files before build mode.",
        },
        {
            "output_record_id": "MNN5_ISC1gamma_full_donor_candidate",
            "output_path": "derived_sequences/MNN5_ISC1gamma_full_donor_candidate.fasta",
            "component_paths": "PATH_TO_MNN5_5P_ARM.fasta;PATH_TO_LINKER.fasta;PATH_TO_ISC1gamma_PAYLOAD.fasta;PATH_TO_MNN5_3P_ARM.fasta",
            "expected_length_bp": "2299",
            "notes": "Replace placeholder component paths with reviewed source files before build mode.",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Audit or rebuild sequence files from a reviewed component plan.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--mode", choices=["audit", "build", "write-template"], default="audit")
    parser.add_argument("--plan", default="10_methods_and_provenance/sequence_build_plan.csv", help="Build plan CSV path relative to repo root.")
    parser.add_argument("--inventory-output", default="00_metadata/sequence_inventory.csv", help="Audit inventory output path relative to repo root.")
    parser.add_argument("--build-manifest-output", default="00_metadata/rebuilt_sequence_outputs.csv", help="Build manifest output path relative to repo root.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    if args.mode == "write-template":
        write_template(repo_root / args.plan)
        print(f"Wrote template build plan: {(repo_root / args.plan).as_posix()}")
        return 0
    if args.mode == "build":
        return build_from_plan(repo_root, repo_root / args.plan, repo_root / args.build_manifest_output)
    return audit_sequences(repo_root, repo_root / args.inventory_output)


if __name__ == "__main__":
    raise SystemExit(main())
