from __future__ import annotations

import numpy as np
import pandas as pd


def thickness_weighted_permeability(
    permeability_md: pd.Series,
    thickness_m: pd.Series,
) -> float:
    """Calculate thickness-weighted mean permeability."""
    k = pd.to_numeric(permeability_md, errors="coerce")
    h = pd.to_numeric(thickness_m, errors="coerce")
    mask = k.notna() & h.notna() & (h > 0)
    if not mask.any():
        return float("nan")
    return float((k[mask] * h[mask]).sum() / h[mask].sum())


def _normalize(series: pd.Series, inverse: bool = False) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")
    lo, hi = x.min(), x.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        out = pd.Series(0.5, index=series.index)
    else:
        out = (x - lo) / (hi - lo)
    return 1.0 - out if inverse else out


def connectivity_screening(
    df: pd.DataFrame,
    weights: dict[str, float] | None = None,
) -> pd.DataFrame:
    """Create a screening-level static connectivity score.

    This score is intentionally a relative index, not a probability of
    communication. Dynamic evidence should be used for calibration/update.
    """
    required = {"well", "formation", "porosity_pct", "permeability_md", "net_pay_m", "sw_pct"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    w = weights or {
        "porosity": 0.20,
        "permeability": 0.35,
        "net_pay": 0.25,
        "water_saturation": 0.20,
    }

    out = df.copy()
    out["porosity_norm"] = _normalize(out["porosity_pct"])
    out["permeability_norm"] = _normalize(np.log1p(pd.to_numeric(out["permeability_md"], errors="coerce")))
    out["net_pay_norm"] = _normalize(out["net_pay_m"])
    out["sw_norm"] = _normalize(out["sw_pct"], inverse=True)

    out["static_connectivity_index"] = (
        w["porosity"] * out["porosity_norm"]
        + w["permeability"] * out["permeability_norm"]
        + w["net_pay"] * out["net_pay_norm"]
        + w["water_saturation"] * out["sw_norm"]
    )

    return out[
        [
            "well",
            "formation",
            "static_connectivity_index",
            "porosity_norm",
            "permeability_norm",
            "net_pay_norm",
            "sw_norm",
        ]
    ]


def pairwise_connectivity(
    df: pd.DataFrame,
    formation: str | None = None,
) -> pd.DataFrame:
    """Create a simple pairwise similarity matrix from well-level features.

    If x_m/y_m are available, distance is also returned. No claim of
    geological communication is made by this function.
    """
    work = df.copy()
    if formation is not None:
        work = work[work["formation"] == formation]

    cols = ["well", "formation", "porosity_pct", "permeability_md", "net_pay_m", "sw_pct"]
    work = work[cols + [c for c in ["x_m", "y_m"] if c in work.columns]]
    work = work.groupby("well", as_index=False).mean(numeric_only=True)

    rows = []
    for i in range(len(work)):
        for j in range(i + 1, len(work)):
            a, b = work.iloc[i], work.iloc[j]
            features = ["porosity_pct", "permeability_md", "net_pay_m", "sw_pct"]
            vals = []
            for f in features:
                scale = max(float(work[f].max() - work[f].min()), 1e-9)
                vals.append(abs(float(a[f]) - float(b[f])) / scale)
            similarity = 1.0 - float(np.mean(vals))

            row = {
                "well_a": a["well"],
                "well_b": b["well"],
                "formation": formation or "mixed",
                "static_similarity_index": max(0.0, min(1.0, similarity)),
            }
            if "x_m" in work.columns and "y_m" in work.columns:
                row["distance_m"] = float(
                    np.hypot(a["x_m"] - b["x_m"], a["y_m"] - b["y_m"])
                )
            rows.append(row)

    return pd.DataFrame(rows)
