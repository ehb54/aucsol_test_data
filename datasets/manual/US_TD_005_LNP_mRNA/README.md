# US_TD_005 mRNA-loaded lipid nanoparticles

Real Optima AUC data for protein-conjugated, mRNA-loaded lipid nanoparticles,
in OpenAUC format, published by its creator on Zenodo under the Creative
Commons Attribution 4.0 International license.

## Attribution

| | |
|---|---|
| Title | AUC Data for manuscript "High-resolution characterization of protein-conjugated, mRNA-loaded lipid nanoparticles by analytical ultracentrifugation" |
| Creator | Borries Demeler (University of Lethbridge) |
| Published | 2025-08-30, Zenodo |
| Source | <https://doi.org/10.5281/zenodo.17009858> |
| License | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

Cite as: Demeler, B. (2025). *AUC Data for manuscript "High-resolution
characterization of protein-conjugated, mRNA-loaded lipid nanoparticles by
analytical ultracentrifugation"* [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.17009858

This copy is redistributed under the same license. The creator does not
endorse its use here.

## Changes from the source

The source archive, `LNP-data.tar.gz` (16,405,779 bytes, md5
`cebc67142fda3fa36444818dec9c50fb`), is repackaged as `LNP-data.zip` so this
repository's tools can unpack it. The 33 files inside are unchanged.

## Contents

Four Optima AUC experiments, each with its `.auc` data and edit profiles:

| Experiment | Optical system | Cells | Wavelength |
|---|---|---|---|
| `LNP-DensityMatch` (four D2O/H2O ratios) | `RI` | 1-3 and 5-7, A and B | 300 nm |
| `LNP-Fluorescence` | `FI` | 5A, 6A | 488 nm |
| `LNP-UV-Control1` | `RI` | 2A | 280 nm |
| `LNP-UV-Control2` | `RI` | 7A | 280 nm |

The edit profiles can be copied to `~/ultrascan/results/<RunID>` to recreate
the creator's edited datasets.

## Use here

Real `FI` reference data alongside `US_TD_004`, and real `RI` data stored as
pseudo-absorbance, whose random noise (0.0009-0.0019 OD) the synthetic
absorbance noise is checked against.

## Limitations

Buffer, centerpiece and instrument details not in the OpenAUC files are in the
manuscript. Nanoparticle fluorescence is much noisier than a dissolved
protein's, because individual particles add their own scatter.
