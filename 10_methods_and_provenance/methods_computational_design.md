# Methods: computational donor-candidate design and reproducibility audit

## Scope

This repository is a computational design package for three Saccharomyces cerevisiae / BY4741-compatible HDR donor candidates targeting OCH1/YGL038C, MNN2/YBR015C, and MNN5/YJL186W. The current package documents donor architecture, sequence provenance, locus coordinate logic, annotated construct records, and sequence-level QC.

This package does **not** demonstrate yeast transformation, genomic integration, ISC1 expression, lipid remodeling, extracellular-vesicle phenotype, immune evasion, peptide loading, blood-brain-barrier delivery, or therapeutic function.

## Reference background

The design uses the Saccharomyces cerevisiae S288C reference genome context, with BY4741 treated as a laboratory strain background requiring explicit locus-level compatibility checks. The current reference-genome anchor should be recorded as R64 / GCF_000146045.2 unless a later verified reference is intentionally substituted.

## Target loci

The three design targets are:

| Target | Systematic ID | Intended design role | Current evidence type |
|---|---:|---|---|
| OCH1 | YGL038C | N-glycan outer-chain initiation locus; donor target | Computational sequence design |
| MNN2 | YBR015C | Mannan branch extension locus; donor target | Computational sequence design |
| MNN5 | YJL186W | Mannan branch extension locus; donor target | Computational sequence design |

## Payload

The payload is derived from ISC1/YER019W. The repository README currently defines the canonical payload block as 1269 bp, composed of 1266 bp coding sequence corresponding to ISC1/YER019W amino acids 56-477 plus a 3 bp TAA stop codon.

## Canonical donor architecture

Each full donor candidate should be represented as:

```text
500 bp 5-prime homology arm
+ 30 bp (GGGGS)2 linker
+ 1269 bp ISC1/YER019W payload block including TAA
+ 500 bp 3-prime homology arm
= 2299 bp full donor candidate
```

## Reproducibility approach

The repository should support three levels of reproducibility:

1. **Inventory reproducibility:** every file can be listed with a stable path, size, SHA-256 hash, and inferred role.
2. **Sequence QC reproducibility:** every FASTA/plain DNA sequence can be parsed, checked for valid nucleotide alphabet, summarized by length and GC fraction, and compared against expected design constraints where applicable.
3. **Sequence-build reproducibility:** each derived donor sequence can be regenerated from explicitly listed component files using a reviewed `sequence_build_plan.csv`.

## Recommended command sequence

From the repository root:

```bash
python 09_reproducible_pipeline/rebuild_manifest.py --repo-root .
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode audit
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode write-template
python 09_reproducible_pipeline/run_sequence_qc.py --repo-root .
python 09_reproducible_pipeline/visualize_design_model.py --repo-root .
pytest -q 09_reproducible_pipeline/tests
```

After manually verifying the component paths in `10_methods_and_provenance/sequence_build_plan.csv`, run:

```bash
python 09_reproducible_pipeline/generate_all_sequences.py --repo-root . --mode build
python 09_reproducible_pipeline/run_sequence_qc.py --repo-root . --strict
```

## Evidence boundaries

Use conservative language in all reports and manuscript drafts:

- Acceptable: "computational donor-candidate design"
- Acceptable: "in-silico sequence-level QC"
- Acceptable: "locus-level compatibility audit"
- Not acceptable without wet-lab data: "validated engineered yeast strain"
- Not acceptable without wet-lab data: "confirmed ISC1 expression"
- Not acceptable without wet-lab data: "altered EV phenotype"
- Not acceptable without wet-lab data: "therapeutic delivery platform"

## Future validation needed before biological claims

The next experimental layer would need, at minimum:

1. transformation and clone screening records;
2. PCR/Sanger or long-read confirmation of integration junctions;
3. transcript/protein evidence for payload expression;
4. lipidomic or sphingolipid evidence for altered lipid remodeling;
5. EV isolation quality controls;
6. NTA/TEM/protein quantification controls;
7. peptide-loading quantification, if peptide loading is claimed;
8. cell uptake/safety assays, if delivery is claimed.
