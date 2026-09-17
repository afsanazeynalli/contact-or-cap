# Data

## Public repository rule

Do **not** place confidential company or field data in this directory.

For a public GitHub repository, use:

- synthetic data
- anonymized well IDs
- non-sensitive derived values
- toy examples

The research workflow can then be demonstrated without exposing proprietary information.

## Current workbook

`Fluid_Contact_Detector_CHIRAG.xlsx` contains the detector framework and master-data structure.

The workbook is designed so that sensitive source data can remain outside the public repository.

## Recommended private-data workflow

```text
Private field dataset
       ↓
Local / private repository
       ↓
Fluid Contact Detector
       ↓
Anonymized derived outputs
       ↓
Public research repository
```
