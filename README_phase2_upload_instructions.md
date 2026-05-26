# Phase 2 upload instructions

Upload these folders/files into the root of the GitHub repository:

```text
.github/workflows/reproducibility_qc.yml
09_reproducible_pipeline/
10_methods_and_provenance/
11_publication_readiness/
README_phase2_upload_instructions.md
```

After uploading, run these commands locally from the repository root, or let GitHub Actions run them after commit:

```bash
python -m pip install -r 09_reproducible_pipeline/requirements.txt
python 09_reproducible_pipeline/rebuild_manifest.py --repo-root .
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode audit
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode write-template
python 09_reproducible_pipeline/run_sequence_qc.py --repo-root .
python 09_reproducible_pipeline/visualize_design_model.py --repo-root .
pytest -q 09_reproducible_pipeline/tests
```

Then upload the generated outputs:

```text
00_metadata/rebuilt_file_manifest.csv
00_metadata/sequence_inventory.csv
10_methods_and_provenance/sequence_build_plan.csv
07_sequence_qc_and_validation_reports/sequence_qc_results.csv
07_sequence_qc_and_validation_reports/sequence_qc_results.json
10_methods_and_provenance/visual_design_models.md
```

Do not claim publication-ready status until:

1. `sequence_build_plan.csv` contains exact reviewed component paths;
2. the build mode successfully regenerates donor FASTA files;
3. the GitHub Actions workflow passes;
4. the repository has a versioned release and DOI archive;
5. all source database accessions/download dates/checksums are filled in.
