import pandas as pd

from connected_ish.connectivity import (
    connectivity_screening,
    thickness_weighted_permeability,
)


def test_weighted_permeability():
    k = pd.Series([100.0, 200.0])
    h = pd.Series([10.0, 20.0])
    assert round(thickness_weighted_permeability(k, h), 6) == round((1000 + 4000) / 30, 6)


def test_connectivity_output():
    df = pd.DataFrame(
        {
            "well": ["A", "B", "C"],
            "formation": ["F1", "F1", "F1"],
            "porosity_pct": [10, 20, 15],
            "permeability_md": [10, 100, 40],
            "net_pay_m": [5, 20, 10],
            "sw_pct": [70, 20, 50],
        }
    )
    result = connectivity_screening(df)
    assert len(result) == 3
    assert result["static_connectivity_index"].between(0, 1).all()
