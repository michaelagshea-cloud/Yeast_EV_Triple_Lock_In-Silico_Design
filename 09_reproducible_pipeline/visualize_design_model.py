#!/usr/bin/env python3
"""Generate simple visual models for the repository workflow and donor architecture.

Outputs are Mermaid diagrams that render directly on GitHub in Markdown files.
No biological validation is implied by these diagrams.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

WORKFLOW_MERMAID = """flowchart TD
    A[Reference sources\nNCBI/SGD/Benchling exports] --> B[Reference-gene provenance\n01_reference_gene_provenance]
    B --> C[ISC1 payload design\n02_isc1_payload_design]
    C --> D[Payload validation\n03_isc1_payload_validation]
    B --> E[Locus coordinate design\n04_locus_coordinate_design]
    C --> F[Full donor cassette assembly\n05_full_donor_cassette_assembly]
    E --> F
    F --> G[Annotated construct records/maps\n06_annotated_construct_records_and_maps]
    F --> H[Sequence QC reports\n07_sequence_qc_and_validation_reports]
    H --> I[BY4741/locus compatibility addendum\n08_genome_assembly_confidence]
    H --> J[Publication readiness\n11_publication_readiness]
    K[Reproducible scripts\n09_reproducible_pipeline] --> H
    K --> L[Machine-readable manifest\n00_metadata]
"""

DONOR_MERMAID = """flowchart LR
    A[500 bp 5-prime homology arm\nretains native N-terminal anchor] --> B[30 bp linker\nGGGGS x2]
    B --> C[1269 bp ISC1/YER019W payload block\naa56-477 + TAA]
    C --> D[500 bp 3-prime homology arm]
    D --> E[2299 bp full HDR donor candidate]
"""

ARCHITECTURE_MARKDOWN = """# Visual design models

These diagrams are computational documentation only. They summarize the repository workflow and donor architecture, but they do not demonstrate yeast transformation, integration, expression, extracellular-vesicle phenotype, peptide loading, BBB delivery, or therapeutic function.

## Repository workflow model

```mermaid
{workflow}
```

## Donor architecture model

```mermaid
{donor}
```
"""


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Write Mermaid visual models for GitHub rendering.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--output", default="10_methods_and_provenance/visual_design_models.md", help="Output Markdown path relative to repo root.")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(ARCHITECTURE_MARKDOWN.format(workflow=WORKFLOW_MERMAID.strip(), donor=DONOR_MERMAID.strip()), encoding="utf-8")
    print(f"Wrote: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
