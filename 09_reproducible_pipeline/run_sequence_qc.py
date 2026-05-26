#!/usr/bin/env python3
"""
Run sequence-level QC for the Yeast EV Triple-Lock in-silico design package.

This script intentionally uses only the Python standard library so reviewers can
run it without specialized bioinformatics installation friction. It does not
claim biological validation. It checks file integrity, FASTA syntax, alphabet,
record lengths, GC content, and design-rule warnings where filenames or record
IDs match known project patterns.

Typical usage from the repository root:
    python 09_reproducible_pipeline/run_sequence_qc.py --repo-root .
    python 09_reproducible_pipeline/run_sequence_qc.py --repo-root . --strict
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Iterator, List, Dict, Any, Optional, Tuple

DNA_RE = re.compile(r"^[ACGTNacgtn\-\.]+$")
FASTA_EXTS = {".fa", ".fasta", ".fna", ".ffn", ".fas"}
TEXT_SEQ_EXTS = {".txt"}


@dataclass
class FastaRecord:
    record_id: str
    description: str
    sequence: str


@dataclass
class QCResult:
    path: str
    record_id: str
    length_bp: int
    gc_fraction: float
    n_count: int
    gap_or_dot_count: int
    sha256: str
    alphabet_status: str
    expected_rule: str
    expected_length_bp: str
    length_status: str
    qc_status: str
    notes: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_fasta(text: str) -> List[FastaRecord]:
    records: List[FastaRecord] = []
    header: Optional[str] = None
    seq_parts: List[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records.append(_record_from_parts(header, seq_parts))
            header = line[1:].strip()
            seq_parts = []
        else:
            if header is None:
                raise ValueError("Sequence content found before FASTA header")
            seq_parts.append(line.replace(" ", ""))

    if header is not None:
        records.append(_record_from_parts(header, seq_parts))
    return records


def _record_from_parts(header: str, seq_parts: List[str]) -> FastaRecord:
    sequence = "".join(seq_parts).upper()
    record_id = header.split()[0] if header else "unnamed_record"
    return FastaRecord(record_id=record_id, description=header, sequence=sequence)


def parse_plain_sequence(path: Path) -> List[FastaRecord]:
    """Parse simple sequence text only if it looks mostly like DNA.

    A plain-text file may contain characters such as >= in requirements.txt,
    so only call FASTA parsing if a line actually starts with a FASTA header.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    if any(line.strip().startswith(">") for line in text.splitlines()):
        return parse_fasta(text)
    candidate = "".join(line.strip() for line in text.splitlines() if not line.strip().startswith("#"))
    candidate = re.sub(r"\s+", "", candidate).upper()
    if not candidate:
        return []
    # Avoid treating prose notes as DNA. Require 90% DNA-ish characters and at least 20 bp.
    dna_chars = sum(1 for c in candidate if c in "ACGTN-." )
    if len(candidate) >= 20 and dna_chars / max(len(candidate), 1) >= 0.90:
        return [FastaRecord(path.stem, path.stem, candidate)]
    return []


def gc_fraction(seq: str) -> float:
    clean = [base for base in seq.upper() if base in "ACGTN"]
    denom = sum(1 for base in clean if base in "ACGT")
    if denom == 0:
        return 0.0
    return sum(1 for base in clean if base in "GC") / denom


def load_constraints(repo_root: Path, explicit_path: Optional[Path]) -> Dict[str, Any]:
    if explicit_path:
        path = explicit_path
    else:
        path = repo_root / "09_reproducible_pipeline" / "expected_design_constraints.json"
        if not path.exists():
            path = Path(__file__).resolve().parent / "expected_design_constraints.json"
    if not path.exists():
        return {"record_rules": []}
    return json.loads(path.read_text(encoding="utf-8"))


def match_rule(record: FastaRecord, path: Path, constraints: Dict[str, Any]) -> Tuple[str, str, str]:
    haystack = f"{path.as_posix()} {record.record_id} {record.description}".lower()
    for rule in constraints.get("record_rules", []):
        patterns = [p.lower() for p in rule.get("match_any_case_insensitive", [])]
        if any(p in haystack for p in patterns):
            return str(rule.get("name", "matched_rule")), str(rule.get("expected_length_bp", "")), str(rule.get("severity", "warn"))
    return "", "", ""


def collect_sequence_files(repo_root: Path) -> List[Path]:
    ignored = {".git", "__pycache__", ".pytest_cache"}
    paths: List[Path] = []
    for path in repo_root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in FASTA_EXTS or suffix in TEXT_SEQ_EXTS:
            paths.append(path)
    return sorted(paths)


def qc_record(path: Path, record: FastaRecord, repo_root: Path, constraints: Dict[str, Any]) -> QCResult:
    seq = record.sequence.upper()
    rel = path.relative_to(repo_root).as_posix() if path.is_relative_to(repo_root) else path.as_posix()
    alphabet_status = "PASS" if DNA_RE.match(seq or "") else "FAIL"
    n_count = seq.count("N")
    gap_or_dot_count = seq.count("-") + seq.count(".")
    rule_name, expected_len, severity = match_rule(record, path, constraints)
    length_status = "NOT_CHECKED"
    notes: List[str] = []

    if expected_len:
        try:
            expected_int = int(expected_len)
            length_status = "PASS" if len(seq) == expected_int else severity.upper()
            if len(seq) != expected_int:
                notes.append(f"Expected {expected_int} bp by rule {rule_name}; observed {len(seq)} bp.")
        except ValueError:
            length_status = "NOT_CHECKED"

    if alphabet_status == "FAIL":
        notes.append("Non-DNA characters detected; inspect source file and sequence wrapping.")
    if n_count > 0:
        notes.append(f"Contains {n_count} ambiguous N base(s).")
    if gap_or_dot_count > 0:
        notes.append(f"Contains {gap_or_dot_count} gap/dot character(s).")

    qc_status = "PASS"
    if alphabet_status == "FAIL" or length_status == "FAIL":
        qc_status = "FAIL"
    elif length_status == "WARN" or n_count > 0 or gap_or_dot_count > 0:
        qc_status = "WARN"

    return QCResult(
        path=rel,
        record_id=record.record_id,
        length_bp=len(seq.replace("-", "").replace(".", "")),
        gc_fraction=round(gc_fraction(seq), 6),
        n_count=n_count,
        gap_or_dot_count=gap_or_dot_count,
        sha256=sha256_file(path),
        alphabet_status=alphabet_status,
        expected_rule=rule_name,
        expected_length_bp=expected_len,
        length_status=length_status,
        qc_status=qc_status,
        notes=" | ".join(notes),
    )


def run_qc(repo_root: Path, constraints_path: Optional[Path] = None) -> List[QCResult]:
    constraints = load_constraints(repo_root, constraints_path)
    results: List[QCResult] = []
    for path in collect_sequence_files(repo_root):
        try:
            if path.suffix.lower() in FASTA_EXTS:
                records = parse_fasta(path.read_text(encoding="utf-8", errors="replace"))
            else:
                records = parse_plain_sequence(path)
        except Exception as exc:  # noqa: BLE001 - reviewers need file-level failure in output
            rel = path.relative_to(repo_root).as_posix() if path.is_relative_to(repo_root) else path.as_posix()
            results.append(QCResult(rel, "PARSE_ERROR", 0, 0.0, 0, 0, sha256_file(path), "FAIL", "", "", "FAIL", "FAIL", str(exc)))
            continue
        for record in records:
            results.append(qc_record(path, record, repo_root, constraints))
    return results


def write_outputs(results: List[QCResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "sequence_qc_results.csv"
    json_path = output_dir / "sequence_qc_results.json"
    fields = list(asdict(results[0]).keys()) if results else [field.name for field in QCResult.__dataclass_fields__.values()]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow(asdict(row))
    json_path.write_text(json.dumps([asdict(row) for row in results], indent=2), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run sequence QC for the Yeast EV Triple-Lock design repository.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--constraints", default=None, help="Optional path to expected_design_constraints.json.")
    parser.add_argument("--output-dir", default="07_sequence_qc_and_validation_reports", help="Output directory for QC CSV/JSON.")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero on WARN as well as FAIL.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    constraints = Path(args.constraints).resolve() if args.constraints else None
    output_dir = repo_root / args.output_dir
    results = run_qc(repo_root, constraints)
    write_outputs(results, output_dir)

    if not results:
        print("No sequence records found. Check FASTA/TXT source files or repo root.", file=sys.stderr)
        return 2 if args.strict else 0

    status_counts: Dict[str, int] = {}
    for result in results:
        status_counts[result.qc_status] = status_counts.get(result.qc_status, 0) + 1
    print(f"QC complete: {len(results)} record(s). Status counts: {status_counts}")
    print(f"Wrote: {(output_dir / 'sequence_qc_results.csv').as_posix()}")
    print(f"Wrote: {(output_dir / 'sequence_qc_results.json').as_posix()}")

    if any(result.qc_status == "FAIL" for result in results):
        return 1
    if args.strict and any(result.qc_status == "WARN" for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
