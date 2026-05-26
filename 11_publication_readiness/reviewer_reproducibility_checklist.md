# Reviewer reproducibility checklist

Use this checklist before submitting or sharing the repository as publication-ready.

## Repository and archiving

- [ ] Repository is public.
- [ ] Repository has a versioned GitHub release.
- [ ] Release is archived with a persistent DOI.
- [ ] README clearly states computational-only status.
- [ ] License terms are clear for data/docs and code.

## Source provenance

- [ ] Every target gene has database accession, URL, and download date.
- [ ] Every payload sequence has extraction coordinates and source accession.
- [ ] Every Benchling/manual export has export date, filename, and checksum.
- [ ] Every derived donor sequence has a source component trail.

## Reproducibility scripts

- [ ] `rebuild_manifest.py` runs successfully.
- [ ] `generate_all_sequences.py --mode audit` runs successfully.
- [ ] `generate_all_sequences.py --mode build` runs successfully after component paths are reviewed.
- [ ] `run_sequence_qc.py` runs successfully.
- [ ] `visualize_design_model.py` generates Markdown diagrams.
- [ ] `pytest -q 09_reproducible_pipeline/tests` passes.
- [ ] GitHub Actions passes on the public repository.

## Claims

- [ ] No wording implies wet-lab validation.
- [ ] No wording implies therapeutic efficacy.
- [ ] No wording implies EV phenotype or peptide loading unless experimental files are added.
- [ ] Figures/diagrams are labeled as computational models.

## Manuscript/package readiness

- [ ] Data availability statement includes repository URL and DOI.
- [ ] Code availability statement includes repository URL and DOI.
- [ ] Methods cite exact databases and tools.
- [ ] Results distinguish design/QC findings from biological validation.
