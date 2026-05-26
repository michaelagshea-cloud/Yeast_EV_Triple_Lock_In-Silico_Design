# Repository Validation Report

Repository: `michaelagshea-cloud/Yeast_EV_Triple_Lock_In-Silico_Design`

Review status: public GitHub repository reviewed as an in-silico design package.

## Overall assessment

The current repository order is logical and mostly publication-style for a computational design archive. It already separates source-gene provenance, ISC1 payload design, payload validation, locus-coordinate design, donor-cassette assembly, annotated construct records, sequence QC, and BY4741 assembly/locus compatibility.

The strongest part of the repository is its restraint: the README and validation report clearly state that the package is computational only and does not demonstrate transformation, genomic integration, expression, EV phenotype, immune evasion, BBB delivery, or therapeutic function.

The main weakness is reproducibility. The repository contains the generated output files, checksums, reports, and construct records, but it does not yet contain the full executable pipeline that regenerates every FASTA, CSV, GenBank, checksum, and QC result from the stated reference inputs.

## Folder-order review

PASS: The current folder order makes sense.

Recommended interpretation:

```text
00_metadata = inventory, manifest, data dictionary, checksums, version notes
01_reference_gene_provenance = source/reference records
02_isc1_payload_design = payload blocks and payload design notes
03_isc1_payload_validation = payload QC, translation checks, pairwise identity
04_locus_coordinate_design = locus coordinates, BY4741/R64 compatibility logic
05_full_donor_cassette_assembly = final donor FASTA files and feature tables
06_annotated_construct_records_and_maps = GenBank and visual construct records
07_sequence_qc_and_validation_reports = synthesis/QC/restriction/primer reports
08_genome_assembly_confidence = BY4741 target-locus compatibility addendum
```

Suggested improvement: rename `08_genome_assembly_confidence` to `08_by4741_locus_compatibility` unless true genome-wide BUSCO, SV/synteny, or read-mapping evidence is added. The current contents support target-locus compatibility, not full genome-assembly confidence.

## Missing publication-style files

High priority additions:

1. `00_metadata/data_dictionary.csv`  
   Explains every CSV column and how to interpret each file.

2. `00_metadata/claim_strength_audit.csv`  
   Separates supported computational claims from unsupported biological claims.

3. `09_reproducible_pipeline/`  
   Scripts that regenerate the FASTA, CSV, GenBank, reports, and manifest from the raw/reference inputs.

4. `09_reproducible_pipeline/requirements.txt` or `environment.yml`  
   Software versions and dependencies.

5. `09_reproducible_pipeline/run_all.sh`  
   One command that rebuilds the package.

6. `10_methods_and_provenance/methods_computational_design.md`  
   Step-by-step computational method, without wet-lab transformation claims.

7. `10_methods_and_provenance/tool_versions.txt`  
   Python version, package versions, sequence tools, Benchling export date/version if known.

8. `11_publication_readiness/data_availability_statement.md`  
   States what data are in GitHub, what external databases were used, and what is not included.

9. `11_publication_readiness/code_availability_statement.md`  
   Required once analysis code is added.

10. A fixed release archive with DOI.  
   A GitHub branch can change. A publication should cite a fixed release.

## Claim-strength audit

Supported with current repository files:

- Computational donor candidate design.
- Documented use of OCH1/YGL038C, MNN2/YBR015C, MNN5/YJL186W, and ISC1/YER019W reference logic.
- Donor architecture of 500 bp 5-prime arm + linker + ISC1 payload + 500 bp 3-prime arm.
- In-silico sequence QC, translation/frame checks, restriction-site screens, and feature-boundary documentation.
- BY4741 target-locus compatibility for checked regions.

Use with caution:

- “Computationally validated.” This is acceptable only when immediately qualified as sequence-level/in-silico validation.
- “BY4741-compatible.” Safer wording: “BY4741 target-locus compatible in silico.”
- “Genome assembly confidence.” Safer wording: “target-locus compatibility addendum.”

Not supported:

- transformation;
- genomic integration;
- protein expression;
- altered lipid metabolism;
- EV phenotype;
- EV yield, size, purity, cargo loading, or uptake;
- immune evasion;
- BBB delivery;
- Alzheimer’s, aging-brain, disease, or therapeutic effects;
- whole-genome structural validation.

## Recommended final status statement

Use this wording in the README and reports:

> This repository is a versioned in-silico donor-candidate design package. It supports sequence-level documentation, donor architecture review, reference-gene provenance, and computational QC of three HDR donor candidates. It does not provide experimental evidence of editing, expression, EV phenotype, cargo loading, therapeutic delivery, or biological function.

## Bottom line

The repository is organized well enough for a clean dry-lab design archive. It is not yet a full publication-grade reproducibility package because the code and command-level regeneration workflow are missing. Add a reproducible pipeline, data dictionary, tool versions, claim audit, and DOI-archived release before treating it as publication-ready.
