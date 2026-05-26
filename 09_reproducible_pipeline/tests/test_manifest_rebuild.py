from pathlib import Path
import sys

PIPELINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE))

from rebuild_manifest import build_manifest, infer_role  # noqa: E402


def test_infer_role_for_python_file():
    assert infer_role(Path("09_reproducible_pipeline/run_sequence_qc.py")) == "reproducible_code"


def test_build_manifest_counts_file(tmp_path):
    (tmp_path / "README.md").write_text("# test\n", encoding="utf-8")
    rows = build_manifest(tmp_path)
    assert len(rows) == 1
    assert rows[0].filename == "README.md"
    assert rows[0].inferred_role == "readme/documentation"
