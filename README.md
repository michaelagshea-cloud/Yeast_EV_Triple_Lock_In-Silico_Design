# Yeast EV Triple-Lock In Silico Design Package v1.0

This repository contains a clean computational design package for three *Saccharomyces cerevisiae* / BY4741-compatible HDR donor candidates targeting **OCH1/YGL038C**, **MNN2/YBR015C**, and **MNN5/YJL186W**.

Current status: **computational design package only**.

This package documents donor cassette architecture, ISC1 payload design, reference-gene provenance, locus coordinates, BY4741 locus compatibility, annotated construct records, Benchling visual imports, and sequence-QC summaries.

This repository does **not** demonstrate yeast transformation, genomic integration, ISC1 expression, lipid remodeling, extracellular vesicle phenotype, immune evasion, peptide loading, BBB delivery, or therapeutic function. Those require future experimental validation.

## Canonical design summary

Each full donor candidate is **2299 bp**.

Architecture:

```text
500 bp 5-prime homology arm, with retained native N-terminal anchor at the end of the arm
+ 30 bp (GGGGS)2 linker
+ 1269 bp ISC1/YER019W aa56-477 payload block including TAA
+ 500 bp 3-prime homology arm
```

The **1269 bp ISC1 payload block includes the TAA stop codon**:

```text
1266 bp coding sequence encoding ISC1/YER019W aa56-477
+ 3 bp TAA stop codon
= 1269 bp total payload block
```

## Donor designs

```text
OCH1 5-prime arm ending at codon 45
+ (GGGGS)2
+ ISC1alpha
+ TAA
+ OCH1 3-prime arm after native stop

MNN2 5-prime arm ending at codon 41
+ (GGGGS)2
+ ISC1beta
+ TAA
+ MNN2 3-prime arm after native stop

MNN5 5-prime arm ending at codon 45
+ (GGGGS)2
+ ISC1gamma
+ TAA
+ MNN5 3-prime arm after native stop
```

## Folder order

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
