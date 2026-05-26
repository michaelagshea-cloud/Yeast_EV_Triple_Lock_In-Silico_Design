from pathlib import Path
import sys

PIPELINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE))

from run_sequence_qc import parse_fasta, gc_fraction, run_qc  # noqa: E402


def test_parse_fasta_single_record():
    records = parse_fasta(">seq1 description\nACGT\nGGCC\n")
    assert len(records) == 1
    assert records[0].record_id == "seq1"
    assert records[0].sequence == "ACGTGGCC"


def test_gc_fraction_ignores_n():
    assert gc_fraction("GGCCNN") == 1.0
    assert gc_fraction("AATTNN") == 0.0


def test_run_qc_on_tmp_dna_fasta(tmp_path):
    repo = tmp_path
    fasta = repo / "test.fasta"
    fasta.write_text(">test\nACGTACGT\n", encoding="utf-8")

    results = run_qc(repo)

    assert len(results) == 1
    assert results[0].sequence_type == "dna"
    assert results[0].length_bp == 8
    assert results[0].length_observed == 8
    assert results[0].alphabet_status == "PASS"
    assert results[0].qc_status == "PASS"


def test_protein_translation_record_is_not_treated_as_failed_dna(tmp_path):
    repo = tmp_path
    fasta = repo / "protein_translation.fasta"
    fasta.write_text(
        ">example_protein_translation|length_6aa\nMKTWQ*\n",
        encoding="utf-8",
    )

    results = run_qc(repo)

    assert len(results) == 1
    assert results[0].sequence_type == "protein"
    assert results[0].length_observed == 6
    assert results[0].alphabet_status == "PASS"
    assert results[0].qc_status == "PASS"
    assert "Protein translation record" in results[0].notes
