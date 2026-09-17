from __future__ import annotations

import math
import pandas as pd


FLUID_ALIASES = {
    "gas": "GAS",
    "g": "GAS",
    "oil": "OIL",
    "o": "OIL",
    "oil_water": "OIL_WATER",
    "oil/water": "OIL_WATER",
    "ow": "OIL_WATER",
    "water": "WATER",
    "w": "WATER",
    "gas_water": "GAS_WATER",
    "gas/water": "GAS_WATER",
    "gw": "GAS_WATER",
}


def normalize_fluid(value: object) -> str:
    if pd.isna(value):
        return "UNKNOWN"
    key = str(value).strip().lower().replace(" ", "_")
    return FLUID_ALIASES.get(key, "UNKNOWN")


def contact_uncertainty_m(
    effective_thickness_m: float,
    minimum_m: float = 5.0,
    fraction: float = 0.03,
) -> float:
    """Transparent screening uncertainty: max(minimum, fraction * thickness)."""
    if pd.isna(effective_thickness_m):
        return float(minimum_m)
    return max(float(minimum_m), float(fraction) * abs(float(effective_thickness_m)))


def classify_transition(shallow: str, deep: str) -> str | None:
    pair = (normalize_fluid(shallow), normalize_fluid(deep))
    mapping = {
        ("GAS", "OIL"): "GOC",
        ("GAS", "OIL_WATER"): "GOC",
        ("GAS", "WATER"): "GWC",
        ("OIL", "WATER"): "OWC",
        ("OIL_WATER", "WATER"): "OWC",
        ("GAS_WATER", "WATER"): "GWC",
        ("GAS", "UNKNOWN"): "GAS-UNKNOWN",
        ("OIL", "UNKNOWN"): "OIL-UNKNOWN",
    }
    return mapping.get(pair)


def detect_contacts(
    df: pd.DataFrame,
    minimum_uncertainty_m: float = 5.0,
    uncertainty_fraction: float = 0.03,
) -> pd.DataFrame:
    """Detect adjacent fluid transitions within each well/formation.

    Records are sorted from shallower to deeper TVD. The returned contact
    depth is the midpoint of the transition interval.
    """
    required = {
        "well", "formation", "tvd_scs_m", "gross_thickness_m",
        "net_pay_m", "porosity_pct", "permeability_md", "sw_pct", "fluid"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    work = df.copy()
    work["fluid_norm"] = work["fluid"].map(normalize_fluid)
    work = work.sort_values(["well", "formation", "tvd_scs_m"])

    rows = []
    for (well, formation), group in work.groupby(["well", "formation"], sort=False):
        group = group.reset_index(drop=True)
        for i in range(len(group) - 1):
            a, b = group.iloc[i], group.iloc[i + 1]
            transition = classify_transition(a["fluid_norm"], b["fluid_norm"])
            if transition is None:
                continue

            interval = abs(float(b["tvd_scs_m"]) - float(a["tvd_scs_m"]))
            effective = max(
                float(a.get("net_pay_m", 0) or 0),
                float(b.get("net_pay_m", 0) or 0),
                interval,
            )
            unc = contact_uncertainty_m(
                effective, minimum_uncertainty_m, uncertainty_fraction
            )
            contact_tvd = (float(a["tvd_scs_m"]) + float(b["tvd_scs_m"])) / 2.0
            sw_diff = abs(float(b["sw_pct"]) - float(a["sw_pct"]))

            # Transparent screening score, deliberately not a probability.
            score = min(
                100.0,
                35.0
                + min(interval / max(effective, 1.0), 1.0) * 20.0
                + min(sw_diff / 50.0, 1.0) * 25.0
                + min(
                    (float(a["porosity_pct"]) + float(b["porosity_pct"])) / 2.0 / 30.0,
                    1.0,
                )
                * 20.0,
            )

            rows.append(
                {
                    "well": well,
                    "formation": formation,
                    "contact_type": transition,
                    "shallow_fluid": a["fluid_norm"],
                    "deep_fluid": b["fluid_norm"],
                    "shallow_tvd_scs_m": a["tvd_scs_m"],
                    "deep_tvd_scs_m": b["tvd_scs_m"],
                    "candidate_contact_tvd_scs_m": contact_tvd,
                    "uncertainty_m": unc,
                    "low_tvd_scs_m": contact_tvd - unc,
                    "high_tvd_scs_m": contact_tvd + unc,
                    "sw_difference_pct": sw_diff,
                    "screening_score": round(score, 2),
                    "evidence_flag": "candidate transition",
                }
            )

    return pd.DataFrame(rows)


def well_contact_summary(contacts: pd.DataFrame) -> pd.DataFrame:
    if contacts.empty:
        return pd.DataFrame(
            columns=["well", "n_candidates", "median_contact_tvd_scs_m", "p10_tvd_scs_m", "p90_tvd_scs_m"]
        )

    return (
        contacts.groupby("well")
        .agg(
            n_candidates=("candidate_contact_tvd_scs_m", "count"),
            median_contact_tvd_scs_m=("candidate_contact_tvd_scs_m", "median"),
            p10_tvd_scs_m=("candidate_contact_tvd_scs_m", lambda x: x.quantile(0.10)),
            p90_tvd_scs_m=("candidate_contact_tvd_scs_m", lambda x: x.quantile(0.90)),
        )
        .reset_index()
    )
