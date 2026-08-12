# Buffers

Each subdirectory contains one reusable `buffer.xml`. See the
[configuration overview](../README.md) for how specs combine buffers with
models and simulation parameters.

## Available buffers

| Buffer directory | Base category | Composition | Density (g/mL) | Viscosity (cP) | pH |
|---|---|---|---:|---:|---:|
| `tris-200mm-nacl` | `ra` | 50 mM Tris pH 7.5, 200 mM NaCl | 1.0079 | 1.03173 | 7.5 |
| `tris-edta-nacl` | `ri`, `ri_ip` | 10 mM Tris, 1 mM EDTA, 150 mM NaCl | 1.00463 | 1.01046 | 8.0 |
| `cscl` | `ip` | CsCl | 1.23866 | 2.63866 | 7.0 |
| `tris-50mm-nacl` | `fi` | 10 mM Tris, 50 mM NaCl | 1.00058 | 1.00536 | 7.0 |
| `water20` | `wi` | Water at 20C | 0.998234 | 1.00192 | 7.0 |
| `cacl2-tris-nacl` | `ri_mwl` | 20 mM CaCl2, 50 mM Tris, 150 mM NaCl | 1.00777 | 1.02879 | 8.51 |

Every file sets `manual="1"`: density, viscosity, and pH are stored as provided,
without temperature or density correction. `us_sim_inputs_gen --emit-buffer`
does not calculate or verify them from the description.

The water density and viscosity match published values at 20 °C [1]. The
Netrin-1 buffer composition and pH match the conditions reported for purified
Netrin-1ΔC [2]; its density and viscosity remain test parameters. The other
buffer properties are also test parameters unless a future reference documents
the complete composition, temperature, and measured values.

## References

1. Swindells, Coe, and Godfrey, “Absolute Viscosity of Water at 20 °C,”
   *Journal of Research of the National Bureau of Standards* 48 (1952),
   [NIST publication](https://nvlpubs.nist.gov/nistpubs/jres/048/jresv48n1p1_A1b.pdf).
2. Moya-Torres et al., “Homogenous overexpression of the extracellular matrix
   protein Netrin-1 in a hollow fiber bioreactor,” *Applied Microbiology and
   Biotechnology* (2021), [doi:10.1007/s00253-021-11438-0](https://doi.org/10.1007/s00253-021-11438-0).

## Add or update a buffer

Generate `<buffer-slug>/buffer.xml`. For example:

```bash
us_sim_inputs_gen --emit-buffer \
  --out config/buffers/tris-edta-nacl/buffer.xml \
  --density 1.00463 \
  --viscosity 1.01046 \
  --ph 8 \
  --description "10mM Tris, 1mM EDTA, 150mM NaCl"
```

Then update the table above and set the channel's `"buffer"` field in the
appropriate spec. Reusing an existing buffer requires only the spec change.

Buffer files are checked in, not generated at runtime.

The simulation tools live in
[ehb54/ultrascan3](https://github.com/ehb54/ultrascan3), not this repository.
See [Repository boundary](../../README.md#repository-boundary).
