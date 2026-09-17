# connected-ish

### Because reservoirs are connected-ish until the data prove otherwise. 🛢️

[![Tests](https://github.com/afsanazeynalli/connected-ish/actions/workflows/tests.yml/badge.svg)](https://github.com/afsanazeynalli/connected-ish/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

`connected-ish` is a transparent, uncertainty-aware Python research workflow for screening **fluid contacts and interwell connectivity** from well and formation data.

The project is deliberately built around a simple scientific principle:

> **A reservoir interpretation should expose its assumptions instead of hiding them inside a spreadsheet.**

## Why this project exists

Fluid contacts are often reduced to a single picked depth, while connectivity can be treated as an implicit assumption. In heterogeneous reservoirs, both can carry uncertainty and should be traceable to observations.

`connected-ish` turns those ideas into a reproducible workflow:

```text
well / formation observations
            ↓
      fluid classification
            ↓
 candidate GOC / OWC / GWC
            ↓
 transparent uncertainty envelope
            ↓
 static connectivity evidence
            ↓
 future dynamic calibration / Bayesian update
```

The current implementation is a **screening and research prototype**. It does not claim to prove geological communication or provide field-approved contacts.

## Features

- 🔎 Candidate **GOC, OWC and GWC** detection from adjacent fluid observations
- 📐 Transparent contact uncertainty using a configurable screening rule
- 🪨 Thickness-weighted permeability calculation
- 🔗 Static interwell connectivity screening
- 📊 Pairwise well similarity with optional spatial distance
- 🧪 Synthetic example data for reproducibility
- ✅ Automated unit tests and GitHub Actions
- 📚 Scientific reference map linking methods to literature
- 📝 `CITATION.cff` for software citation
- 🚫 No Excel dependency

## Quick start

```bash
git clone https://github.com/afsanazeynalli/connected-ish.git
cd connected-ish

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -e ".[dev]"
```

Run the example:

```bash
connected-ish --input data/sample_well_data.csv --output outputs
```

Or:

```bash
python -m connected_ish.cli --input data/sample_well_data.csv --output outputs
```

Expected outputs:

```text
outputs/
├── candidate_contacts.csv
├── well_summary.csv
└── connectivity_screening.csv
```

Run tests:

```bash
pytest -q
```

## Input schema

### Required

| Column | Meaning |
|---|---|
| `well` | Well identifier |
| `formation` | Reservoir / formation unit |
| `tvd_scs_m` | TVD subsea, m |
| `gross_thickness_m` | Gross interval thickness, m |
| `net_pay_m` | Net-pay thickness, m |
| `porosity_pct` | Porosity, % |
| `permeability_md` | Average permeability, md |
| `sw_pct` | Water saturation, % |
| `fluid` | Observed/interpreted fluid class |

### Optional

| Column | Meaning |
|---|---|
| `tst_s_m` | Shifted/effective thickness, if available |
| `x_m`, `y_m` | Spatial coordinates |
| `pressure_mpa` | Dynamic pressure evidence |
| `production_rate` | Production evidence |
| `injection_rate` | Injection evidence |

The included dataset is synthetic and should not be interpreted as measured field data.

## Methodology

### 1. Fluid-contact screening

Records are sorted by well, formation and TVD. Adjacent observations are checked for transitions such as:

- `GAS → OIL` → candidate **GOC**
- `OIL → WATER` → candidate **OWC**
- `GAS → WATER` → candidate **GWC**

The candidate contact is the midpoint of the transition interval rather than an invented zero-thickness observation.

### 2. Contact uncertainty

The default screening envelope is:

```text
U = max(5 m, 0.03 × effective thickness)
```

This is a configurable research assumption—not a universal geological uncertainty standard.

### 3. Static connectivity screening

The current static index combines normalized:

- porosity
- log-transformed permeability
- net pay
- inverse water saturation

Default weights:

```text
porosity          0.20
permeability      0.35
net pay           0.25
water saturation  0.20
```

The resulting `static_connectivity_index` is a **relative screening index**, not a calibrated probability of communication.

### 4. Future dynamic update

The intended research pathway is:

```text
static evidence / prior
          ↓
pressure / production / injection / 4D evidence
          ↓
probabilistic update
          ↓
validated connectivity estimate
```

Potential dynamic evidence includes pressure interference, production/injection response, tracer response and 4D seismic.

## What this project does NOT claim

This repository is not:

- a reserves calculator
- a certified field model
- a calibrated 3D geomodel
- a history-matched reservoir simulator
- a replacement for seismic interpretation
- a replacement for pressure-transient or interference analysis
- proof of interwell communication

A high static similarity score does **not** automatically mean that two wells are connected.

## Research context

The scientific motivation combines reservoir characterization, uncertainty analysis, interwell connectivity, graph/network representations and physics-informed/data-driven workflows.

See [`docs/references.md`](docs/references.md) for the literature map and [`docs/methodology.md`](docs/methodology.md) for the detailed assumptions.

## Project structure

```text
connected-ish/
├── src/connected_ish/
│   ├── contacts.py
│   ├── connectivity.py
│   ├── io.py
│   └── cli.py
├── data/
│   ├── sample_well_data.csv
│   └── README.md
├── docs/
│   ├── methodology.md
│   └── references.md
├── tests/
│   ├── test_contacts.py
│   └── test_connectivity.py
├── .github/
│   ├── workflows/tests.yml
│   └── CONTRIBUTING.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── GITHUB_SETUP.md
├── LICENSE
└── pyproject.toml
```

## Data confidentiality

Do not publish proprietary field data, confidential well coordinates, internal interpretations, pressure histories or company-only datasets without authorization.

The public demonstration data in this repository are synthetic.

## Citation

If you use this software in research, please cite the repository using GitHub's **Cite this repository** feature. The project includes `CITATION.cff` for this purpose.

## License

MIT — see [`LICENSE`](LICENSE).
