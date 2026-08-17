# UltraScan Test Data

Public `.auc` datasets for UltraScan system testing. The repository contains
synthetic simulator output and curated reference data; it does not contain
customer, patient, or proprietary third-party data.

This repository holds **data artifacts only**. The generator that produces the
synthetic datasets, and the model, buffer, and simulation-parameter
configuration it reads, are maintained separately and are not part of this
repository. Nothing here is executable.

## Choose a dataset

| Dataset | Use case |
|---|---|
| [`datasets/generated/base/`](datasets/generated/base/) | Standard synthetic runs using the checked-in simulation parameters |
| [`datasets/generated/base/samples/`](datasets/generated/base/samples/) | Smaller synthetic runs for tests that do not need full datasets |
| [`datasets/manual/`](datasets/manual/) | Curated reference datasets added by hand |

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
The root `VERSION` file records the current version.

## About the generated data

### Which revision produced a dataset

Because the data and the generator now live in separate repositories, each
generated tier's `README.md` is stamped with the LIMS generator commit that
produced it, and with whether that working tree had uncommitted changes:

```text
> Generated 2026-08-16 16:09 UTC by `scripts/test-corpus/generate_synthetic_data.py`
> from LIMS generator commit `2201bab`.
```

That stamp is the only link from an archive back to the code that built it.
Capture it alongside the repository tag and checksum result when recording a
test execution.

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

Before writing a tier, the generator validates its inputs, including sample
limits and simulation geometry, and during type relabeling it checks the `UCDA`
file signature and recomputes the CRC. These safeguards do not establish
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

Steps 1 through 3 happen in the LIMS repo, not here; only the review and commit
of the resulting artifacts happens in this repository.

1. Follow the configuration workflow at
   `scripts/test-corpus/config/README.md#add-or-change-configuration` to update
   an existing spec or add a compatible spec with a unique `dataset_name`.
2. Add or update model, buffer, or simulation-parameter XML under
   `scripts/test-corpus/config/`, and only when the required input does not
   already exist.
3. Run the generator with `--output-root` pointing at this checkout, plus
   `--spec <name>` when not using `base.json` and `--samples` when updating the
   samples tier.
4. Review the regenerated zip, checksum file, and stamped README here before
   committing. Commit the matching configuration change in the LIMS repo too,
   so the commit named in the stamp actually contains the inputs used.

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

This repository stores test datasets and their provenance: zips, checksum
files, and generated tier READMEs.

- Generator code and its configuration live in the LIMS repository
  (private), under `scripts/test-corpus/`.
- Simulation executables and runtime reference files remain in the UltraScan
  installation or build tree ([`ehb54/ultrascan3`](https://github.com/ehb54/ultrascan3)),
  and are vendored by neither repository.

The split is code versus artifacts: everything executable and every generator
input sits in the LIMS repo, so a dataset here can be versioned, pinned, and
verified independently of the stack that consumes it.
