# UltraScan Test Data

Public `.auc` datasets for UltraScan system testing. The repository contains
synthetic simulator output and curated reference data; it does not contain
customer, patient, or proprietary third-party data.

## Choose a dataset

| Dataset | Use case |
|---|---|
| [`datasets/generated/base/`](datasets/generated/base/) | Standard synthetic runs using the checked-in simulation parameters |
| [`datasets/generated/base/samples/`](datasets/generated/base/samples/) | Smaller synthetic runs for tests that do not need full datasets |
| [`datasets/manual/`](datasets/manual/) | Curated reference datasets added by hand |

The generated base dataset covers seven core categories (`ra`, `ri`, `ip`,
`fi`, `wi`, `ri_mwl`, and `ri_ip`) plus a multi-cell, multi-channel example.
Each dataset is distributed as a zip and listed in a GNU-format
`checksums.sha256` file.

## Get and verify the data

```bash
git clone git@github.com:ehb54/aucsol_test_data.git
cd aucsol_test_data
```

Verify a generated tier from its root directory:

```bash
cd datasets/generated/base
sha256sum -c checksums.sha256
```

On macOS, `shasum` is also available:

```bash
shasum -a 256 -c checksums.sha256
```

On Windows PowerShell:

```powershell
cd datasets\generated\base
Get-Content checksums.sha256 | ForEach-Object {
    $hash, $file = $_ -split '  '
    $actual = (Get-FileHash $file -Algorithm SHA256).Hash.ToLower()
    if ($actual -eq $hash) { "OK: $file" } else { "FAILED: $file" }
}
```

A mismatch means the file is corrupt or has changed. The checksum file uses
two spaces between each hash and filename:

```text
98d30b93ece674d0dd37ef103dccdfd3445862152bd89188f285f0dd2a70b8ab  ri/dna-monomer-208bp-ri_synthetic.zip
```

Record the repository tag, dataset path, and checksum result with each test
execution. For example:

```text
Dataset: datasets/generated/base/ri/dna-monomer-208bp-ri_synthetic.zip
Repository tag: 1.0.0
Checksum verified: PASS
```

Pin reproducible workflows to a repository tag rather than a moving branch.
The root `VERSION` file records the current version between tags, and the
manually triggered [Bump Version workflow](.github/workflows/bump-version.yml)
prepares version updates.

## Generate synthetic data

The generator runs UltraScan's finite-element simulators headlessly and creates
one zip per experiment. Generated output has a stable directory and naming
structure, but separate runs are not guaranteed to be byte-identical.

[`base.json`](config/specs/base.json) is the default dataset spec.
[`examples.json`](config/specs/examples.json) contains worked examples of the
schema. Any compatible spec can be selected with `--spec`; its `dataset_name`
sets the output directory under `datasets/generated/`.

### Requirements

Use the `bin/` directory from an
[UltraScan Desktop](https://github.com/ehb54/ultrascan3) installation or build.
The directory must contain these executables:

- `us_sim_inputs_gen`
- `us_astfem_sim`
- `us_mwl_species_sim`

The adjacent UltraScan `etc/` directory must also contain the rotor and
centerpiece definitions used by the simulations. This repository does not
vendor those binaries or reference files.

### Commands

Run commands from the repository root:

```bash
# Generate the standard base dataset.
python3 scripts/generate_synthetic_data.py --us-bin-dir /path/to/ultrascan/bin

# Generate the smaller samples tier.
python3 scripts/generate_synthetic_data.py --us-bin-dir /path/to/ultrascan/bin --samples

# Validate configuration without generating data.
python3 scripts/generate_synthetic_data.py --validate

# Use another spec, such as the worked examples.
python3 scripts/generate_synthetic_data.py --spec examples --us-bin-dir /path/to/ultrascan/bin
```

Set `US_BIN_DIR` instead of passing `--us-bin-dir` each time. Supplying the
binary path with `--validate` also enables rotor and centerpiece checks.

The generator is run manually. Review and commit its output; data is not
created automatically at container startup or in CI.

### Inputs and outputs

Start with the [configuration overview](config/README.md). It explains how a
spec assembles experiments from independently reusable models, buffers, and
simulation parameters, including multi-channel geometry and output mapping.

Without `--samples`, each experiment keeps the configured scan count and
duration. With `--samples`, the generator reduces both according to
`sample_defaults` and any per-experiment override in the active spec. It rejects
zero values and values larger than the original simulation.

Each run also updates the tier's `checksums.sha256` and generated `README.md`.
Change an experiment's `description` in the spec to update its summary entry.

### Data-type relabeling

The UltraScan simulators write `RA`-tagged `.auc` files. For other test
categories, the generator changes the two-byte type at offset 6 and recomputes
the trailing little-endian CRC-32.

UltraScan's first CRC call produces an effective initial register of `0`. The
equivalent Python calculation is:

```python
import zlib

crc = zlib.crc32(file_bytes[:-4], 0xFFFFFFFF) & 0xFFFFFFFF
```

### Validation and limitations

`--validate` checks the spec and referenced XML inputs, including sample limits
and simulation geometry. During type relabeling, the generator checks the
`UCDA` file signature and recomputes the CRC. These safeguards do not establish
scientific equivalence to an experimental run.

Known limitations:

- **Wavelength scans (`wi`):** The synthetic `wi` fixture is a relabeled
  radius-based file. It has the correct type tag but not a true wavelength
  x-axis because `us_astfem_sim` has no native wavelength-scan mode. Its model
  is a simulation placeholder.
- **Signal magnitude:** Checked-in models default to `signal="1"`. Use a
  channel's `signal` field in the spec to test another magnitude.

## Add or update data

### Generated data

1. Follow the [configuration workflow](config/README.md#add-or-change-configuration)
   to update an existing spec or add a compatible spec with
   a unique `dataset_name`.
2. Add or update model, buffer, or simulation-parameter XML only when the
   required input does not already exist.
3. Run the generator with `--spec <name>` when not using `base.json`. Add
   `--samples` when updating the samples tier.
4. Review the regenerated zip, checksum file, and README before committing.

Do not edit files under `datasets/generated/` by hand. Their README and
checksums are generator output.

### Curated reference data

1. Add or replace the zip under
   `datasets/manual/US_TD_NNN_Short_Description/`.
2. Regenerate the containing directory's `checksums.sha256`.
3. Document the dataset's provenance, de-identification, contents, and known
   limitations when supporting documentation is present.

To generate a GNU-format checksum file for all zips in the current directory:

```bash
sha256sum *.zip > checksums.sha256
```

On macOS:

```bash
shasum -a 256 *.zip > checksums.sha256
```

## Repository boundary

This repository stores generator code, configuration, and test datasets.
Simulation executables and runtime reference files remain in the UltraScan
installation or build tree.
