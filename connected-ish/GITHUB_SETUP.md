# GitHub setup — connected-ish

## Repository identity

**Repository name**

```text
connected-ish
```

**Description**

```text
Because reservoirs are connected-ish until the data prove otherwise. 🛢️
```

**Suggested topics**

```text
reservoir-engineering
reservoir-geoscience
petrophysics
fluid-contacts
interwell-connectivity
uncertainty-quantification
petroleum-engineering
subsurface
machine-learning
caspian-basin
```

GitHub recommends using a README, license and citation information to make repositories understandable and reusable. Repository topics also help classify and discover projects. See the official GitHub documentation for current guidance.

## If you are replacing `contact-or-cap`

1. Rename the GitHub repository to `connected-ish` under **Settings → General → Repository name**.
2. On your computer, replace the old repository contents with everything in this folder.
3. Make sure the old Excel workbook is removed.
4. Review `data/sample_well_data.csv` and confirm that only synthetic/non-confidential data are present.
5. Commit with:

```text
Replace spreadsheet prototype with connected-ish Python workflow
```

6. Push to `main`.

## If using GitHub Desktop

1. Open the local repository.
2. Copy all files from this prepared folder into the repository directory.
3. GitHub Desktop should show the changed/new files.
4. Enter the commit message above.
5. Click **Commit to main**.
6. Click **Push origin**.

## Repository settings after publishing

Recommended:

- Add the suggested topics.
- Keep the repository public only if all data are authorized for public release.
- Enable Dependabot alerts.
- Enable secret scanning/push protection where available.
- Keep GitHub Actions enabled so every push and pull request runs the test suite.

## Local verification

Before pushing:

```bash
pip install -e ".[dev]"
pytest -q
connected-ish --input data/sample_well_data.csv --output outputs
```

You should see five passing tests and three CSV output files.

## Important scientific positioning

Do not describe this repository as a field-validated connectivity model unless independent field validation has actually been performed.

Use language such as:

> uncertainty-aware screening workflow

> research prototype

> static connectivity evidence

> candidate fluid-contact detection

Avoid presenting the screening index as a calibrated probability.
