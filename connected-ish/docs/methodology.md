# Methodology

## 1. Fluid-contact screening

The algorithm sorts observations by well, formation and TVD subsea and evaluates adjacent records.

Examples:

- GAS → OIL → candidate GOC
- OIL → WATER → candidate OWC
- GAS → WATER → candidate GWC

A transition interval is not treated as a measured zero-thickness contact.

The screening contact is:

`TVD_contact = (TVD_shallow + TVD_deep) / 2`

## 2. Contact uncertainty

The default screening envelope is:

`U = max(5 m, 0.03 × effective thickness)`

This is a configurable research assumption, not a universal geological uncertainty standard.

## 3. Contact score

The contact score combines:

- transition interval relative to effective thickness
- water-saturation contrast
- average porosity of the adjacent observations

It is explicitly called a **screening score**.

It is not:
- a probability
- a confidence interval
- a reserves uncertainty
- a calibrated contact probability

## 4. Thickness-weighted permeability

Where multiple intervals contribute to a formation-level property:

`k_bar = Σ(k_i h_i) / Σh_i`

This prevents thin and thick intervals from being treated as equally influential when the intended aggregation is thickness weighted.

## 5. Static connectivity screening

The current implementation combines normalized:

- porosity
- log-transformed permeability
- net pay
- inverse water saturation

into a relative `static_connectivity_index`.

The default weights are:

- porosity: 0.20
- permeability: 0.35
- net pay: 0.25
- water saturation: 0.20

These are starting assumptions only.

## 6. What is deliberately NOT claimed

High static similarity does not prove interwell communication.

Actual connectivity can depend on:

- fault transmissibility
- shale/baffle continuity
- depositional architecture
- pressure communication
- completion intervals
- fluid properties
- dynamic depletion/injection history

The intended research pathway is:

`static prior → dynamic evidence → calibrated connectivity probability`

Potential dynamic evidence includes interference response, pressure propagation, production/injection response, tracer response, and 4D seismic.

## 7. Validation

For a field implementation, compare the screening outputs against independent evidence.

Possible validation questions:

- Did wells interpreted as connected show pressure response?
- Does the predicted contact agree with independent saturation/fluid evidence?
- Does the connectivity pattern survive alternative geological interpretations?
- Does the model remain stable under reasonable uncertainty perturbations?
- Can blind wells be withheld for validation?

## 8. Uncertainty expansion

A future research version can sample uncertainty in:

- formation thickness
- fluid-contact depth
- permeability
- NTG
- shale/baffle continuity
- fault transmissibility
- connectivity weights
- dynamic response thresholds

and report P10/P50/P90 distributions rather than a single deterministic answer.
