# UltraScan Test Datasets

Public test datasets for UltraScan system testing support.

All data is lab-owned (samples or simulations). No customer data is present.


## Versioning and Reproducibility

This repo uses simple repo-level Git tags (e.g., `v1.0.0`, `v1.1.0`) to mark reproducible states. A tag captures the state of all datasets at that point.

To check out a specific tagged state:

```bash
git checkout v1.2.0
```
## Test Development

Test procedures may reference the “latest” release of a dataset to avoid frequent updates to procedural text.

Example:
Use the latest release of `US_TD_001_DNA_Standards_AUC`.

During test execution, the exact repository tag and successful checksum verification must be recorded.
## Recording Test Execution

When running tests against this data, record the following:

1. **Repo tag** used (e.g., `v1.2.0`)
2. **Dataset ID(s)** used (e.g., `US_TD_001_DNA_Standards_AUC`)
3. **Checksum verification result** — confirm SHA-256 hashes match before use

Example test record entry:
```
Dataset: US_TD_001_DNA_Standards_AUC
Repo tag: v1.2.0
Checksum verified: PASS (sha256sum -c checksums.sha256)
```

## SHA-256 Checksum Verification

SHA-256 checksums are identical across operating systems as long as file bytes are identical. A checksum mismatch means the file is corrupt or was modified.

### Verify existing checksums

**Linux / macOS:**
```bash
cd datasets/US_TD_001_DNA_Standards_AUC
sha256sum -c checksums.sha256
```

**macOS (alternative):**
```bash
shasum -a 256 -c checksums.sha256
```

**Windows (PowerShell):**
```powershell
cd datasets\US-TD-001_DNA-Standards
Get-Content checksums.sha256 | ForEach-Object {
    $hash, $file = $_ -split '  '
    $actual = (Get-FileHash $file -Algorithm SHA256).Hash.ToLower()
    if ($actual -eq $hash) { "OK: $file" } else { "FAILED: $file" }
}
```

### Generate checksums for new files

**Linux / macOS:**
```bash
sha256sum *.zip > checksums.sha256
# or for all files:
find . -type f -not -name 'checksums.sha256' | sort | xargs sha256sum > checksums.sha256
```

**Windows (PowerShell):**
```powershell
Get-ChildItem -File | Where-Object { $_.Name -ne 'checksums.sha256' } | ForEach-Object {
    $hash = (Get-FileHash $_.Name -Algorithm SHA256).Hash.ToLower()
    "$hash  $($_.Name)"
} | Set-Content checksums.sha256
```

## Adding or Updating a Dataset

1. Create a folder under `datasets/` using the naming convention `US_TD_NNN_Short_Description`.
2. Add data files (or upload a zip as a GitHub Release asset if large).
3. Generate `checksums.sha256` in the dataset folder (see above).

To update an existing dataset, follow the same steps — just overwrite the files and regenerate checksums before tagging.


## Public Data Statement

All datasets in this repository are safe for public access. They contain only lab-owned reference samples or simulated data. No customer, patient, or proprietary third-party data is included.
```
