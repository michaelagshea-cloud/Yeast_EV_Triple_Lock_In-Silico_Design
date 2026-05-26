# Source database accessions and provenance register

This file is the working provenance register for sequence sources and literature sources. It should be updated every time a sequence is downloaded, edited, exported from Benchling, or rebuilt by code.

## Primary genome/reference sources

| Source type | Database/source | Accession or identifier | Current use in repository | Verification status | URL |
|---|---|---|---|---|---|
| Reference genome assembly | NCBI RefSeq / SGD | GCF_000146045.2 / R64 / sacCer3 | S. cerevisiae S288C reference coordinate background | Verified source to cite; exact local downloaded file still needs checksum record | https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000146045.2/ |
| Reference strain page | Saccharomyces Genome Database | S288C | Reference strain context and genome sequence metadata | Verified source to cite | https://www.yeastgenome.org/strain/s288c |
| Payload gene | SGD | ISC1 / YER019W / S000000821 | Payload source gene; aa56-477 payload region | Gene identity verified; exact sequence extraction route needs local record | https://yeastgenome.org/locus/S000000821 |
| Target gene | SGD | OCH1 / YGL038C / S000003006 | OCH1 donor target | Gene identity verified; exact coordinate/sequence extraction route needs local record | https://yeastgenome.org/locus/S000003006 |
| Target gene | SGD | MNN2 / YBR015C / S000000219 | MNN2 donor target | Gene identity verified; exact coordinate/sequence extraction route needs local record | https://yeastgenome.org/locus/S000000219 |
| Target gene | SGD | MNN5 / YJL186W / S000003722 | MNN5 donor target | Gene identity verified; exact coordinate/sequence extraction route needs local record | https://yeastgenome.org/locus/S000003722 |

## Core biological literature sources to verify/cite

| Topic | Citation candidate | Why it matters | DOI/identifier | Status |
|---|---|---|---|---|
| ISC1 function | Sawai et al., 2000, Journal of Biological Chemistry | Identifies ISC1/YER019W as inositol phosphosphingolipid phospholipase C in S. cerevisiae | 10.1074/jbc.M007721200 | Verified citation candidate |
| MNN2/MNN5 function | Rayner & Munro, 1998, Journal of Biological Chemistry | Identifies MNN2 and MNN5 mannosyltransferases required for outer-chain mannan branching | 10.1074/jbc.273.41.26836 | Verified citation candidate |
| OCH1 function | Nakayama et al., 1997, FEBS Letters | OCH1 encodes the mannosyltransferase initiating N-linked outer-chain elongation | PubMed 9276464 | Verify full DOI/details before final manuscript |
| Yeast genome database | Engel et al., 2024/2025 SGD update papers | Supports SGD as authoritative yeast genome/annotation source | Add DOI after final citation check | Needs final citation formatting |

## Exact source-file provenance still needed

Before presenting this repository as publication-ready, fill in the exact source for every generated sequence:

| Derived file | Source file(s) used | Database accession(s) | Download date | Export tool | Exact command or manual step | SHA-256 of source | Verified by |
|---|---|---|---|---|---|---|---|
| OCH1_ISC1alpha full donor | TODO | TODO | TODO | TODO | TODO | TODO | TODO |
| MNN2_ISC1beta full donor | TODO | TODO | TODO | TODO | TODO | TODO | TODO |
| MNN5_ISC1gamma full donor | TODO | TODO | TODO | TODO | TODO | TODO | TODO |
| ISC1alpha payload | TODO | TODO | TODO | TODO | TODO | TODO | TODO |
| ISC1beta payload | TODO | TODO | TODO | TODO | TODO | TODO | TODO |
| ISC1gamma payload | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## Rule for future edits

Do not replace a sequence file without also updating:

1. `00_metadata/rebuilt_file_manifest.csv`
2. `00_metadata/sequence_inventory.csv`
3. `07_sequence_qc_and_validation_reports/sequence_qc_results.csv`
4. this provenance file
5. `10_methods_and_provenance/command_log.txt`
