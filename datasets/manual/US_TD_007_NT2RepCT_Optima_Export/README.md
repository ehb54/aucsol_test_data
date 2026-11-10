# US_TD_007 NT-2Rep-CT native Optima export

One run of real analytical ultracentrifugation data for the mini-spidroin
NT-2Rep-CT, in the Optima AUC's own export format, published by its creator on
Zenodo under the Creative Commons Attribution 4.0 International license.

## Attribution

| | |
|---|---|
| Title | Analytical ultracentrifugation datasets of NT-2Rep-CT |
| Creator | Dmitrii Fedorov (Aalto University) |
| Published | 2024-09-14, Zenodo |
| Source | <https://doi.org/10.5281/zenodo.13365377> |
| License | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

Cite as: Fedorov, D. (2024). *Analytical ultracentrifugation datasets of
NT-2Rep-CT* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.13365377

The data supports the publication "Metastable liquid-liquid phase separation
and aging lead to strong processing path dependence in mini-spidroin
solutions". This copy is redistributed under the same license. The creator
does not endorse its use here.

## Changes from the source

`RunId861-all.tar.gz` is one of the record's twelve run archives, unchanged
(17,983,149 bytes, md5 `a4bf1b51dfe44c644d05d52b7edbf84a`). It stays a
`.tar.gz` because that is the instrument's export format. The other eleven runs
are not included; they are available from the source.

## Contents

RunId 861 corresponds to the publication's Fig. 2a and Fig. 4a: NT-2Rep-CT at
20 g/l in 20 mM Tris pH 8.0 and 110 mM Tris pH 7.2. The archive holds the
experiment definition (`ExpDefId159.json`), the system status
(`RunId861-SystemStatusData-s0001.fuge`), and one file per scan:

| Cells | Wavelengths | Files |
|---|---|---|
| 1 and 3 | 290 nm (100 scans each), 300 nm (250 scans each) | 700 absorbance (`.ra*`) and 700 intensity (`.ri*`) |

## Use here

A real example of the archive the Optima writes for a run
(`RunId<id>-all.tar.gz`), the format the mock Optima's HTTP interface
imitates for exports, and real absorbance and intensity data.

## Limitations

The per-scan export files need converting (for example with UltraScan's
import) before analysis. `--unpack` in the LIMS fetch script unpacks zips
only, so extract this archive by hand.
