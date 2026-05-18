# scipilot-figure-skill

> SciPilot Skills family. Publication-grade scientific figure copilot.
> SciPilot Skills 家族成员 — 期刊投稿级科研数据图副驾驶。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)](#dependencies--依赖)
[![Status: v1.0.0](https://img.shields.io/badge/Status-v1.0.0-success.svg)](#)
[![Stack](https://img.shields.io/badge/Stack-matplotlib%20%7C%20seaborn%20%7C%20plotly-orange.svg)](#)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://claude.com/claude-code)

A [Claude Code](https://claude.com/claude-code) / [Codex](https://github.com/openai/codex) / Cursor Skill that **draws publication-grade scientific figures**—line, bar, scatter, box/violin, heatmap, error-bar, regression, multi-panel composites—at exact final size for Nature / Science / IEEE / Elsevier / PNAS / Chinese journals. Built on **matplotlib + seaborn + SciencePlots** (static) and **plotly** (interactive), with **CJK font auto-configuration** so Chinese text never renders as boxes.

> [中文文档](#中文文档) | [English](#english)

---

## 中文文档

### 概览

`scipilot-figure-skill` 是 SciPilot Skills 家族第二个成员，专做**期刊投稿级科研数据图**。技术栈：

- **静态图**：matplotlib + seaborn + SciencePlots（可选增强）
- **交互图**：plotly
- **覆盖范围**：折线、柱状、散点、箱线/小提琴、热力、误差棒、回归、多面板组合
- **不做**：示意图、流程图、架构图（那是另一类工具的活）

支持的期刊预设：**Nature / Science / IEEE / Elsevier / PNAS / 中文核心期刊**。中英文双语，中文模式自动配置 Noto Sans CJK / Source Han Sans / SimHei / Microsoft YaHei 并修复负号方框。

### 五条硬性原则

1. **按最终尺寸出图，不二次缩放** — `figsize=(3.5, 2.625)` 直接定 Nature 单栏
2. **矢量优先** — 数据图必走 PDF / SVG / EPS；照片才用 TIFF/PNG；**绝不 JPEG**
3. **配色对色盲友好** — 默认 Okabe-Ito，加冗余编码（不同线型/marker），出图前查灰度
4. **字号在最终尺寸下可读** — 7–9 pt 正文，最小 6 pt
5. **误差必有交代** — 图注必须写清 SD/SEM/95%CI + n + 检验方法

### 安装

**方式 A：让 Claude Code / Codex 自己装（推荐）**

```
请帮我安装这个 Skill：https://github.com/Haojae/scipilot-figure-skill.git
```

**方式 B：手动 clone**

```bash
git clone https://github.com/Haojae/scipilot-figure-skill.git \
          ~/.claude/skills/scipilot-figure-skill
pip install -r ~/.claude/skills/scipilot-figure-skill/requirements.txt
```

**方式 C：下载 ZIP**

1. GitHub 页面点 `Code` → `Download ZIP`
2. 解压到 `~/.claude/skills/scipilot-figure-skill/`
3. `pip install -r requirements.txt`

`SciencePlots` 和 `pypdf` 是可选增强，缺失时不影响运行。

### 中文支持

中文 matplotlib 出方框的根本原因：默认字体不含 CJK 字符表。`setup_style(lang='zh')` 自动按优先级查找：

```
Noto Sans CJK SC > Source Han Sans SC > SimHei > Microsoft YaHei
```

找不到任何 CJK 字体时抛出清晰的安装提示（不会让你画完图发现是方框）。中文期刊的"宋体 + Times New Roman 数字"混排：传 `serif_for_zh=True`。

### 使用示例

启动 Claude Code 直接用自然语言：

```
帮我画一张 Nature 单栏的折线图，x 是时间 0-10 秒，
y 是两条对照曲线带 SEM 阴影，色盲安全配色，
导出 PDF + PNG，DPI 300。
```

```
我有这个 results.csv，3 组 × 2 条件 × 10 次重复，
画带误差棒的分组柱状图，叠加 stripplot 显示原始点，
IEEE 双栏格式，要求黑白可读。
```

```
帮我把这张 Excel 截的散点图改造成投稿级——600×400 PNG，
要变成 Nature 投稿规格，中文期刊宋体混排。
```

Skill 在 Step 0 强制问清四件事（**期刊/场景 + 图类型 + 中英文 + 数据来源**），收齐确认后才进入"读规范 → 配环境 → 画图 → 导出 → 自检"五步流程。

### 命令行直接调脚本

```bash
# 列出可用 CJK 字体
python scripts/setup_style.py --list-fonts

# 跑一张演示图导出 PDF/SVG/PNG + 灰度预览
python scripts/export_figure.py demo --out ./test_demo

# 合规自检
python scripts/check_figure.py figs/*.pdf figs/*.png \
       --min-dpi 300 --width-in 3.5 --height-in 2.625 --strict
```

### SciPilot Skills 家族

| Skill | 状态 | 功能 |
|---|---|---|
| scipilot-cite-skill | [v1.0.0](https://github.com/Haojae/scipilot-cite-skill) | 文献检索与引用插入 |
| **scipilot-figure-skill** | **v1.0.0 (本仓库)** | **科研数据图绘制** |
| scipilot-polish-skill | 规划中 | 学术论文润色 |
| scipilot-review-skill | 规划中 | AI 模拟审稿 |
| scipilot-submit-skill | 规划中 | 投稿格式适配 |
| scipilot-read-skill | 规划中 | 论文阅读与翻译 |

### 许可证

[MIT](LICENSE) © 2026 Haojae

---

## English

### Overview

`scipilot-figure-skill` is the second member of the SciPilot Skills family, focused on **publication-grade scientific figures**. Stack:

- **Static**: matplotlib + seaborn + SciencePlots (optional enhancement)
- **Interactive**: plotly
- **Coverage**: line, bar, scatter, box / violin, heatmap, error-bar, regression, multi-panel composites
- **Out of scope**: schematics, flowcharts, architecture diagrams

Journal presets: **Nature / Science / IEEE / Elsevier / PNAS / Chinese journals**. Bilingual support — Chinese mode auto-configures Noto Sans CJK / Source Han Sans / SimHei / Microsoft YaHei and fixes the unicode-minus square-box bug.

### Five hard rules

1. **Render at final size, never rescale** — set `figsize=(3.5, 2.625)` directly for a Nature single column
2. **Vectors first** — data figures must be PDF / SVG / EPS; only photographs may be TIFF/PNG; **never JPEG**
3. **Colorblind-safe palette** — default Okabe-Ito with redundant encoding (line styles / markers), grayscale-check before submission
4. **Readable type at final size** — 7–9 pt body, 6 pt minimum
5. **Error must be explained** — captions must declare SD/SEM/95% CI, n, and test type

### Installation

**Option A: let Claude Code / Codex install it (recommended)**

```
Please install this Skill for me: https://github.com/Haojae/scipilot-figure-skill.git
```

**Option B: manual clone**

```bash
git clone https://github.com/Haojae/scipilot-figure-skill.git \
          ~/.claude/skills/scipilot-figure-skill
pip install -r ~/.claude/skills/scipilot-figure-skill/requirements.txt
```

**Option C: download ZIP**

1. GitHub page → `Code` → `Download ZIP`
2. Extract into `~/.claude/skills/scipilot-figure-skill/`
3. `pip install -r requirements.txt`

`SciencePlots` and `pypdf` are optional enhancements; the skill degrades gracefully if either is missing.

### Chinese support

The reason Chinese characters render as boxes in matplotlib by default is that the fallback font (DejaVu Sans, etc.) ships without CJK glyphs. `setup_style(lang='zh')` automatically scans in priority order:

```
Noto Sans CJK SC > Source Han Sans SC > SimHei > Microsoft YaHei
```

If no CJK font is found, the skill raises a clear install hint instead of silently emitting boxes. For Chinese journals that require the "Songti body + Times New Roman digits" convention, pass `serif_for_zh=True`.

### Usage examples

Just speak naturally inside Claude Code:

```
Draw a Nature single-column line plot, x is time 0-10 s, y is two
conditions with SEM shading. Use a colorblind palette. Export PDF and
PNG at 300 DPI.
```

```
I have results.csv (3 groups × 2 conditions × 10 replicates).
Make a grouped bar plot with error bars, overlay stripplot for raw
points, IEEE double-column format, must read in grayscale.
```

```
Help me convert this Excel scatter screenshot (600×400 PNG) into a
Nature submission-ready figure, with Chinese Songti + Times New Roman
mixed font.
```

The skill enforces a 4-question Step 0 (**journal / figure type / language / data source**), then walks the user through "read spec → configure → plot → export → audit".

### Command-line scripts

```bash
# List available CJK fonts
python scripts/setup_style.py --list-fonts

# Demo: render a sample figure and export in multiple formats + grayscale
python scripts/export_figure.py demo --out ./test_demo

# Pre-submission compliance audit
python scripts/check_figure.py figs/*.pdf figs/*.png \
       --min-dpi 300 --width-in 3.5 --height-in 2.625 --strict
```

### SciPilot Skills family

| Skill | Status | Purpose |
|---|---|---|
| scipilot-cite-skill | [v1.0.0](https://github.com/Haojae/scipilot-cite-skill) | Reference discovery & insertion |
| **scipilot-figure-skill** | **v1.0.0 (this repo)** | **Scientific figure plotting** |
| scipilot-polish-skill | Planned | Academic prose polishing |
| scipilot-review-skill | Planned | AI peer-review simulation |
| scipilot-submit-skill | Planned | Submission formatting |
| scipilot-read-skill | Planned | Paper reading & translation |

### License

[MIT](LICENSE) © 2026 Haojae

### Dependencies

```
matplotlib>=3.7
seaborn>=0.13
plotly>=5.18
Pillow>=10.0
SciencePlots>=2.1   # optional
pypdf>=4.0          # optional
kaleido>=0.2.1      # optional, for plotly static export
```

Python 3.9+ recommended.
