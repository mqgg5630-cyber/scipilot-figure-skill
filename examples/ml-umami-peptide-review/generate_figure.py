#!/usr/bin/env python3
"""Generate an icon-rich, fully editable SVG review figure.

Every icon is an original vector assembled from SVG primitives. Text remains
editable text; no raster image or third-party logo is embedded.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

W, H = 1800, 1200
OUT = Path(__file__).with_name("ml_umami_peptide_screening.svg")
FONT = "Noto Sans SC Thin"
C = {
    "ink": "#17324D", "muted": "#5B7082", "line": "#AFC2CF",
    "blue": "#2B7FB3", "blue_l": "#E5F2FA", "teal": "#138A7E",
    "teal_l": "#E2F4F0", "amber": "#D18418", "amber_l": "#FFF1D8",
    "purple": "#7355A5", "purple_l": "#EEE8F8", "green": "#5A8F36",
    "green_l": "#EAF4DF", "red": "#B64B4B", "red_l": "#F9E8E8",
    "white": "#FFFFFF", "bg": "#F7FAFC", "membrane": "#F2D6A2",
}


def esc(v: object) -> str:
    return escape(str(v), quote=True)


def text(x: float, y: float, value: str, size: int = 22, weight: int = 400,
         fill: str | None = None, anchor: str = "start") -> str:
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill or C["ink"]}" '
            f'text-anchor="{anchor}">{escape(value)}</text>')


def rect(x: float, y: float, w: float, h: float, fill: str, rx: float = 18,
         stroke: str = "none", sw: float = 1.5) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def circle(x: float, y: float, r: float, fill: str, stroke: str = "none", sw: float = 1.5) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1: float, y1: float, x2: float, y2: float, color: str, sw: float = 3,
         dash: str = "") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{d}/>'


def path(d: str, fill: str = "none", stroke: str = "none", sw: float = 2,
         marker: bool = False, dash: str = "") -> str:
    m = ' marker-end="url(#arrow)"' if marker else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{m}{da}/>'


def group(gid: str, body: list[str]) -> str:
    return f'<g id="{gid}" data-editable="true">' + "".join(body) + "</g>"


def badge(x: float, y: float, w: float, value: str, fill: str, ink: str) -> str:
    return rect(x, y, w, 36, fill, 18) + text(x + w / 2, y + 25, value, 18, 700, ink, "middle")


def food_fish(x: float, y: float) -> str:
    b = [circle(x, y, 52, C["blue_l"]),
         path(f"M{x-29},{y} C{x-5},{y-23} {x+24},{y-20} {x+35},{y} C{x+24},{y+20} {x-5},{y+23} {x-29},{y} Z", C["blue"]),
         path(f"M{x-29},{y} L{x-49},{y-19} L{x-48},{y+19} Z", C["blue"]),
         circle(x+21, y-6, 3.5, C["white"]), line(x-3, y-17, x+4, y-31, C["blue"], 5)]
    return group("icon-food-fish", b)


def food_soy(x: float, y: float) -> str:
    b = [circle(x, y, 52, C["teal_l"]),
         path(f"M{x-30},{y+27} C{x-12},{y+4} {x+8},{y-13} {x+32},{y-29}", stroke=C["teal"], sw=5),
         path(f"M{x-18},{y+11} C{x-46},{y+4} {x-42},{y-24} {x-11},{y-15} Z", C["teal"]),
         path(f"M{x+5},{y-8} C{x+5},{y-38} {x+34},{y-43} {x+31},{y-12} Z", C["teal"]),
         circle(x+14, y+16, 11, C["amber_l"], C["amber"]), circle(x+35, y+7, 9, C["amber_l"], C["amber"])]
    return group("icon-food-soy", b)


def food_mushroom(x: float, y: float) -> str:
    b = [circle(x, y, 52, C["amber_l"]),
         path(f"M{x-40},{y} C{x-35},{y-42} {x+35},{y-42} {x+40},{y} Z", C["amber"]),
         rect(x-12, y-1, 24, 38, C["white"], 8, C["amber"], 3),
         circle(x-19, y-15, 4, C["white"]), circle(x+15, y-22, 5, C["white"])]
    return group("icon-food-mushroom", b)


def ferment_jar(x: float, y: float) -> str:
    b = [circle(x, y, 52, C["purple_l"]), rect(x-29, y-27, 58, 65, C["white"], 13, C["purple"], 3),
         rect(x-35, y-34, 70, 13, C["purple"], 6),
         path(f"M{x-20},{y+9} C{x-7},{y-1} {x+7},{y+18} {x+21},{y+5}", stroke=C["purple"], sw=4),
         circle(x-13, y-2, 4, C["purple_l"], C["purple"]), circle(x+14, y-5, 4, C["purple_l"], C["purple"])]
    return group("icon-fermentation", b)


def protein_chain(x: float, y: float) -> str:
    pts = [(x+i*33, y + off) for i, off in enumerate((0, -22, 13, -15, 17, -5, 12))]
    b = [path("M" + " L".join(f"{a},{b}" for a, b in pts), stroke=C["blue"], sw=5)]
    for i, (a, bb) in enumerate(pts):
        b.append(circle(a, bb, 12, [C["blue"], C["teal"], C["amber"]][i % 3], C["white"], 2))
    return group("icon-protein-chain", b)


def scissors(x: float, y: float) -> str:
    return group("icon-virtual-digestion", [circle(x-12, y+10, 10, C["white"], C["red"], 3), circle(x+12, y+10, 10, C["white"], C["red"], 3), line(x-5, y+2, x+28, y-28, C["red"], 4), line(x+5, y+2, x-28, y-28, C["red"], 4)])


def mass_spec(x: float, y: float) -> str:
    b = [rect(x-65, y-52, 130, 104, C["white"], 16, C["blue"], 3),
         rect(x-45, y-33, 58, 56, C["blue_l"], 7),
         line(x-35, y+13, x-35, y-2, C["blue"], 4), line(x-22, y+13, x-22, y-18, C["blue"], 4),
         line(x-9, y+13, x-9, y-9, C["blue"], 4), circle(x+38, y-17, 11, C["teal_l"], C["teal"], 3),
         circle(x+38, y+19, 11, C["amber_l"], C["amber"], 3)]
    return group("icon-lcms", b)


def database(x: float, y: float) -> str:
    b = [path(f"M{x-70},{y-35} L{x-70},{y+58} C{x-70},{y+78} {x+70},{y+78} {x+70},{y+58} L{x+70},{y-35}", C["teal_l"], C["teal"], 3),
         path(f"M{x-70},{y-35} C{x-70},{y-58} {x+70},{y-58} {x+70},{y-35} C{x+70},{y-12} {x-70},{y-12} {x-70},{y-35} Z", C["white"], C["teal"], 3),
         path(f"M{x-70},{y+10} C{x-70},{y+31} {x+70},{y+31} {x+70},{y+10}", stroke=C["teal"], sw=2),
         path(f"M{x-70},{y+45} C{x-70},{y+66} {x+70},{y+66} {x+70},{y+45}", stroke=C["teal"], sw=2)]
    return group("icon-peptide-database", b)


def feature_hex(x: float, y: float, label: str, color: str, gid: str) -> str:
    d = f"M{x-47},{y} L{x-24},{y-40} L{x+24},{y-40} L{x+47},{y} L{x+24},{y+40} L{x-24},{y+40} Z"
    return group(gid, [path(d, C["white"], color, 3), text(x, y+7, label, 18, 700, color, "middle")])


def neural_brain(x: float, y: float) -> str:
    nodes = [(x-48,y-28),(x-48,y+30),(x,y-52),(x,y),(x,y+52),(x+48,y-28),(x+48,y+30)]
    edges = [(0,2),(0,3),(1,3),(1,4),(2,5),(3,5),(3,6),(4,6),(2,3),(3,4)]
    b = [circle(x, y, 88, C["amber_l"], C["amber"], 4)]
    for a, bb in edges: b.append(line(*nodes[a], *nodes[bb], C["amber"], 2))
    for i,(a,bb) in enumerate(nodes): b.append(circle(a, bb, 9, C["white"], C["amber"], 3))
    b += [text(x, y+8, "AI", 25, 800, C["amber"], "middle")]
    return group("icon-ai-network", b)


def model_icon(x: float, y: float, label: str, kind: str, color: str, gid: str) -> str:
    b = [rect(x-58, y-44, 116, 88, C["white"], 15, color, 2)]
    if kind == "score":
        for i,w in enumerate((55,38,48)): b.append(line(x-35,y-18+i*14,x-35+w,y-18+i*14,color,3))
    elif kind == "tree":
        b += [line(x,y-22,x-26,y+5,color,3),line(x,y-22,x+26,y+5,color,3),line(x-26,y+5,x-39,y+25,color,3),line(x-26,y+5,x-12,y+25,color,3),circle(x,y-23,5,color),circle(x-39,y+25,5,color),circle(x-12,y+25,5,color),circle(x+26,y+5,5,color)]
    elif kind == "rnn":
        b += [path(f"M{x-40},{y+8} C{x-23},{y-25} {x-6},{y+35} {x+10},{y} C{x+24},{y-26} {x+34},{y+20} {x+43},{y-8}", stroke=color, sw=3)]
    else:
        for i in range(3):
            for j in range(3): b.append(circle(x-24+j*24,y-23+i*22,4+(i+j)%2*2,color))
    b.append(text(x, y+66, label, 17, 700, color, "middle"))
    return group(gid, b)


def funnel(x: float, y: float) -> str:
    b=[path(f"M{x-78},{y-55} L{x+78},{y-55} L{x+30},{y+8} L{x+12},{y+8} L{x+12},{y+65} L{x-12},{y+65} L{x-12},{y+8} L{x-30},{y+8} Z", C["purple_l"], C["purple"], 3)]
    for i, seq in enumerate(("DDE", "SHHPR", "EELR")): b.append(badge(x-105+i*72,y+78,66,seq,C["green_l"],C["green"]))
    return group("icon-consensus-ranking",b)


def receptor(x: float, y: float) -> str:
    b=[]
    for i in range(13):
        b += [circle(x-95+i*16,y-52,6,C["membrane"]),circle(x-95+i*16,y+52,6,C["membrane"])]
    b += [path(f"M{x-48},{y-100} C{x-78},{y-67} {x-62},{y-25} {x-26},{y-12} C{x-3},{y-5} {x-7},{y+27} {x-25},{y+82}", stroke=C["purple"], sw=13),
          path(f"M{x+48},{y-100} C{x+78},{y-67} {x+62},{y-25} {x+26},{y-12} C{x+3},{y-5} {x+7},{y+27} {x+25},{y+82}", stroke=C["teal"], sw=13),
          text(x-64,y-112,"T1R1",18,700,C["purple"],"middle"),text(x+64,y-112,"T1R3",18,700,C["teal"],"middle"),
          circle(x,y-33,10,C["amber"]),circle(x-15,y-43,7,C["red"]),circle(x+16,y-43,7,C["blue"]),
          line(x-15,y-43,x-34,y-67,C["red"],2,"4 4"),line(x+16,y-43,x+38,y-67,C["blue"],2,"4 4")]
    return group("icon-t1r1-t1r3-docking",b)


def vial(x: float, y: float) -> str:
    return group("icon-peptide-synthesis",[rect(x-20,y-33,40,67,C["blue_l"],9,C["blue"],3),rect(x-24,y-43,48,13,C["blue"],4),path(f"M{x-14},{y+10} C{x-3},{y} {x+5},{y+18} {x+16},{y+5}",stroke=C["teal"],sw=3)])


def tongue(x: float, y: float) -> str:
    return group("icon-sensory-tongue",[path(f"M{x-42},{y-35} C{x-45},{y+8} {x-31},{y+50} {x},{y+58} C{x+31},{y+50} {x+45},{y+8} {x+42},{y-35} C{x+18},{y-22} {x-18},{y-22} {x-42},{y-35} Z",C["red_l"],C["red"],3),line(x,y-18,x,y+38,C["red"],2),circle(x-18,y+2,3,C["red"]),circle(x+19,y+14,3,C["red"])])


def e_tongue(x: float, y: float) -> str:
    b=[rect(x-45,y-42,90,84,C["white"],13,C["purple"],3),rect(x-27,y-25,54,39,C["purple_l"],5)]
    for i,h in enumerate((12,25,18,31)): b.append(line(x-20+i*13,y+8,x-20+i*13,y+8-h,C["purple"],3))
    for dx in (-28,-9,10,29): b.append(line(x+dx,y+42,x+dx,y+55,C["purple"],2))
    return group("icon-electronic-tongue",b)


def food_bowl(x: float, y: float) -> str:
    return group("icon-food-matrix",[path(f"M{x-55},{y-5} C{x-47},{y+45} {x+47},{y+45} {x+55},{y-5} Z",C["green_l"],C["green"],3),line(x-60,y-5,x+60,y-5,C["green"],4),path(f"M{x-24},{y-18} C{x-40},{y-45} {x-8},{y-55} {x-18},{y-76}",stroke=C["amber"],sw=4),path(f"M{x+11},{y-18} C{x-5},{y-47} {x+28},{y-54} {x+18},{y-78}",stroke=C["amber"],sw=4)])


def build() -> str:
    s=['<?xml version="1.0" encoding="UTF-8"?>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#6B8495"/></marker><filter id="shadow"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#17324D" flood-opacity="0.12"/></filter></defs>',
       f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
    s += [group("title",[text(70,67,"机器学习如何加速鲜味肽发现？",42,800),text(70,105,"从食源候选生成、智能筛选到受体机制与真实感官证据",23,400,C["muted"]),badge(1515,48,215,"图形综述 · 2026",C["teal_l"],C["teal"])])]
    # Colored research landscapes, not card panels.
    s += [path("M35,155 C180,125 405,130 540,180 L540,905 C390,950 165,940 35,875 Z",C["blue_l"]),
          path("M570,180 C760,125 1085,125 1235,180 L1235,910 C1060,955 760,955 570,900 Z",C["amber_l"]),
          path("M1265,180 C1415,130 1635,125 1765,165 L1765,900 C1610,950 1410,950 1265,905 Z",C["green_l"]),
          group("zone-headings",[circle(83,180,26,C["blue"]),text(83,189,"1",24,800,C["white"],"middle"),text(122,190,"构建候选肽空间",29,800),
                                  circle(620,180,26,C["amber"]),text(620,189,"2",24,800,C["white"],"middle"),text(660,190,"AI 虚拟筛选与排序",29,800),
                                  circle(1315,180,26,C["green"]),text(1315,189,"3",24,800,C["white"],"middle"),text(1355,190,"机制解释与实验闭环",29,800)])]
    # Zone 1.
    s += [food_fish(105,290),food_soy(235,290),food_mushroom(365,290),ferment_jar(495,290),
          group("food-labels",[text(105,365,"水产",18,700,C["blue"],"middle"),text(235,365,"豆类",18,700,C["teal"],"middle"),text(365,365,"菌菇",18,700,C["amber"],"middle"),text(495,365,"发酵食品",18,700,C["purple"],"middle")]),
          path("M105,385 C155,420 200,420 240,430 M235,385 C240,410 250,420 265,430 M365,385 C335,415 320,420 300,430 M495,385 C430,420 385,425 330,435",stroke=C["line"],sw=2),
          protein_chain(150,455),scissors(405,455),
          group("peptide-fragments",[badge(105,523,64,"DDE",C["white"],C["blue"]),badge(180,523,74,"SHHPR",C["white"],C["teal"]),badge(265,523,62,"EELR",C["white"],C["amber"]),text(405,535,"虚拟酶解",18,700,C["red"],"middle")]),
          mass_spec(165,675),text(165,752,"LC–MS/MS 肽组学",20,700,C["blue"],"middle"),
          group("in-silico-source",[circle(405,675,62,C["white"],C["teal"],3),text(405,666,"in silico",19,800,C["teal"],"middle"),text(405,694,"酶解 / 宏基因组",17,600,C["teal"],"middle")]),
          path("M165,775 C230,830 335,830 405,755",stroke=C["blue"],sw=3,marker=True),
          badge(115,842,350,"多来源、去重、可追溯候选库",C["white"],C["blue"]) ]
    # Cross-zone stream and center.
    s += [path("M505,610 C560,610 570,430 625,430",stroke="#6B8495",sw=4,marker=True),database(685,335),
          group("db-label",[text(685,324,"鲜味 / 非鲜味",18,700,C["teal"],"middle"),text(685,352,"序列 + 标签",18,700,C["teal"],"middle"),text(685,443,"TastePeptidesDB · BIOPEP",15,600,C["muted"],"middle"),text(685,463,"+ 自建数据",15,600,C["muted"],"middle")]),
          feature_hex(875,300,"AAC",C["blue"],"feature-aac"),feature_hex(1000,300,"DPC",C["teal"],"feature-dpc"),feature_hex(1125,300,"CTD",C["purple"],"feature-ctd"),
          feature_hex(875,420,"理化",C["amber"],"feature-physchem"),feature_hex(1125,420,"BERT",C["red"],"feature-bert"),
          neural_brain(1000,540),
          path("M755,340 C835,350 885,470 915,500 M875,345 C900,420 935,450 950,470 M1000,345 L1000,445 M1125,345 C1100,420 1065,450 1050,470",stroke=C["line"],sw=2,marker=True),
          model_icon(700,700,"iUmami-SCM","score",C["blue"],"model-iumami-scm"),model_icon(850,700,"集成学习","tree",C["teal"],"model-ensemble"),model_icon(1000,700,"RNN / MLP","rnn",C["amber"],"model-rnn"),model_icon(1150,700,"Transformer","attn",C["purple"],"model-transformer"),
          path("M1000,630 L1000,640",stroke=C["amber"],sw=4,marker=True),
          path("M700,785 C770,835 855,835 915,835 M850,785 C885,810 910,820 935,830 M1000,785 L1000,815 M1150,785 C1105,815 1080,825 1060,835",stroke=C["line"],sw=2),
          funnel(1000,855),text(1000,975,"共识概率 · 校准 · SHAP · 适用域",19,700,C["purple"],"middle")]
    # Zone 3: receptor and validations.
    s += [path("M1085,915 C1205,920 1240,520 1310,520",stroke="#6B8495",sw=4,marker=True),
          receptor(1435,365),text(1435,510,"T1R1/T1R3 结合与构象稳定性",20,700,C["purple"],"middle"),
          group("mechanism-tags",[badge(1300,545,90,"氢键",C["white"],C["blue"]),badge(1400,545,90,"静电",C["white"],C["red"]),badge(1500,545,90,"疏水",C["white"],C["teal"]),badge(1595,545,125,"MD/MM-GBSA",C["white"],C["purple"])]),
          path("M1435,580 C1435,615 1360,620 1345,660 M1435,580 C1435,615 1495,625 1510,660 M1510,580 C1580,615 1640,620 1660,660",stroke=C["line"],sw=2,marker=True),
          vial(1335,710),tongue(1455,710),e_tongue(1575,710),food_bowl(1690,715),
          group("validation-labels",[text(1335,790,"合成与纯度",17,700,C["blue"],"middle"),text(1455,790,"盲法感官阈值",17,700,C["red"],"middle"),text(1575,790,"电子舌 / SPR",17,700,C["purple"],"middle"),text(1690,790,"食品基质验证",17,700,C["green"],"middle")]),
          rect(1310,835,405,70,C["white"],35,C["green"],3),text(1512,866,"最终判据：真实感官效应",23,800,C["green"],"middle"),text(1512,891,"预测与对接仅用于优先级排序",17,600,C["red"],"middle")]
    # Bottom evidence rail and active-learning feedback.
    s += [group("evidence-rail",[text(70,1005,"证据强度",21,800),path("M180,995 L1650,995",stroke=C["line"],sw=5,marker=True),
          circle(375,995,10,C["blue"]),circle(850,995,10,C["amber"]),circle(1300,995,10,C["purple"]),circle(1620,995,10,C["green"]),
          text(375,1030,"候选",17,700,C["blue"],"middle"),text(850,1030,"模型",17,700,C["amber"],"middle"),text(1300,1030,"机制",17,700,C["purple"],"middle"),text(1620,1030,"实证",17,700,C["green"],"middle")]),
          group("active-learning-loop",[path("M1660,930 C1680,1135 405,1145 245,930",stroke=C["teal"],sw=4,marker=True,dash="10 8"),rect(620,1083,570,55,C["teal_l"],28,C["teal"],2),text(905,1118,"主动学习：实验标签回流 → 数据更新 → 模型再训练",21,800,C["teal"],"middle")]),
          group("footer",[text(70,1170,"质量控制：同源聚类划分 · 外部测试 · MCC/AUPRC · 防止数据泄漏 · 对接分数不等于鲜味阈值",18,600,C["muted"]),text(1730,1170,"文献综合 [1–7]  ·  CC BY 4.0",17,600,C["muted"],"end")])]
    s.append("</svg>")
    return "\n".join(s)


def main() -> None:
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
