# Methodology

## 1. Objective

The Fluid Contact Detector is the fluid-contact interpretation layer of the CHIRAG FLOWSCAPE framework.

Its purpose is to preserve formation-specific fluid evidence and quantify uncertainty around candidate contacts.

## 2. Input model

The workbook uses formation-by-well observations including:

- well
- formation
- TVD-SCS
- thickness
- PHIT
- permeability
- Sw
- NTG
- net rock
- net reservoir
- net pay
- interpreted fluids

Optional `TST-S` can be supplied when a shifted thickness interpretation is available.

## 3. Depth model

For a formation:

```text
Top = TVD-SCS

Base = TVD-SCS + TST-S
```

when TST-S is supplied.

Otherwise the workbook falls back to the original gross thickness reference.

The resulting position is a theoretical interpretation quantity, not a measured fluid movement.

## 4. Contact uncertainty

The screening uncertainty is:

```text
U = MAX(5 m, 3% × effective thickness)
```

Therefore:

```text
Low contact  = Candidate TVD − U
High contact = Candidate TVD + U
```

The value should be replaced or recalibrated when field-quality uncertainty estimates become available.

## 5. Fluid transition detector

The tool preserves mixed-fluid observations instead of forcing them into sharp contacts.

### Direct transitions

```text
GAS → OIL       GOC
OIL → WATER     OWC
GAS → WATER     GWC
```

### Transition examples

```text
OIL → OIL_WATER
OIL_WATER → WATER
GAS → GAS_WATER
GAS_WATER → OIL
```

These are retained as transition intervals.

## 6. Saturation diagnostic

For a candidate downward fluid transition:

```text
ΔSw = Sw_lower − Sw_upper
```

If the lower interval has greater/equal Sw, the transition is saturation-consistent.

If not, the workbook creates a diagnostic conflict.

## 7. Screening score

The workbook uses a transparent weighted screening score based on:

1. direct transition evidence
2. Sw consistency
3. data completeness

This score is **not** the Dynamic Connectivity Index.

The DCI should only be calibrated when independent dynamic observations are available.

## 8. Scientific interpretation

The correct interpretation of a candidate contact is:

> candidate depth + uncertainty + supporting evidence + conflicting evidence

rather than:

> exact contact depth

## 9. Future dynamic layer

Future versions should ingest:

- pressure response
- injection/production perturbations
- response onset
- response magnitude
- persistence
- repeatability
- 4D seismic evidence

These can then update the static interpretation probabilistically.

## 10. Future uncertainty layer

Monte Carlo realizations can vary:

- contact depth
- thickness
- permeability
- NTG
- fault transmissibility
- shale continuity
- DCI weights
- dynamic thresholds

Outputs should include P10/P50/P90 and sensitivity ranking.

## 11. Validation

A field implementation should be tested against:

- blind-well observations
- independent pressure/rate response
- history-matched simulation
- alternative geological realizations
- cross-validation
- simple baseline methods

The goal is not merely to produce a visually plausible contact map, but to determine whether the integrated evidence improves prediction.
