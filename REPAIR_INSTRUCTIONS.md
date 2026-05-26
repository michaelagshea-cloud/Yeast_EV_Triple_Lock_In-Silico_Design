# Final GitHub Repair Bundle

Replace these four files in the repository with the versions in this bundle:

- README.md
- 09_reproducible_pipeline/run_sequence_qc.py
- 09_reproducible_pipeline/tests/test_sequence_qc.py
- .github/workflows/reproducibility_qc.yml

Then run:

```bash
git fetch origin
git pull --rebase origin main

python 09_reproducible_pipeline/run_sequence_qc.py --repo-root .
python -m pytest -q 09_reproducible_pipeline/tests

git status --short
git add -A
git commit -m "Repair README and reproducibility QC files"
git push origin main
```

Expected local result:

```text
QC complete: 27 record(s). Status counts: {'PASS': 27}
6 passed
```

Do not delete folders 09, 10, or 11.
Do not force-push.
