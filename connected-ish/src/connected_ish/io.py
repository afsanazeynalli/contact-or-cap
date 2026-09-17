from __future__ import annotations

from pathlib import Path
import pandas as pd


def read_input(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() != ".csv":
        raise ValueError("connected-ish currently expects CSV input.")
    return pd.read_csv(path)


def write_outputs(
    contacts: pd.DataFrame,
    summary: pd.DataFrame,
    connectivity: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    contacts.to_csv(out / "candidate_contacts.csv", index=False)
    summary.to_csv(out / "well_summary.csv", index=False)
    connectivity.to_csv(out / "connectivity_screening.csv", index=False)
