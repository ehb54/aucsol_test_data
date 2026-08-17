# Synthetic Samples

> Generated 2026-08-17 20:59 UTC by `scripts/test-corpus/generate_synthetic_data.py`
> from LIMS generator commit `509958f (uncommitted local changes)`.
> Do not edit by hand.

This is the smaller companion to the [standard synthetic dataset](../). It uses
the same chemistry but reduces each experiment by default to 4 scans
over 0 h 20 min. The `sample_defaults` in
the generator's `config/specs/examples.json` and any experiment-level `samples` values control
these limits.

Use this tier for tests that do not need a full multi-scan run. See
[Generating synthetic data](../../../../README.md#generate-synthetic-data) for
the method and known limitations.

## Contents

| Experiment ID | Archive | Data type | Description |
|---|---|---|---|
| `example-single-cell` | `single-cell/example-single-cell_sample_synthetic.zip` | RA | Single channel, no centerpiece override — 1A: RA; s ≈ 4.3 S |
| `example-reference-channel` | `reference-channel/example-reference-channel_sample_synthetic.zip` | RI | Paired channels in one cell; channel B adds noise and baseline — 1A: RI; s ≈ 5.9 S; 1B: RI; s ≈ 5.9 S |
| `example-multi-wavelength` | `multi-wavelength/example-multi-wavelength_sample_synthetic.zip` | RI | DNA fragment scanned at 3 wavelengths — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `example-dual-tag` | `dual-tag/example-dual-tag_sample_synthetic.zip` | RI/IP | One physical channel, tagged both RI and IP — 1A: RI + IP; s ≈ 5.9 S |
| `example-reduced-run-override` | `reduced-run-override/example-reduced-run-override_sample_synthetic.zip` | RA | Per-experiment scan and duration limits for --samples — 1A: RA; s ≈ 4.3 S |
| `example-multicell` | `multicell/example-multicell_sample_synthetic.zip` | RA, RI, IP | Multi-cell x multi-channel: 2 cells, 2 channels each, one channel mwl, one channel noisier — 1A: RA; s ≈ 4.3 S; 1B: RA; s ≈ 4.3 S; 2A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.9 S; 2B: IP; s ≈ 5.9 S |

## Regenerate

The generator lives in the LIMS repo, not here. Run
from that repository's root:

```bash
python3 scripts/test-corpus/generate_synthetic_data.py \
  --us-bin-dir /path/to/ultrascan/bin --output-root /path/to/test-data --samples --spec examples
```
