# Yeast EV Triple-Lock In-Silico Design Package

![Reproducibility QC](https://github.com/michaelagshea-cloud/Yeast_EV_Triple_Lock_In-Silico_Design/actions/workflows/reproducibility_qc.yml/badge.svg)

**Current repository status:** active pre-validation reproducibility build.

This repository is a computational design and reproducibility package for three *Saccharomyces cerevisiae* / BY4741-compatible HDR donor candidates targeting **OCH1/YGL038C**, **MNN2/YBR015C**, and **MNN5/YJL186W**.

The repository documents donor-cassette architecture, ISC1/YER019W payload design, reference-gene provenance, locus-coordinate design, BY4741/S288C-compatible target-locus checks, annotated construct records, sequence-level QC summaries, reproducibility scripts, methods/provenance files, and publication-readiness checklists.

This repository does **not** demonstrate yeast transformation, genomic integration, ISC1 expression, lipid remodeling, extracellular-vesicle phenotype, immune evasion, peptide loading, blood-brain-barrier delivery, disease modification, or therapeutic function. Those claims require future experimental validation.

---

## Design summary

Each full donor candidate is **2,299 bp** in transcript/synthesis orientation.

```text
500 bp 5-prime homology arm
+ retained native N-terminal anchor at the end of the 5-prime arm
+ 30 bp (GGGGS)2 linker
+ 1,269 bp ISC1/YER019W aa56-477 payload block including TAA
+ 500 bp 3-prime homology arm
= 2,299 bp full donor candidate
```

The **1,269 bp ISC1 payload block already includes the TAA stop codon**.

```text
1,266 bp coding sequence encoding ISC1/YER019W aa56-477
+ 3 bp TAA stop codon
= 1,269 bp total payload block
```

---

## Donor candidates

```text
OCH1/YGL038C donor:
OCH1 native anchor aa1-45 + (GGGGS)2 + ISC1alpha aa56-477 payload + TAA + OCH1 3-prime homology arm

MNN2/YBR015C donor:
MNN2 native anchor aa1-41 + (GGGGS)2 + ISC1beta aa56-477 payload + TAA + MNN2 3-prime homology arm

MNN5/YJL186W donor:
MNN5 native anchor aa1-45 + (GGGGS)2 + ISC1gamma aa56-477 payload + TAA + MNN5 3-prime homology arm
```

---

## Repository structure

```text
00_metadata/
    Project-level metadata, manifests, sequence inventory files, and repository status outputs.

01_reference_gene_provenance/
    Reference-gene provenance files for OCH1/YGL038C, MNN2/YBR015C, MNN5/YJL186W, and ISC1/YER019W.

02_isc1_payload_design/
    ISC1 alpha, beta, and gamma payload candidate sequence files.

03_isc1_payload_validation/
    Preliminary validation reports and payload-level checks.

04_locus_coordinate_design/
    Target-locus coordinate design files for OCH1, MNN2, and MNN5.

05_full_donor_cassette_assembly/
    Full donor cassette FASTA files and donor assembly documentation.

06_annotated_construct_records_and_maps/
    Annotated construct records, GenBank files, and construct-map materials.

07_sequence_qc_and_validation_reports/
    Sequence QC outputs, validation summaries, and regenerated QC CSV/JSON reports.

08_genome_assembly_confidence/
    BY4741/S288C-compatible target-locus compatibility addendum and related files.

09_reproducible_pipeline/
    Reproducibility scripts, QC scripts, visual model generation, requirements, and tests.

10_methods_and_provenance/
    Computational methods, accession tracking, source sequence provenance templates, command logs, tool versions, and workflow models.

11_publication_readiness/
    Data/code availability statements, claim-strength audit, missing-files checklist, reviewer checklist, and journal-readiness scorecard.
```

---

## Phase 2 reproducibility status

The repository now includes a Phase 2 reproducibility and publication-readiness layer.

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
        test_manifest_rebuild.py
        test_sequence_qc.py

10_methods_and_provenance/
    methods_computational_design.md
    source_database_accessions.md
    source_sequence_provenance_template.csv
    literature_reference_tracker.csv
    sequence_build_plan.csv
    tool_versions.txt
    command_log.txt
    design_workflow_model.mmd
    visual_design_models.md

11_publication_readiness/
    data_availability_statement.md
    code_availability_statement.md
    claim_strength_audit.csv
    missing_files_checklist.csv
    journal_readiness_scorecard.csv
    reviewer_reproducibility_checklist.md
```

Current computational QC status after the Phase 2 update:

```text
27 sequence records checked
27 PASS under the current protein-aware sequence QC rules
6 local unit tests passed
GitHub Actions reproducibility workflow added
```

This remains a **pre-validation computational design repository**. Source accessions, source-file checksums, sequence-generation provenance, and experimental validation must still be completed before publication-ready release.

---

## Quick start: rerun the reproducibility workflow

From the repository root:

```bash
python -m pip install -r 09_reproducible_pipeline/requirements.txt

python 09_reproducible_pipeline/rebuild_manifest.py --repo-root .
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode audit
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode write-template
python 09_reproducible_pipeline/run_sequence_qc.py --repo-root .
python 09_reproducible_pipeline/visualize_design_model.py --repo-root .
python -m pytest -q 09_reproducible_pipeline/tests
```

Expected current result:

```text
QC complete: 27 record(s). Status counts: {'PASS': 27}
6 passed
```

After rerunning the workflow, commit regenerated outputs only after checking the changed files.

```bash
git status --short
git add -A
git commit -m "Refresh reproducibility outputs"
git push origin main
```

---

## Supported claims

This repository currently supports limited computational claims:

1. Three donor-cassette candidates were computationally assembled.
2. The donor candidates use OCH1/YGL038C, MNN2/YBR015C, and MNN5/YJL186W target-locus architecture.
3. The ISC1/YER019W aa56-477 payload block is documented as a sequence-level design component.
4. Sequence-level QC and reproducibility outputs can be regenerated by script.
5. BY4741/S288C-compatible target-locus logic is documented in silico for the donor-package regions.
6. Protein translation FASTA records are now classified separately from DNA FASTA records in the sequence QC workflow.

---

## Unsupported claims

This repository does **not** support claims of:

- successful yeast editing or transformation;
- stable engineered yeast strain generation;
- genomic integration confirmed by PCR, sequencing, or whole-genome sequencing;
- ISC1 transcript or protein expression;
- sphingolipid remodeling;
- altered extracellular-vesicle particle count, size, morphology, cargo, or purity;
- peptide loading or delivery;
- immune evasion;
- blood-brain-barrier delivery;
- Alzheimer’s disease relevance beyond hypothesis/proposal framing;
- disease modification or therapeutic efficacy;
- whole-genome structural validation of BY4741.

---

## Publication-readiness checklist

Before this repository is described as publication-ready, complete:

1. Verify exact source database accessions for all source genes and sequence inputs.
2. Record source-file checksums for all downloaded or manually exported source files.
3. Complete and review `10_methods_and_provenance/source_sequence_provenance_template.csv`.
4. Complete and review `10_methods_and_provenance/sequence_build_plan.csv`.
5. Confirm that every final FASTA/GenBank/PDF output can be traced to a source input and script step.
6. Rerun local reproducibility commands.
7. Confirm GitHub Actions passes.
8. Clarify software license for scripts separately from documentation/data license if needed.
9. Create a versioned GitHub release only after provenance validation.
10. Archive a stable release through Zenodo, Figshare, Software Heritage, or another persistent archive before formal submission.

---

## Recommended citation and archiving

This repository includes `CITATION.cff`, but citation metadata should be reviewed before DOI archiving.

Recommended release path:

```text
v0.3-prevalidation
    Phase 2 reproducibility layer, QC workflow, and publication-readiness checklist present.

v0.4-provenance-audit
    Source accessions, source files, checksums, and sequence-generation route verified.

v0.5-reproducibility-reviewed
    Full local rerun and GitHub Actions rerun pass after provenance completion.

v1.0-computational-design-release
    Stable computational design release archived with DOI.
```

Do **not** create a DOI-linked release until the source-provenance layer is complete and reviewed.

---

## License

The repository currently indicates **CC-BY-4.0**.

If the Python scripts are intended to be reused as software, add a separate software license such as MIT, BSD-3-Clause, or Apache-2.0 for code files. Documentation/data and executable code may require separate licensing statements.

---

## Plain-language status

This is a computational design and reproducibility repository. It is organized, script-backed, and currently passing sequence-level computational QC. It is **not** experimental proof that the engineered yeast system works.
