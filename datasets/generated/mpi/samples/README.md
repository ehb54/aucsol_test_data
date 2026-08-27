# Synthetic Samples

> Generated 2026-08-27 13:13 UTC by `scripts/test-corpus/generate_synthetic_data.py`
> from LIMS generator commit `1e1d44a (uncommitted local changes)`.
> Do not edit by hand.

This is the smaller companion to the [standard synthetic dataset](../). It uses
the same chemistry but reduces each experiment by default to 6 scans
over 0 h 30 min. The `sample_defaults` in
the generator's `config/specs/mpi.json` and any experiment-level `samples` values control
these limits.

Use this tier for tests that do not need a full multi-scan run. See
[Generating synthetic data](../../../../README.md#generate-synthetic-data) for
the method and known limitations.

## Contents

| Experiment ID | Archive | Data type | Description |
|---|---|---|---|
| `canonical-4solute` | `canonical/canonical-4solute_sample_synthetic.zip` | RA | Canonical 4-solute discrete distribution, RA with TI+RI noise (T1-01 shape, reference.json solute_count) — 1A: RA; s ≈ 2.5 + 5.0 + 9.0 + 14.0 S |
| `tb01-grid-node` | `boundary/tb01_grid_node/tb01-grid-node_sample_synthetic.zip` | RA | Single solute exactly on a grid node, s=5S k=1.5 (TB-01) — 1A: RA; s ≈ 5.0 S |
| `tb02-near-degenerate` | `boundary/tb02_near_degenerate/tb02-near-degenerate_sample_synthetic.zip` | RA | Two solutes 0.05S apart at equal loading (TB-02) — 1A: RA; s ≈ 5.0 + 5.0 S |
| `tb03-grid-edges` | `boundary/tb03_grid_edges/tb03-grid-edges_sample_synthetic.zip` | RA | Solutes at s_min=1S and s_max=20S, nothing between (TB-03) — 1A: RA; s ≈ 1.0 + 20.0 S |
| `tb04a-od-low` | `boundary/tb04a_od_low/tb04a-od-low_sample_synthetic.zip` | RA | Grid-node solute loaded to peak OD 1.40, the low end of the 1.4-1.6 band (TB-04a) — 1A: RA; s ≈ 5.0 S |
| `tb04b-od-high` | `boundary/tb04b_od_high/tb04b-od-high_sample_synthetic.zip` | RA | Grid-node solute loaded to peak OD 1.60, the high end of the 1.4-1.6 band (TB-04b) — 1A: RA; s ≈ 5.0 S |
| `tb05-od-trace` | `boundary/tb05_od_trace/tb05-od-trace_sample_synthetic.zip` | RA | Grid-node solute at trace loading, signal 0.02 (TB-05) — 1A: RA; s ≈ 5.0 S |
| `tb06-wide-range` | `boundary/tb06_wide_range/tb06-wide-range_sample_synthetic.zip` | RA | Eight solutes spanning the full s and k box, for depth promotion (TB-06) — 1A: RA; s ≈ 1.0 + 3.0 + 5.5 + 8.0 + 11.0 + 14.0 + 17.0 + 20.0 S |
| `tb08-out-of-bucket` | `boundary/tb08_out_of_bucket/tb08-out-of-bucket_sample_synthetic.zip` | RA | Solute at s=15S k=2.0, outside GA buckets covering s=1-10S (TB-08) — 1A: RA; s ≈ 15.0 S |
| `tb11-uniform` | `boundary/tb11_uniform/tb11-uniform_sample_synthetic.zip` | RA | Four near-uniform solutes, for mrecs sort stability (TB-11) — 1A: RA; s ≈ 5.0 + 5.0 + 5.0 + 5.0 S |
| `t2-2dsa-ms` | `variants/multispeed/t2-2dsa-ms_sample_synthetic.zip` | RA | Two speed steps, 40,000 then 50,000 rpm, one RA channel, persisted as the two runs t2-2dsa-ms-40000 and t2-2dsa-ms-50000 (T2-2DSA-MS, T2-GA-MS, T2-PCSA-MS) — 1A: RA; s ≈ 2.5 + 5.0 + 9.0 + 14.0 S |
| `t2-2dsa-cg` | `variants/custom_grid/t2-2dsa-cg_sample_synthetic.zip` | RA | Data axis for the custom-grid cells; the CG_model itself is a config-axis artifact (T2-2DSA-CG and its -IT/-MC variants) — 1A: RA; s ≈ 2.5 + 5.0 + 9.0 + 14.0 S |
| `t2-dmga-reacting` | `variants/dmga_reacting/t2-dmga-reacting_sample_synthetic.zip` | RA | Reversible BSA monomer-dimer at K_d=1e-6 M, the production DMGA data shape — 1A: RA; s ≈ 4.7 + 7.5 S; 2A: RA; s ≈ 4.7 + 7.5 S |

## Regenerate

The generator lives in the LIMS repo, not here. Run
from that repository's root:

```bash
python3 scripts/test-corpus/generate_synthetic_data.py \
  --us-bin-dir /path/to/ultrascan/bin --output-root /path/to/test-data --samples --spec mpi
```
