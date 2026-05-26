# Yeast EV Triple-Lock In-Silico Design Package v1.0

This repository is a computational design and documentation package for three *Saccharomyces cerevisiae* / BY4741-compatible HDR donor candidates targeting **OCH1/YGL038C**, **MNN2/YBR015C**, and **MNN5/YJL186W**.

## Current status

**Computational design package only.**

This repository documents donor cassette architecture, ISC1/YER019W payload design, reference-gene provenance, locus-coordinate design, BY4741 target-locus compatibility checks, annotated construct records, Benchling visual imports, and sequence-level QC summaries.

This repository does **not** demonstrate yeast transformation, genomic integration, ISC1 expression, lipid remodeling, extracellular-vesicle phenotype, immune evasion, peptide loading, blood-brain-barrier delivery, disease modification, or therapeutic function. Those claims require future experimental validation.

## Design summary

Each full donor candidate is **2,299 bp** in transcript/synthesis orientation.

```text
500 bp 5-prime homology arm
+ retained native N-terminal anchor at the end of the 5-prime arm
+ 30 bp (GGGGS)2 linker
+ 1,269 bp ISC1/YER019W aa56-477 payload block including TAA
+ 500 bp 3-prime homology arm
```

Important wording: the **1,269 bp ISC1 payload block already includes the TAA stop codon**.

```text
1,266 bp coding sequence encoding ISC1/YER019W aa56-477
+ 3 bp TAA stop codon
= 1,269 bp total payload block
```

## Donor candidates

```text
OCH1/YGL038C donor:
OCH1 native anchor aa1-45
+ (GGGGS)2
+ ISC1alpha aa56-477 payload
+ TAA
+ OCH1 3-prime homology arm

MNN2/YBR015C donor:
MNN2 native anchor aa1-41
+ (GGGGS)2
+ ISC1beta aa56-477 payload
+ TAA
+ MNN2 3-prime homology arm

MNN5/YJL186W donor:
MNN5 native anchor aa1-45
+ (GGGGS)2
+ ISC1gamma aa56-477 payload
+ TAA
+ MNN5 3-prime homology arm
```

## Canonical folder order

```text
00_metadata
01_reference_gene_provenance
02_isc1_payload_design
03_isc1_payload_validation
04_locus_coordinate_design
05_full_donor_cassette_assembly
06_annotated_construct_records_and_maps
07_sequence_qc_and_validation_reports
08_genome_assembly_confidence
```

This order is appropriate for a dry-lab design package because it moves from metadata and source provenance, to payload design, to locus design, to full cassette assembly, to annotated construct records, to sequence QC, and finally to BY4741 assembly/locus-confidence addenda.

## What this package supports

The repository supports the following limited claims:

1. Three donor-cassette candidates were computationally assembled.
2. The donor candidates use OCH1, MNN2, and MNN5 target-locus architecture.
3. The ISC1/YER019W aa56-477 payload block is documented as a sequence-level design component.
4. Sequence-level QC summaries were generated for frame, translation, restriction-site screening, pairwise identity, repeat flags, and expected feature boundaries.
5. BY4741 target-locus compatibility was checked in silico for the target donor-package regions.

## What this package does not support

The repository does not support claims of:

- successful yeast editing or integration;
- stable engineered strain generation;
- ISC1 protein expression;
- altered sphingolipid metabolism;
- extracellular vesicle production changes;
- EV particle count, size, morphology, purity, or cargo loading;
- immune evasion or therapeutic delivery;
- animal, cell-culture, BBB, Alzheimer’s, or aging-brain efficacy;
- whole-genome structural validation of BY4741.

## Recommended publication-style additions

For a stronger dry-lab publication/reproducibility package, add the following before presenting the repository as publication-ready:

```text
09_reproducible_pipeline/
    generate_all_sequences.py
    run_sequence_qc.py
    rebuild_manifest.py
    requirements.txt or environment.yml
    README_pipeline.md

10_methods_and_provenance/
    methods_computational_design.md
    source_database_accessions.md
    tool_versions.txt
    command_log.txt

11_publication_readiness/
    data_availability_statement.md
    code_availability_statement.md
    claim_strength_audit.csv
    missing_files_checklist.csv
```

## Recommended citation and archiving

GitHub is useful for active version control. For publication, archive a fixed release through a DOI-issuing repository such as Zenodo or Figshare, then cite the archived version rather than a moving branch.

## License

The repository currently indicates CC-BY-4.0. If executable code is added later, consider adding a separate open-source software license for the code files while keeping CC-BY-4.0 for documentation/data.
