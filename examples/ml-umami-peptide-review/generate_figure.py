#!/usr/bin/env python3
"""Generate an editable Chinese review figure for ML-guided umami peptide screening.

The output is plain SVG: text remains text and every panel, label, arrow, and
icon is an independently editable element. No plotting package is required.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

W, H = 1800, 1260
OUT = Path(__file__).with_name("ml_umami_peptide_screening.svg")
FONT = "Noto Sans SC Thin"

COLORS = {
    "ink": "#17324D",
    "muted": "#536779",
    "line": "#B9C8D3",
    "bg": "#F6F9FB",
    "white": "#FFFFFF",
    "blue": "#DCECF7",
    "blue_dark": "#2474A6",
    "teal": "#D9F0EB",
    "teal_dark": "#168276",
    "amber": "#FCE9C6",
    "amber_dark": "#C77916",
    "purple": "#EAE3F6",
    "purple_dark": "#7652A8",
    "red": "#F8E1E1",
    "red_dark": "#B84A4A",
    "green": "#E5F2D9",
    "green_dark": "#5B8C36",
}


def attrs(**kwargs: object) -> str:
    return " ".join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in kwargs.items())


def text(x: float, y: float, value: str, size: int = 24, weight: int = 400,
         fill: str | None = None, anchor: str = "start", extra: str = "") -> str:
    fill = fill or COLORS["ink"]
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>'
        f'{escape(value)}</text>'
    )


def multiline(x: float, y: float, lines: list[str], size: int = 22,
              leading: int = 31, fill: str | None = None, weight: int = 400,
              anchor: str = "start") -> str:
    fill = fill or COLORS["ink"]
    tspans = "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else leading}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{tspans}</text>'
    )


def rounded_rect(x: float, y: float, w: float, h: float, fill: str,
                 stroke: str = "none", sw: float = 1.5, rx: float = 18) -> str:
    return f'<rect {attrs(x=x, y=y, width=w, height=h, rx=rx, fill=fill, stroke=stroke, stroke_width=sw)}/>'


def pill(x: float, y: float, w: float, label: str, fill: str, ink: str) -> str:
    return rounded_rect(x, y, w, 38, fill, rx=19) + text(x + w / 2, y + 27, label, 19, 600, ink, "middle")


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = "#6E8798",
          dashed: bool = False, width: float = 3) -> str:
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    return (
        f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" marker-end="url(#arrow)"{dash}/>'
    )


def stage_panel(i: int, x: float, y: float, w: float, h: float, title: str,
                subtitle: str, fill: str, dark: str, bullets: list[str],
                output: str) -> str:
    parts = [f'<g id="stage-{i}" data-editable="true">']
    parts.append(rounded_rect(x, y, w, h, COLORS["white"], COLORS["line"], 1.5, 24))
    parts.append(rounded_rect(x, y, w, 105, fill, rx=24))
    parts.append(f'<circle cx="{x + 42}" cy="{y + 42}" r="25" fill="{dark}"/>')
    parts.append(text(x + 42, y + 51, str(i), 24, 700, COLORS["white"], "middle"))
    parts.append(text(x + 78, y + 43, title, 23, 700))
    parts.append(text(x + 78, y + 75, subtitle, 17, 400, COLORS["muted"]))
    yy = y + 145
    for bullet in bullets:
        parts.append(f'<circle cx="{x + 28}" cy="{yy - 7}" r="4" fill="{dark}"/>')
        parts.append(text(x + 43, yy, bullet, 18, 400))
        yy += 43
    parts.append(rounded_rect(x + 18, y + h - 66, w - 36, 44, fill, rx=10))
    parts.append(text(x + w / 2, y + h - 36, output, 19, 700, dark, "middle"))
    parts.append("</g>")
    return "".join(parts)


def build_svg() -> str:
    s: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        "<defs>",
        '<marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="5" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#6E8798"/></marker>',
        '<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">'
        '<feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#17324D" flood-opacity="0.10"/></filter>',
        "</defs>",
        f'<rect width="{W}" height="{H}" fill="{COLORS["bg"]}"/>',
        '<g id="title" data-editable="true">',
        text(80, 76, "机器学习驱动的鲜味肽发现：从候选空间到感官证据", 42, 700),
        text(80, 116, "可复用的闭环筛选框架｜机器学习用于优先级排序，不能替代真实感官验证", 23, 400, COLORS["muted"]),
        pill(1515, 52, 205, "综述框架 · 2026", COLORS["teal"], COLORS["teal_dark"]),
        "</g>",
        '<g id="pipeline-shadow" filter="url(#shadow)">',
    ]

    xs = [65, 410, 755, 1100, 1445]
    panel_w, panel_y, panel_h = 290, 590, 520
    stages = [
        ("候选肽空间", "来源决定外推边界", COLORS["blue"], COLORS["blue_dark"],
         ["食源蛋白 / 发酵体系", "LC–MS/MS 与从头测序", "虚拟酶解 / 宏基因组", "数据库：已知鲜味与负例"], "输出：去重候选序列库"),
        ("数据治理与表征", "先防泄漏，再谈性能", COLORS["teal"], COLORS["teal_dark"],
         ["去重、冲突标签与同源聚类", "训练 / 验证 / 独立测试划分", "AAC、DPC、CTD、理化描述符", "ProtBERT / Transformer 嵌入"], "输出：可追溯特征矩阵"),
        ("多模型智能筛选", "预测概率 ≠ 感官强度", COLORS["amber"], COLORS["amber_dark"],
         ["可解释：iUmami-SCM", "集成学习：UMPred-FRL / GBDT", "深度学习：BERT / RNN / 注意力", "共识排序 + 校准 + SHAP"], "输出：高置信候选短名单"),
        ("机制与可开发性排序", "结构证据用于解释与降本", COLORS["purple"], COLORS["purple_dark"],
         ["毒性 / 致敏 / 溶解性 / 苦味", "T1R1/T1R3 结构建模", "分子对接 + 动力学 / MM-GBSA", "氢键、静电与疏水作用"], "输出：机制支持的优先级"),
        ("实验与食品基质验证", "最终证据来自真实体系", COLORS["green"], COLORS["green_dark"],
         ["肽合成与纯度确认", "盲法感官：阈值 / 剂量–反应", "电子舌 / SPR 等正交证据", "食品基质、协同增鲜与稳定性"], "输出：经验证鲜味肽"),
    ]
    for idx, (x, spec) in enumerate(zip(xs, stages), 1):
        s.append(stage_panel(idx, x, panel_y, panel_w, panel_h, *spec))
        if idx < 5:
            s.append(arrow(x + panel_w + 8, panel_y + 286, xs[idx] - 8, panel_y + 286))
    s.append("</g>")

    # Evidence funnel above the main pipeline.
    s.extend([
        '<g id="evidence-funnel" data-editable="true">',
        text(80, 186, "证据漏斗", 24, 700),
        text(80, 218, "候选减少，证据增强", 19, 400, COLORS["muted"]),
        '<path d="M 310 175 L 1665 175 L 1530 355 L 445 355 Z" fill="#EAF1F5" stroke="#C5D4DE" stroke-width="1.5"/>',
        '<path d="M 310 175 L 650 175 L 705 355 L 445 355 Z" fill="#DCECF7"/>',
        '<path d="M 650 175 L 930 175 L 970 355 L 705 355 Z" fill="#D9F0EB"/>',
        '<path d="M 930 175 L 1190 175 L 1230 355 L 970 355 Z" fill="#FCE9C6"/>',
        '<path d="M 1190 175 L 1435 175 L 1490 355 L 1230 355 Z" fill="#EAE3F6"/>',
        '<path d="M 1435 175 L 1665 175 L 1530 355 L 1490 355 Z" fill="#E5F2D9"/>',
        text(500, 250, "10³–10⁶", 28, 700, COLORS["blue_dark"], "middle"),
        text(500, 285, "候选序列", 20, 400, COLORS["ink"], "middle"),
        text(790, 250, "规范数据", 25, 700, COLORS["teal_dark"], "middle"),
        text(790, 285, "减少偏差", 20, 400, COLORS["ink"], "middle"),
        text(1080, 250, "Top-k", 28, 700, COLORS["amber_dark"], "middle"),
        text(1080, 285, "模型共识", 20, 400, COLORS["ink"], "middle"),
        text(1350, 250, "10–100", 28, 700, COLORS["purple_dark"], "middle"),
        text(1350, 285, "机制优选", 20, 400, COLORS["ink"], "middle"),
        text(1538, 250, "1–10", 28, 700, COLORS["green_dark"], "middle"),
        text(1538, 285, "实验证实", 20, 400, COLORS["ink"], "middle"),
        text(990, 401, "计算证据", 20, 600, COLORS["muted"], "middle"),
        arrow(1060, 394, 1518, 394, COLORS["green_dark"], False, 3),
        text(1590, 401, "感官证据", 20, 700, COLORS["green_dark"], "middle"),
        "</g>",
    ])

    # Closed-loop feedback and caveat strip.
    s.extend([
        '<g id="feedback-loop" data-editable="true">',
        '<path d="M 1590 1080 C 1590 1185, 260 1185, 260 1080" fill="none" stroke="#168276" stroke-width="4" stroke-dasharray="11 8" marker-end="url(#arrow)"/>',
        rounded_rect(590, 1145, 620, 52, COLORS["teal"], COLORS["teal_dark"], 1.2, 26),
        text(900, 1179, "主动学习闭环：实验标签 → 数据库更新 → 模型再训练", 21, 700, COLORS["teal_dark"], "middle"),
        "</g>",
        '<g id="caveats-and-citations" data-editable="true">',
        rounded_rect(65, 442, 1670, 105, COLORS["white"], COLORS["line"], 1.2, 16),
        text(92, 478, "关键质量控制", 22, 700, COLORS["red_dark"]),
        multiline(255, 475, [
            "① 按序列同源性划分数据，避免近重复肽跨集合造成性能虚高；",
            "② 报告 MCC / AUROC / AUPRC 与外部测试，不只报告准确率；③ 对接分数不能直接代表鲜味阈值。",
        ], 19, 28, COLORS["ink"]),
        text(1710, 532, "[1–7]", 18, 600, COLORS["muted"], "end"),
        "</g>",
        text(65, 1235, "图注建议：ML = machine learning；AAC/DPC/CTD = 序列组成特征；SPR = 表面等离子体共振。图为文献综合框架，非定量比例。", 17, 400, COLORS["muted"]),
        text(1735, 1235, "CC BY 4.0 · SciPilot", 17, 600, COLORS["muted"], "end"),
        "</svg>",
    ])
    return "\n".join(s)


def main() -> None:
    OUT.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
