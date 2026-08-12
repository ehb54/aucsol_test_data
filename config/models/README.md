# Models

Each subdirectory contains one reusable `model.xml` for simulation. Some inputs
match published values; the remaining values are documented test assumptions.
See the [configuration overview](../README.md) for how specs combine models with
buffers and simulation parameters.

These files are intentionally simpler than UltraScan database models. In
UltraScan, a model component links to a separate `US_Analyte` record through an
`analyteGUID`. Here, `us_sim_inputs_gen --emit-model` writes the required
properties directly into `model.xml`; there is no database record or
`analyteGUID`.

## Available models

Molecular weight (`mw`), partial specific volume (`vbar20`), and frictional
ratio (`f_f0`) are explicit simulator inputs. A reference applies only to the
values identified below; it does not validate the complete model.

`us_sim_inputs_gen` derives the sedimentation and diffusion coefficients (`s`
and `D`) from these values using UltraScan's
`US_Model::update_coefficients()` code path.

| Model directory | Base category | `mw` (Da) | `vbar20` (mL/g) | `f_f0` | Basis |
|---|---|---:|---:|---:|---|
| `netrin1` | `ra` | 49,535 | 0.7134 | 1.20 | Published Netrin-1ΔC mass; other values are test assumptions [1] |
| `dna-monomer-208bp` | `ri`, `ri_ip` | 128,396 | 0.55 | 1.80 | Published dsDNA approximation for `vbar20`; mass and `f_f0` are test assumptions [2] |
| `anellovirus` | `ip` | 4,700,000 | 0.70 | 1.30 | Anellovirus identity reference; numeric values are test assumptions [3] |
| `sma-nanodisk` | `fi` | 40,000 | 0.71 | 1.30 | Test assumptions |
| `small-molecule-placeholder` | `wi` | 500 | 0.70 | 1.05 | Arbitrary structural-test values |
| `dna-196bp-ms` | `ri_mwl` | 120,980 | 0.55 | 1.80 | Published dsDNA approximation for `vbar20`; mass and `f_f0` are test assumptions [2] |

The small-molecule fixture exists because `us_astfem_sim` requires a model
component. It is not a physical wavelength-calibration standard.

## References

1. Moya-Torres et al., “Homogenous overexpression of the extracellular matrix
   protein Netrin-1 in a hollow fiber bioreactor,” *Applied Microbiology and
   Biotechnology* (2021), [doi:10.1007/s00253-021-11438-0](https://doi.org/10.1007/s00253-021-11438-0).
   The paper reports 49.5 kDa for Netrin-1ΔC.
2. Ranasinghe et al., “Suitability of double-stranded DNA as a molecular
   standard for the validation of analytical ultracentrifugation instruments,”
   *European Biophysics Journal* (2023),
   [doi:10.1007/s00249-023-01671-y](https://doi.org/10.1007/s00249-023-01671-y).
   The study uses `0.55 mL/g` as the partial specific volume of dsDNA in water.
3. Kraberger et al., “ICTV Virus Taxonomy Profile: Anelloviridae 2026,”
   *Journal of General Virology* (2026),
   [ICTV report](https://ictv.global/report/chapter/anelloviridae/anelloviridae).
   It supports the virus classification, not this fixture's hydrodynamic values.

## Add or update a model

1. Generate `<model-slug>/model.xml`. For example:

   ```bash
   us_sim_inputs_gen --emit-model \
     --out config/models/dna-monomer-208bp/model.xml \
     --mw 128396 \
     --vbar20 0.55 \
     --f-f0 1.80 \
     --description "DNA fragment, Monomer (208 bp)"
   ```

2. Add or update its row in the table above.
3. Set the channel's `"model"` field in the appropriate spec file. To reuse an
   existing model, only this step is required.

Model files are checked in; they are not normally generated at runtime.

### Multi-wavelength exception

For `ri_mwl`, `generate_synthetic_data.py` reads
`dna-196bp-ms/model.xml`, then generates one temporary model per wavelength.
It supplies the run ID, channel, wavelength, and physical properties to
`us_sim_inputs_gen` so each description follows the naming convention required
by `us_mwl_species_sim`.

The simulation tools live in
[ehb54/ultrascan3](https://github.com/ehb54/ultrascan3), not this repository.
See [Repository boundary](../../README.md#repository-boundary).
