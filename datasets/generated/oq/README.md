# Synthetic Data

> Generated 2026-11-04 14:59 UTC by the [LIMS synthetic-data generator](https://github.com/ehb54/uslims_stack/blob/945d18d/scripts/test-corpus/generate_synthetic_data.py)
> from `uslims_stack` commit `945d18d`.
> Do not edit by hand.

UltraScan's finite-element simulators compute these datasets from the
generator's checked-in models, buffers, and simulation parameters. This
standard tier keeps each experiment's configured scan count and duration.

See [Generating synthetic data](../../../README.md#generate-synthetic-data) for
the generation method, inputs, and known limitations.

The generator's `config/specs/oq.json` defines this dataset. Its `dataset_name` selects
the directory under `datasets/generated/`; each experiment's `id` names its
archive and its `dir` selects the archive's subdirectory. Other specs generate
separate sibling datasets.

## Contents

| Experiment ID | Archive | Data type | Description |
|---|---|---|---|
| `oq-dna-196bp` | `ri/oq-dna-196bp_synthetic.zip` | RI | DNA fragment, 196 bp MS, for the OQ GMP cycle — 1A: RI; 1 wavelengths (280 nm); s ≈ 5.8 S; 1B: RI; 1 wavelengths (280 nm); s ≈ 5.8 S; 5A: RI; 1 wavelengths (280 nm); s ≈ 5.8 S; 5B: RI; 1 wavelengths (280 nm); s ≈ 5.8 S |

## Regenerate

The generator lives in the LIMS repo, not here. Run
from that repository's root:

```bash
python3 scripts/test-corpus/generate_synthetic_data.py \
  --us-bin-dir /path/to/ultrascan/bin --output-root /path/to/test-data --spec oq
```
