# Synthetic Samples

> Generated 2026-08-18 13:11 UTC by `scripts/test-corpus/generate_synthetic_data.py`
> from LIMS generator commit `f1e9ce2 (uncommitted local changes)`.
> Do not edit by hand.

This is the smaller companion to the [standard synthetic dataset](../). It uses
the same chemistry but reduces each experiment by default to 6 scans
over 0 h 30 min. The `sample_defaults` in
the generator's `config/specs/base.json` and any experiment-level `samples` values control
these limits.

Use this tier for tests that do not need a full multi-scan run. See
[Generating synthetic data](../../../../README.md#generate-synthetic-data) for
the method and known limitations.

## Contents

| Experiment ID | Archive | Data type | Description |
|---|---|---|---|
| `netrin1-ra` | `ra/netrin1-ra_sample_synthetic.zip` | RA | Netrin1 (protein, globular) — 1A: RA; s ≈ 4.3 S |
| `dna-monomer-208bp-ri` | `ri/dna-monomer-208bp-ri_sample_synthetic.zip` | RI | DNA fragment, Monomer 208bp (extended) — 1A: RI; s ≈ 5.9 S |
| `anellovirus-ip` | `ip/anellovirus-ip_sample_synthetic.zip` | IP | Anellovirus (large protein/virus, compact) — 1A: IP; s ≈ 87.7 S |
| `sma-nanodisk-fi` | `fi/sma-nanodisk-fi_sample_synthetic.zip` | FI | SMA Nanodisk — 1A: FI; s ≈ 3.5 S |
| `small-molecule-placeholder-wi` | `wi/small-molecule-placeholder-wi_sample_synthetic.zip` | WI | Small-molecule calibration placeholder — 1A: WI; s ≈ 0.24 S |
| `bsa-monomer-dimer-ra` | `ra_monomer_dimer/bsa-monomer-dimer-ra_sample_synthetic.zip` | RA | BSA monomer/dimer mixture (two discrete species, 3:1 loading) — 1A: RA; s ≈ 4.6 + 6.5 S |
| `dna-196bp-ms-ri-mwl` | `ri_mwl/dna-196bp-ms-ri-mwl_sample_synthetic.zip` | RI | DNA fragment, 196bp MS — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `dna-monomer-208bp-ri-ip` | `ri_ip/dna-monomer-208bp-ri-ip_sample_synthetic.zip` | RI/IP | DNA fragment, Monomer 208bp, tagged both ways — 1A: RI + IP; s ≈ 5.9 S |
| `multicell-demo` | `demo/multicell_demo/multicell-demo_sample_synthetic.zip` | RA, RI, IP | Multi-cell x multi-channel demo: 2 cells, 2 channels each, one channel mwl, one channel noisier — 1A: RA; s ≈ 4.3 S; 1B: RA; s ≈ 4.3 S; 2A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.9 S; 2B: IP; s ≈ 5.9 S |

## Regenerate

The generator lives in the LIMS repo, not here. Run
from that repository's root:

```bash
python3 scripts/test-corpus/generate_synthetic_data.py \
  --us-bin-dir /path/to/ultrascan/bin --output-root /path/to/test-data --samples
```
