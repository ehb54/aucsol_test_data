# Synthetic Data

> Generated 2026-08-27 13:13 UTC by the [LIMS synthetic-data generator](https://github.com/ehb54/uslims_stack/blob/1e1d44a/scripts/test-corpus/generate_synthetic_data.py)
> from `uslims_stack` commit `1e1d44a` with uncommitted generator/input changes.
> Do not edit by hand.

UltraScan's finite-element simulators compute these datasets from the
generator's checked-in models, buffers, and simulation parameters. This
standard tier keeps each experiment's configured scan count and duration.

See [Generating synthetic data](../../../README.md#generate-synthetic-data) for
the generation method, inputs, and known limitations.

The generator's `config/specs/examples.json` defines this dataset. Its `dataset_name` selects
the directory under `datasets/generated/`; each experiment's `id` names its
archive and its `dir` selects the archive's subdirectory. Other specs generate
separate sibling datasets.

## Contents

| Experiment ID | Archive | Data type | Description |
|---|---|---|---|
| `example-single-cell` | `single-cell/example-single-cell_synthetic.zip` | RA | Single channel, no centerpiece override — 1A: RA; s ≈ 4.3 S |
| `example-reference-channel` | `reference-channel/example-reference-channel_synthetic.zip` | RI | Paired channels in one cell; channel B adds noise and baseline — 1A: RI; s ≈ 5.9 S; 1B: RI; s ≈ 5.9 S |
| `example-multi-wavelength` | `multi-wavelength/example-multi-wavelength_synthetic.zip` | RI | DNA fragment scanned at 3 wavelengths — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `example-dual-tag` | `dual-tag/example-dual-tag_synthetic.zip` | RI/IP | One physical channel, tagged both RI and IP — 1A: RI + IP; s ≈ 5.9 S |
| `example-reduced-run-override` | `reduced-run-override/example-reduced-run-override_synthetic.zip` | RA | Per-experiment scan and duration limits for --samples — 1A: RA; s ≈ 4.3 S |
| `example-multicell` | `multicell/example-multicell_synthetic.zip` | RA, RI, IP | Multi-cell x multi-channel: 2 cells, 2 channels each, one channel mwl, one channel noisier — 1A: RA; s ≈ 4.3 S; 1B: RA; s ≈ 4.3 S; 2A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.9 S; 2B: IP; s ≈ 5.9 S |

## Regenerate

The generator lives in the LIMS repo, not here. Run
from that repository's root:

```bash
python3 scripts/test-corpus/generate_synthetic_data.py \
  --us-bin-dir /path/to/ultrascan/bin --output-root /path/to/test-data --spec examples
```
