# UltraScan Test Data

Public `.auc` datasets for UltraScan system testing. The repository contains
synthetic simulator output, curated reference data, and published real
datasets redistributed under open licenses (see
[Third-party datasets](#third-party-datasets)). It does not contain customer,
patient, or proprietary data.

This repository holds **data artifacts only**: dataset archives, checksums, and
documentation. Nothing here is executable.

## Choose a dataset

| Dataset | Use case |
|---|---|
| [`datasets/generated/base/`](datasets/generated/base/) | Standard full-size synthetic runs |
| [`datasets/generated/base/samples/`](datasets/generated/base/samples/) | Smaller synthetic runs for tests that do not need full datasets |
| [`datasets/generated/examples/`](datasets/generated/examples/) | Synthetic examples of supported experiment layouts |
| [`datasets/generated/mpi/`](datasets/generated/mpi/) | Synthetic MPI analysis fixtures |
| [`datasets/generated/noise/`](datasets/generated/noise/) | Synthetic noise-model fixtures |
| [`datasets/manual/`](datasets/manual/) | Curated reference datasets added by hand, including real instrument data |

## Third-party datasets

These datasets are real instrument data published by their creators on
Zenodo under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
license, and are redistributed here under the same license. Each dataset's
README gives its full attribution, how to cite it, and any changes made.
When you use one, cite its source.

| Dataset | Creators | Source |
|---|---|---|
| [`US_TD_004_AcoRL600_Liposomes`](datasets/manual/US_TD_004_AcoRL600_Liposomes/) | R. A. Martin, B. Demeler | <https://doi.org/10.5281/zenodo.18827657> |
| [`US_TD_005_LNP_mRNA`](datasets/manual/US_TD_005_LNP_mRNA/) | B. Demeler | <https://doi.org/10.5281/zenodo.17009858> |
| [`US_TD_006_Myoglobin_BFE`](datasets/manual/US_TD_006_Myoglobin_BFE/) | L. Dobler, W. Cao, R. Martin, B. Demeler | <https://doi.org/10.5281/zenodo.19815759> |
| [`US_TD_007_NT2RepCT_Optima_Export`](datasets/manual/US_TD_007_NT2RepCT_Optima_Export/) | D. Fedorov | <https://doi.org/10.5281/zenodo.13365377> |

## Get and verify the data

```bash
git clone https://github.com/ehb54/aucsol_test_data.git
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
The root [`VERSION`](VERSION) file records the current version.

## About the generated data

### Optical data types

This section describes the `base` and `noise` tiers (standard and `samples`),
which are shaped like instrument runs. The `examples` and `mpi` tiers are
simpler; see [Examples and MPI tiers](#examples-and-mpi-tiers).

The simulators write each optical system's data in its own form:

- **`RA`**: absorbance on the instrument's radial window (5.75-7.249 cm at
  0.001 cm), with random noise of about 0.002 OD, clipped at an OD limit where
  the bottom of the cell piles up.
- **`RI`**: in `base`, raw intensities as the instrument records them: the
  sample sector on its channel and the reference sector on the partner
  channel (A/B, C/D, E/F, G/H), with counts noise. These are what the mock
  Optima serves; UltraScan converts them to pseudo-absorbance against a
  reference before analysis. In `noise`, pseudo-absorbance: one sample
  channel on the absorbance scale, clipped like `RA`, which analysis can fit
  directly.
- **`IP`**: interference fringes on the interference detector's own grid
  (2,048 points from 5.8 cm), with baseline offsets, fixed radial structure
  and occasional whole-fringe jumps.
- **`FI`**: fluorescence on the fluorescence detector's own range,
  5.603-7.296 cm at 0.001 cm (1,694 points). Past the cell bottom it reads no
  signal, only noise like the air before the meniscus. The `base` tiers add
  the detector's constant background (200 counts) and noise calibrated to
  real Optima FI runs.
- **`WI`**: wavelength scans, intensity across wavelengths at one radius,
  with the radius stored in each scan's wavelength field. A wavelength scan
  has no single wavelength, so its files keep the placeholder `123` in their
  names where other files name their wavelength.

A run's cells are scanned in turn, and the recorded speed and temperature
vary as an instrument's do. Every run of one experiment shares one time
state.

### Examples and MPI tiers

The `examples` tier illustrates experiment layouts and the `mpi` tier holds
analysis fixtures. Neither uses the instrument window or scan schedule:

- data starts just past the meniscus (about 5.857 cm) and ends at the cell
  bottom (7.167-7.22 cm), with no air region;
- runs have 30 scans about 306 s apart, at a constant 45,000 rpm and 20.00 °C
  (in `mpi`, `t2-dmga-reacting` is scheduled and records varying speed and
  temperature, like the `base` and `noise` tiers);
- `IP` data uses the same 0.001 cm grid as absorbance (1,311-1,361 points),
  not the interference detector's 2,048-point grid;
- `examples` data has no random noise. `RI` there is pseudo-absorbance, as in
  `noise`.

Where a simulator cannot write a type natively (an `RI` channel on B, D, F or
H, for example), the generator simulates it as `RA`, changes the two-byte type
at offset 6, and recomputes the trailing little-endian CRC-32.

UltraScan seeds this CRC calculation with `0xFFFFFFFF`, rather than zlib's
default initial value of `0`. The equivalent Python calculation is:

```python
import zlib

crc = zlib.crc32(file_bytes[:-4], 0xFFFFFFFF) & 0xFFFFFFFF
```

### Validation and limitations

The generated archives are test fixtures. Their presence and checksums do not
establish scientific equivalence to an experimental run.

Known limitations:

- **Synthetic spectra:** The `wi` wavelength scan and the multi-wavelength
  datasets use synthetic extinction spectra, not measured compounds.
- **RI reference sector:** A 1 OD sample puts the reference sector at about
  38,000-41,000 counts, above the 3,600-14,000 counts measured on real Optima
  plateaus; the sample sector is within that range.

## Add or update data

### Generated data

When importing newly generated data:

1. Import the archives, tier README, and `checksums.sha256` together under the
   appropriate directory in `datasets/generated/`.
2. Verify the checksum file before committing.

Generated provenance must identify a committed generator revision. Output
marked as having uncommitted generator or input changes is suitable for
development only and must be regenerated from a clean revision before a
versioned release is tagged.

### Curated reference data

1. Add or replace the zip under the appropriate directory in
   `datasets/manual/`.
2. Regenerate the containing directory's `checksums.sha256`.
3. Document the dataset's provenance, de-identification, contents, and known
   limitations when supporting documentation is present.

To generate a GNU-format checksum file for every archive (`.zip` and
`.tar.gz`) in the current directory:

```bash
sha256sum $(ls *.zip *.tar.gz 2>/dev/null) > checksums.sha256
```

On macOS:

```bash
shasum -a 256 $(ls *.zip *.tar.gz 2>/dev/null) > checksums.sha256
```

## Repository contents

This repository stores test dataset zips, checksum files, and dataset READMEs.
