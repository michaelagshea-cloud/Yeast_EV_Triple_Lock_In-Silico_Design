# Reproducible pipeline README

This folder adds a conservative reproducibility layer for the Yeast EV Triple-Lock in-silico design repository.

The scripts are designed for auditability, not biological validation. They can rebuild file manifests, inventory sequence files, run sequence QC, and generate visual workflow diagrams. They do **not** prove yeast transformation, genomic integration, ISC1 expression, EV phenotype, peptide loading, BBB delivery, or therapeutic function.

## Folder contents

```text
09_reproducible_pipeline/
    generate_all_sequences.py
    run_sequence_qc.py
    rebuild_manifest.py
    visualize_design_model.py
    expected_design_constraints.json
    requirements.txt
    README_pipeline.md
    tests/
        test_sequence_qc.py
        test_manifest_rebuild.py
## Recommended local setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
python -m pip install -r 09_reproducible_pipeline/requirements.txt
On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r 09_reproducible_pipeline/requirements.txt
## Step 1: rebuild the file manifest

```bash
python 09_reproducible_pipeline/rebuild_manifest.py --repo-root .
Output:

```text
00_metadata/rebuilt_file_manifest.csv
This records path, size, SHA-256 hash, extension, inferred file role, and MIME type.

## Step 2: inventory current sequence files

```bash
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode audit
Output:

```text
00_metadata/sequence_inventory.csv
This is the safest first pass because it does not modify sequences. It records which FASTA or DNA-like text files are currently present.

## Step 3: create a reviewed build plan

```bash
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode write-template
Output:

```text
10_methods_and_provenance/sequence_build_plan.csv
Then manually replace every placeholder path with the exact reviewed component files used to build each donor. Do not run build mode until the source paths are verified.

## Step 4: rebuild derived sequences from the reviewed plan

```bash
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode build
Output:

```text
derived_sequences/*.fasta
00_metadata/rebuilt_sequence_outputs.csv
The script concatenates only the exact components listed in the build plan. It raises an error if the observed output length does not match the expected length.

## Step 5: run sequence QC

```bash
python 09_reproducible_pipeline/run_sequence_qc.py --repo-root .
Output:

```text
07_sequence_qc_and_validation_reports/sequence_qc_results.csv
07_sequence_qc_and_validation_reports/sequence_qc_results.json
Use strict mode only when all expected design constraints have been verified:

```bash
python 09_reproducible_pipeline/run_sequence_qc.py --repo-root . --strict
## Step 6: generate visual workflow/design models

```bash
python 09_reproducible_pipeline/visualize_design_model.py --repo-root .
Output:

```text
10_methods_and_provenance/visual_design_models.md
GitHub renders the Mermaid diagrams directly in Markdown.

## Step 7: run tests

```bash
pytest -q 09_reproducible_pipeline/tests
## Reviewer-facing reproducibility claim

Use this wording until the full build plan has been verified:

> The repository includes a reproducibility layer that inventories source files, rebuilds a file manifest, performs sequence-level QC, and provides a reviewed build-plan format for regenerating derived donor sequences from explicit component files. The package remains computational and does not constitute experimental validation.
