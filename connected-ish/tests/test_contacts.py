import pandas as pd

from connected_ish.contacts import (
    contact_uncertainty_m,
    detect_contacts,
    normalize_fluid,
)


def test_fluid_normalization():
    assert normalize_fluid("Oil") == "OIL"
    assert normalize_fluid("oil/water") == "OIL_WATER"
    assert normalize_fluid("unknown") == "UNKNOWN"


def test_uncertainty_rule():
    assert contact_uncertainty_m(100) == 5.0
    assert contact_uncertainty_m(500) == 15.0


def test_detect_owc():
    df = pd.DataFrame(
        [
            ["X1", "F1", 1000, 20, 10, 20, 100, 30, "OIL"],
            ["X1", "F1", 1040, 20, 10, 18, 80, 70, "WATER"],
        ],
        columns=[
            "well", "formation", "tvd_scs_m", "gross_thickness_m",
            "net_pay_m", "porosity_pct", "permeability_md", "sw_pct", "fluid"
        ],
    )
    result = detect_contacts(df)
    assert len(result) == 1
    assert result.iloc[0]["contact_type"] == "OWC"
    assert result.iloc[0]["candidate_contact_tvd_scs_m"] == 1020
