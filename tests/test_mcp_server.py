from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

import mcp_server


def test_capabilities_are_machine_readable() -> None:
    result = mcp_server.list_figure_capabilities()
    assert "profile_dataset" in result["workflow"]
    assert "chart-selection" in result["guidance_topics"]
    assert "csv" in result["data_inputs"]


def test_profile_dataset(tmp_path: Path) -> None:
    source = tmp_path / "experiment.csv"
    pd.DataFrame(
        {
            "group": ["control"] * 5 + ["treated"] * 5,
            "value": [1.0, 1.2, 0.9, 1.1, 1.3, 2.0, 2.1, 2.2, 1.9, 2.3],
        }
    ).to_csv(source, index=False)

    result = mcp_server.profile_dataset(str(source), ["group"])

    assert result["n_rows"] == 10
    assert result["group_summary"]["n_groups"] == 2
    assert result["columns"]["value"]["type"] == "continuous"


def test_audit_figure_png(tmp_path: Path) -> None:
    output = tmp_path / "figure.png"
    fig, ax = plt.subplots(figsize=(2, 1))
    ax.plot([0, 1], [0, 1])
    fig.savefig(output, dpi=300)
    plt.close(fig)

    result = mcp_server.audit_figure(
        str(output),
        min_dpi=300,
        target_width_inches=2,
        target_height_inches=1,
    )

    assert result["passed"] is True
    assert result["info"]["category"] == "raster"


def test_guidance_and_validation() -> None:
    guide = mcp_server.get_figure_guidance("chart_selection")
    assert guide["topic"] == "chart-selection"
    assert len(guide["content"]) > 100

    with pytest.raises(ValueError, match="Unknown topic"):
        mcp_server.get_figure_guidance("unknown")


def test_audit_requires_dimension_pair(tmp_path: Path) -> None:
    output = tmp_path / "figure.png"
    output.write_bytes(b"not needed")
    with pytest.raises(ValueError, match="both target width"):
        mcp_server.audit_figure(str(output), target_width_inches=3.5)


def test_json_safe_replaces_non_finite_values() -> None:
    assert mcp_server._json_safe({"x": float("nan"), "y": float("inf")}) == {
        "x": None,
        "y": None,
    }
