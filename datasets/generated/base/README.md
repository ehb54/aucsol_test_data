# Synthetic Data

> Generated 2026-08-27 13:13 UTC by the [LIMS synthetic-data generator](https://github.com/ehb54/uslims_stack/blob/1e1d44a/scripts/test-corpus/generate_synthetic_data.py)
> from `uslims_stack` commit `1e1d44a` with uncommitted generator/input changes.
> Do not edit by hand.

UltraScan's finite-element simulators compute these datasets from the
generator's checked-in models, buffers, and simulation parameters. This
standard tier keeps each experiment's configured scan count and duration.

See [About the generated data](../../../README.md#about-the-generated-data) for
the generation method, inputs, and known limitations.

The generator's `config/specs/base.json` defines this dataset. Its `dataset_name` selects
the directory under `datasets/generated/`; each experiment's `id` names its
archive and its `dir` selects the archive's subdirectory. Other specs generate
separate sibling datasets.

## Contents

| Experiment ID | Archive | Data type | Description |
|---|---|---|---|
| `netrin1-ra` | `ra/netrin1-ra_synthetic.zip` | RA | Netrin1 (protein, globular) — 1A: RA; s ≈ 4.3 S |
| `dna-monomer-208bp-ri` | `ri/dna-monomer-208bp-ri_synthetic.zip` | RI | DNA fragment, Monomer 208bp (extended) — 1A: RI; s ≈ 5.9 S |
| `anellovirus-ip` | `ip/anellovirus-ip_synthetic.zip` | IP | Anellovirus (large protein/virus, compact) — 1A: IP; s ≈ 87.7 S |
| `sma-nanodisk-fi` | `fi/sma-nanodisk-fi_synthetic.zip` | FI | SMA Nanodisk — 1A: FI; s ≈ 3.5 S |
| `small-molecule-placeholder-wi` | `wi/small-molecule-placeholder-wi_synthetic.zip` | WI | Small-molecule calibration placeholder — 1A: WI; s ≈ 0.24 S |
| `bsa-monomer-dimer-ra` | `ra_monomer_dimer/bsa-monomer-dimer-ra_synthetic.zip` | RA | BSA monomer/dimer mixture (two discrete species, 3:1 loading) — 1A: RA; s ≈ 4.6 + 6.5 S |
| `dna-196bp-ms-ri-mwl` | `ri_mwl/dna-196bp-ms-ri-mwl_synthetic.zip` | RI | DNA fragment, 196bp MS — 1A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.8 S |
| `dna-monomer-208bp-ri-ip` | `ri_ip/dna-monomer-208bp-ri-ip_synthetic.zip` | RI/IP | DNA fragment, Monomer 208bp, tagged both ways — 1A: RI + IP; s ≈ 5.9 S |
| `multicell-demo` | `demo/multicell_demo/multicell-demo_synthetic.zip` | RA, RI, IP | Multi-cell x multi-channel demo: 2 cells, 2 channels each, one channel mwl, one channel noisier — 1A: RA; s ≈ 4.3 S; 1B: RA; s ≈ 4.3 S; 2A: RI; 3 wavelengths (250/280/310 nm); s ≈ 5.9 S; 2B: IP; s ≈ 5.9 S |

## Regenerate

The generator lives in the LIMS repo, not here. Run
from that repository's root:

```bash
python3 scripts/test-corpus/generate_synthetic_data.py \
  --us-bin-dir /path/to/ultrascan/bin --output-root /path/to/test-data
```
