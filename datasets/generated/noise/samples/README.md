# Synthetic Samples

> Generated 2026-08-17 20:59 UTC by `scripts/test-corpus/generate_synthetic_data.py`
> from LIMS generator commit `509958f (uncommitted local changes)`.
> Do not edit by hand.

This is the smaller companion to the [standard synthetic dataset](../). It uses
the same chemistry but reduces each experiment by default to 6 scans
over 0 h 30 min. The `sample_defaults` in
the generator's `config/specs/noise.json` and any experiment-level `samples` values control
these limits.

Use this tier for tests that do not need a full multi-scan run. See
[Generating synthetic data](../../../../README.md#generate-synthetic-data) for
the method and known limitations.

## Contents

| Experiment ID | Archive | Data type | Description |
|---|---|---|---|
| `t2-2dsa-ra-nn` | `ra/no_systematic/t2-2dsa-ra-nn_sample_synthetic.zip` | RA | Netrin1, random noise only (T2-2DSA-RA-nn) — 1A: RA; s ≈ 4.3 S |
| `t2-2dsa-ra-ti` | `ra/ti/t2-2dsa-ra-ti_sample_synthetic.zip` | RA | Netrin1, time-invariant noise (T2-2DSA-RA-ti) — 1A: RA; s ≈ 4.3 S |
| `t2-2dsa-ra-ri` | `ra/ri/t2-2dsa-ra-ri_sample_synthetic.zip` | RA | Netrin1, radially-invariant noise (T2-2DSA-RA-ri) — 1A: RA; s ≈ 4.3 S |
| `t1-01-ra-tiri` | `ra/ti_ri/t1-01-ra-tiri_sample_synthetic.zip` | RA | Netrin1, TI+RI noise -- canonical 2DSA (T1-01) — 1A: RA; s ≈ 4.3 S |
| `t2-2dsa-ip-nn` | `ip/no_systematic/t2-2dsa-ip-nn_sample_synthetic.zip` | IP | Anellovirus, random noise only (T2-2DSA-IP-nn) — 1A: IP; s ≈ 87.7 S |
| `t2-2dsa-ip-ti` | `ip/ti/t2-2dsa-ip-ti_sample_synthetic.zip` | IP | Anellovirus, time-invariant noise (T2-2DSA-IP-ti) — 1A: IP; s ≈ 87.7 S |
| `t2-2dsa-ip-ri` | `ip/ri/t2-2dsa-ip-ri_sample_synthetic.zip` | IP | Anellovirus, radially-invariant noise (T2-2DSA-IP-ri) — 1A: IP; s ≈ 87.7 S |
| `t1-02-ip-tiri` | `ip/ti_ri/t1-02-ip-tiri_sample_synthetic.zip` | IP | Anellovirus, TI+RI noise -- interference, no ODlimit branch (T1-02) — 1A: IP; s ≈ 87.7 S |
| `t2-2dsa-ri-nn` | `ri/no_systematic/t2-2dsa-ri-nn_sample_synthetic.zip` | RI | DNA Monomer 208bp, random noise only (T2-2DSA-RI-nn) — 1A: RI; s ≈ 5.9 S |
| `t2-2dsa-ri-ti` | `ri/ti/t2-2dsa-ri-ti_sample_synthetic.zip` | RI | DNA Monomer 208bp, time-invariant noise (T2-2DSA-RI-ti) — 1A: RI; s ≈ 5.9 S |
| `t2-2dsa-ri-ri` | `ri/ri/t2-2dsa-ri-ri_sample_synthetic.zip` | RI | DNA Monomer 208bp, radially-invariant noise (T2-2DSA-RI-ri) — 1A: RI; s ≈ 5.9 S |
| `t1-03-ri-tiri` | `ri/ti_ri/t1-03-ri-tiri_sample_synthetic.zip` | RI | DNA Monomer 208bp, TI+RI noise -- ODlimit branch active (T1-03) — 1A: RI; s ≈ 5.9 S |
| `t2-2dsa-fi-nn` | `fi/no_systematic/t2-2dsa-fi-nn_sample_synthetic.zip` | FI | SMA Nanodisk, random noise only (T2-2DSA-FI-nn) — 1A: FI; s ≈ 3.5 S |
| `t1-04-fi-ti` | `fi/ti/t1-04-fi-ti_sample_synthetic.zip` | FI | SMA Nanodisk, time-invariant noise -- fluorescence, no ODlimit (T1-04, T2-2DSA-FI-ti) — 1A: FI; s ≈ 3.5 S |
| `t2-2dsa-fi-ri` | `fi/ri/t2-2dsa-fi-ri_sample_synthetic.zip` | FI | SMA Nanodisk, radially-invariant noise (T2-2DSA-FI-ri) — 1A: FI; s ≈ 3.5 S |
| `t2-2dsa-fi-tiri` | `fi/ti_ri/t2-2dsa-fi-tiri_sample_synthetic.zip` | FI | SMA Nanodisk, TI+RI noise (T2-2DSA-FI-tiri) — 1A: FI; s ≈ 3.5 S |
| `t2-2dsa-mwl-nn` | `mwl/no_systematic/t2-2dsa-mwl-nn_sample_synthetic.zip` | RI | DNA 196bp MS at 3 wavelengths, random noise only (T2-2DSA-MWL-nn) — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `t2-2dsa-mwl-ti` | `mwl/ti/t2-2dsa-mwl-ti_sample_synthetic.zip` | RI | DNA 196bp MS at 3 wavelengths, time-invariant noise (T2-2DSA-MWL-ti) — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `t2-2dsa-mwl-ri` | `mwl/ri/t2-2dsa-mwl-ri_sample_synthetic.zip` | RI | DNA 196bp MS at 3 wavelengths, radially-invariant noise (T2-2DSA-MWL-ri) — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `t1-05-mwl-tiri` | `mwl/ti_ri/t1-05-mwl-tiri_sample_synthetic.zip` | RI | DNA 196bp MS at 3 wavelengths, TI+RI noise -- multi-wavelength global fit (T1-05) — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `t1-07-ra-global-fit` | `ra/global_fit/t1-07-ra-global-fit_sample_synthetic.zip` | RA | Netrin1, two RA channels of one cell for a global fit (T1-07, T2-*-GFIT) — 1A: RA; s ≈ 4.3 S; 1B: RA; s ≈ 4.3 S |

## Regenerate

The generator lives in the LIMS repo, not here. Run
from that repository's root:

```bash
python3 scripts/test-corpus/generate_synthetic_data.py \
  --us-bin-dir /path/to/ultrascan/bin --output-root /path/to/test-data --samples --spec noise
```
