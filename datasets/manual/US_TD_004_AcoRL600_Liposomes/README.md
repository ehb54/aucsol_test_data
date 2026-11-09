# US_TD_004 AcoRL-600 reference liposomes

Real analytical ultracentrifugation data for fluorescently labeled liposomes,
in OpenAUC format, published by its creators on Zenodo under the Creative
Commons Attribution 4.0 International license.

## Attribution

| | |
|---|---|
| Title | AUC Data for manuscript "Characterization of Acoerela AcoRL-600 Reference Liposomes using Analytical Ultracentrifugation" |
| Creators | Reece Anthony Martin; Borries Demeler (University of Lethbridge) |
| Published | 2026-03-01, Zenodo |
| Source | <https://doi.org/10.5281/zenodo.18827657> |
| License | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

Cite as: Martin, R. A., & Demeler, B. (2026). *AUC Data for manuscript
"Characterization of Acoerela AcoRL-600 Reference Liposomes using Analytical
Ultracentrifugation"* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18827657

This copy is redistributed under the same license. The creators do not
endorse its use here.

## Changes from the source

The source archive, `Acoerela_AcoRL-600-AUC-Data.tar.gz` (3,536,920 bytes,
md5 `b59414c8f540ad4defd762535b267cbc`), is repackaged as
`Acoerela_AcoRL-600-AUC-Data.zip` so this repository's tools can unpack it.
The 14 files inside are unchanged.

## Contents

Three runs, each with its `.auc` data, experiment and time-state files, and
edit profiles:

| Run | Optical system | Cell | Wavelength |
|---|---|---|---|
| `Acoerela_AcoRL-600-ABS_13NOV24_14JAN26` | `RI` | 2A | 372 and 518 nm |
| `Acoerela_AcoRL-600-FLUOR_18OCT24_14JAN26` | `FI` | 1A | 488 nm |
| `Acoerela_AcoRL-600-INF_15NOV24_14JAN26` | `IP` | 2A | 660 nm |

## Use here

Real `FI` and `IP` reference data. The synthetic fluorescence in
`datasets/generated/` is calibrated against the `FI` run: the detector's
5.603-7.296 cm range, its background before the meniscus, and its noise.

## Limitations

Buffer, centerpiece and instrument details not in the OpenAUC files are in the
manuscript. A liposome sample's fluorescence is noisier than a dissolved
protein's, because individual particles add their own scatter.
