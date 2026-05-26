# Code availability statement

## Current repository wording

The repository includes Python scripts for manifest rebuilding, sequence inventory/rebuild planning, sequence-level QC, and GitHub-rendered visual workflow models:

```text
09_reproducible_pipeline/rebuild_manifest.py
09_reproducible_pipeline/generate_all_sequences.py
09_reproducible_pipeline/run_sequence_qc.py
09_reproducible_pipeline/visualize_design_model.py
09_reproducible_pipeline/tests/
```

## Required before manuscript submission

Before claiming the code package is publication-ready, add:

1. a tested GitHub Actions workflow status badge;
2. a versioned release;
3. a Zenodo/Figshare/Software Heritage DOI;
4. a full software license for scripts, if different from the data/documentation license;
5. exact runtime versions in `10_methods_and_provenance/tool_versions.txt`;
6. command history in `10_methods_and_provenance/command_log.txt`;
7. test results from `pytest -q 09_reproducible_pipeline/tests`.

## Draft publication-ready wording after release/DOI

Replace bracketed fields before use:

> Custom Python code used to inventory sequence files, rebuild the file manifest, run sequence-level QC, and generate visual workflow documentation is available in the public GitHub repository [GITHUB URL] and archived at [ARCHIVE DOI]. The scripts were tested with Python [VERSION] and pytest [VERSION]. Exact commands are recorded in `10_methods_and_provenance/command_log.txt`. The code performs computational reproducibility checks only and does not constitute experimental validation of the donor designs.
