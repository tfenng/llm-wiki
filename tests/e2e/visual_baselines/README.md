# Visual-regression baselines

This directory holds `baselines.json` — a committed manifest of
SHA-256 hashes for every screenshot the E2E suite captures. See
[`docs/testing/visual-regression.md`](../../../docs/testing/visual-regression.md)
for the workflow.

**Don't hand-edit the JSON.** Use
`scripts/update-visual-baselines.sh` to regenerate it after you've
reviewed the drifted screenshots.
