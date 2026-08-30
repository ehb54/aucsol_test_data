# UltraScan Test Data

Public `.auc` datasets for UltraScan system testing. The repository contains
synthetic simulator output and curated reference data; it does not contain
customer, patient, or proprietary third-party data.

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
| [`datasets/manual/`](datasets/manual/) | Curated reference datasets added by hand |

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

## Generate synthetic data

Synthetic tiers are produced by the
[`uslims_stack` test-corpus tooling](https://github.com/ehb54/uslims_stack/tree/1e1d44a/scripts/test-corpus).
Its [generation guide](https://github.com/ehb54/uslims_stack/blob/1e1d44a/scripts/test-corpus/test-corpus-pipeline.md)
documents the required inputs, commands, and validation process. Each tier
README records the generator revision and command used for that dataset.
Publish the resulting archives, tier README, and checksum manifest together.

## About the generated data

### Data-type relabeling

The UltraScan simulators write `RA`-tagged `.auc` files. For other test
categories, the generator changes the two-byte type at offset 6 and recomputes
the trailing little-endian CRC-32.

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

- **Wavelength scans (`wi`):** The synthetic `wi` fixture is a relabeled
  radius-based file. It has the correct type tag but not a true wavelength
  x-axis. It is a simulation placeholder.

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

To generate a GNU-format checksum file for all zips in the current directory:

```bash
sha256sum *.zip > checksums.sha256
```

On macOS:

```bash
shasum -a 256 *.zip > checksums.sha256
```

## Repository contents

This repository stores test dataset zips, checksum files, and dataset READMEs.
