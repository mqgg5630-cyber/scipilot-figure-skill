---
name: scipilot-figure-skill
description: Scientific data visualization advisor for publication-grade figures. Use for CSV/Excel profiling, chart selection, matplotlib/seaborn/plotly figures, Nature/Science/IEEE/Elsevier/PNAS journal formatting, CJK fonts, colorblind-safe palettes, figure export, and visual or compliance QA. Profiles data and clarifies the scientific claim before plotting. Does not create flowcharts or architecture diagrams.
---

# SciPilot Figure Skill for Antigravity

Work from the repository root. This workspace skill is paired with the
`scipilot-figure` MCP server in `.agents/mcp_config.json`.

## Required workflow

1. Clarify the claim the figure must support and locate the source data.
2. Call MCP tool `profile_dataset` for CSV/Excel input. If MCP is unavailable,
   run `python scripts/profile_data.py --help`, then use that script.
3. Call `get_figure_guidance` with `chart-selection`; recommend one chart with
   a short reason and one or two alternatives. Warn before complying with a
   misleading chart request.
4. Obtain the target journal/output dimensions. Use `journal-specs` guidance.
5. Read only the relevant recipe from `references/plot_recipes.md`. Render at
   final publication size; use a colorblind-safe palette and redundant coding.
6. Render a PNG preview and inspect it for clipped text, missing glyphs,
   occluded data, legend placement, panel alignment, and grayscale separation.
   Use `scripts/visual_qa.py` where applicable and iterate until clean.
7. Export vectors (PDF/SVG) for data figures whenever possible. Call MCP tool
   `audit_figure` on every final output and report warnings/failures.

## Hard rules

- Do not draw before understanding both the data and intended scientific claim.
- For fewer than 10 samples per group, show individual points; do not hide them
  behind mean-only bars.
- Avoid pie charts, 3D charts, unjustified dual-Y axes, truncated proportional
  axes, and rainbow/jet colormaps.
- State n, error definition (SD/SEM/CI), statistical test, correction, and
  significance symbols in the caption whenever relevant.
- Never use JPEG for line/text data figures.
- Do not use this skill for schematics, flowcharts, architecture diagrams, or
  non-data illustrations.

## Local resources

- Main detailed instructions: `SKILL.md`
- Chart decision tree: `references/chart_selection.md`
- Journal dimensions and fonts: `references/journal_specs.md`
- Plot recipes: `references/plot_recipes.md`
- Scientific pitfalls: `references/viz_pitfalls.md`
- Export checklist: `references/publication_checklist.md`
- Visual review loop: `references/visual_review.md`

Run scripts with `--help` before reading their implementation, per Antigravity's
progressive-disclosure guidance.
