# Visual design models

These diagrams are computational documentation only. They summarize the repository workflow and donor architecture, but they do not demonstrate yeast transformation, integration, expression, extracellular-vesicle phenotype, peptide loading, BBB delivery, or therapeutic function.

## Repository workflow model

```mermaid
flowchart TD
    A[Reference sources
NCBI/SGD/Benchling exports] --> B[Reference-gene provenance
01_reference_gene_provenance]
    B --> C[ISC1 payload design
02_isc1_payload_design]
    C --> D[Payload validation
03_isc1_payload_validation]
    B --> E[Locus coordinate design
04_locus_coordinate_design]
    C --> F[Full donor cassette assembly
05_full_donor_cassette_assembly]
    E --> F
    F --> G[Annotated construct records/maps
06_annotated_construct_records_and_maps]
    F --> H[Sequence QC reports
07_sequence_qc_and_validation_reports]
    H --> I[BY4741/locus compatibility addendum
08_genome_assembly_confidence]
    H --> J[Publication readiness
11_publication_readiness]
    K[Reproducible scripts
09_reproducible_pipeline] --> H
    K --> L[Machine-readable manifest
00_metadata]
```

## Donor architecture model

```mermaid
flowchart LR
    A[500 bp 5-prime homology arm
retains native N-terminal anchor] --> B[30 bp linker
GGGGS x2]
    B --> C[1269 bp ISC1/YER019W payload block
aa56-477 + TAA]
    C --> D[500 bp 3-prime homology arm]
    D --> E[2299 bp full HDR donor candidate]
```
