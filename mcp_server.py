"""SciPilot Figure MCP server for Google Antigravity and other MCP clients.

The server uses stdio by default. Protocol messages are written by the MCP SDK;
this module deliberately does not print to stdout.
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path
from typing import Any, Mapping

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent
_REPO_REFERENCES = ROOT / "references"
_INSTALLED_REFERENCES = (
    Path(sys.prefix) / "share" / "scipilot-figure-skill" / "references"
)
REFERENCES = (
    _REPO_REFERENCES if _REPO_REFERENCES.is_dir() else _INSTALLED_REFERENCES
)
REFERENCE_FILES = {
    "chart-selection": "chart_selection.md",
    "data-profiling": "data_profiling.md",
    "journal-specs": "journal_specs.md",
    "plot-recipes": "plot_recipes.md",
    "publication-checklist": "publication_checklist.md",
    "visual-review": "visual_review.md",
    "viz-pitfalls": "viz_pitfalls.md",
}

mcp = FastMCP(
    "scipilot-figure",
    instructions=(
        "Scientific-figure advisor: profile data before choosing a chart, "
        "use publication-safe visual conventions, and audit exported figures."
    ),
)


def _resolved_file(path: str) -> Path:
    """Resolve a user path without restricting it to the server repository."""
    candidate = Path(os.path.expandvars(path)).expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    candidate = candidate.resolve()
    if not candidate.is_file():
        raise ValueError(f"File does not exist: {candidate}")
    return candidate


def _json_safe(value: Any) -> Any:
    """Normalize numpy/pandas values and non-finite floats for MCP JSON."""
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    # Convert numpy scalar values without importing numpy at server startup.
    if hasattr(value, "item") and callable(value.item):
        return _json_safe(value.item())
    if value is None or isinstance(value, (str, int, bool)):
        return value
    return str(value)


@mcp.tool()
def profile_dataset(path: str, group_columns: list[str] | None = None) -> dict[str, Any]:
    """Profile a CSV/XLS/XLSX data file before plotting.

    Returns inferred column types, missingness, distributions, outliers,
    correlations, group sizes, warnings, and initial chart suggestions.

    Args:
        path: Absolute path, or a path relative to the MCP process cwd.
        group_columns: Optional categorical columns used to calculate group n.
    """
    from scripts.profile_data import profile_data

    source = _resolved_file(path)
    try:
        result = profile_data(str(source), group_cols=group_columns or [])
    except Exception as exc:
        raise ValueError(f"Could not profile {source}: {exc}") from exc
    return _json_safe(result)


@mcp.tool()
def audit_figure(
    path: str,
    min_dpi: int = 300,
    target_width_inches: float | None = None,
    target_height_inches: float | None = None,
) -> dict[str, Any]:
    """Audit an exported PDF/SVG/EPS/PNG/TIFF/JPEG scientific figure.

    Checks format, DPI and final dimensions; where supported, it also checks
    PDF font embedding and SVG raster embedding. The operation is read-only.
    """
    from scripts.check_figure import check_figure

    source = _resolved_file(path)
    if (target_width_inches is None) != (target_height_inches is None):
        raise ValueError("Provide both target width and target height, or neither.")
    target = None
    if target_width_inches is not None and target_height_inches is not None:
        if target_width_inches <= 0 or target_height_inches <= 0:
            raise ValueError("Target dimensions must be positive.")
        target = (target_width_inches, target_height_inches)
    issues, info = check_figure(str(source), min_dpi=min_dpi, target_inches=target)
    return _json_safe(
        {
            "passed": not any(severity == "FAIL" for severity, _ in issues),
            "issues": [
                {"severity": severity, "message": message}
                for severity, message in issues
            ],
            "info": info,
        }
    )


@mcp.tool()
def get_figure_guidance(topic: str) -> dict[str, str]:
    """Return one SciPilot figure reference guide.

    Valid topics: chart-selection, data-profiling, journal-specs,
    plot-recipes, publication-checklist, visual-review, viz-pitfalls.
    Use chart-selection before plotting and publication-checklist before export.
    """
    normalized = topic.strip().lower().replace("_", "-").replace(" ", "-")
    filename = REFERENCE_FILES.get(normalized)
    if filename is None:
        raise ValueError(
            f"Unknown topic {topic!r}. Valid topics: {', '.join(REFERENCE_FILES)}"
        )
    path = REFERENCES / filename
    return {"topic": normalized, "content": path.read_text(encoding="utf-8")}


@mcp.tool()
def list_figure_capabilities() -> dict[str, Any]:
    """List MCP tools, guidance topics, supported inputs, and workflow order."""
    return {
        "workflow": [
            "clarify the scientific claim",
            "profile_dataset",
            "get_figure_guidance(topic='chart-selection')",
            "select journal dimensions and render at final size",
            "visually review the rendered preview",
            "audit_figure",
        ],
        "data_inputs": ["csv", "tsv", "xls", "xlsx"],
        "figure_inputs": ["pdf", "svg", "eps", "png", "tif", "tiff", "jpg", "jpeg"],
        "guidance_topics": list(REFERENCE_FILES),
        "scope": "data figures only; not flowcharts, architecture diagrams, or illustrations",
    }


def main() -> None:
    """Run the local stdio MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
