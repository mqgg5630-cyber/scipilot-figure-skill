---
name: scipilot-figure-skill
description: >-
 SciPilot Skills 家族成员，负责科研数据图绘制——生成期刊投稿级别的折线图、
 柱状图、散点图、箱线图/小提琴图、热力图、误差棒图、回归图以及多面板组合图。
 支持 Nature / Science / IEEE / Elsevier / PNAS / 中文核心期刊的硬性规范
 （单/双栏宽度、字号、DPI、矢量格式偏好），技术栈是 matplotlib + seaborn +
 SciencePlots（静态）和 plotly（交互）。中英文双语支持，中文模式按优先级
 自动配置 Noto Sans CJK / Source Han Sans / SimHei / Microsoft YaHei
 并修复负号方框问题，可按中文期刊"宋体正文 + Times New Roman 数字"约定混排。
 默认色盲安全配色（Okabe-Ito / seaborn colorblind）+ 冗余编码（不同线型/标记）。
 当用户的任务涉及以下任何情况时主动触发：论文配图、科研画图、期刊投稿图、
 figure、出版级图表、matplotlib 画图、seaborn 画图、plotly 交互图、
 误差棒、显著性标注、色盲安全配色、矢量图导出（PDF/SVG/EPS）、
 中文论文图表、双栏图、子图布局、figure for paper、publication-ready figure、
 journal figure、Nature 风格图、scientific visualization。**即使用户没有
 明确说"用本技能"，只要任务是给学术论文、毕业论文、会议投稿产出数据图，
 都应该调用本技能。** 不做示意图、流程图、架构图——那些不在覆盖范围内。
---

# scipilot-figure-skill — 科研数据图绘制

> SciPilot Skills 家族成员 | 负责科研数据图绘制

## 概述

本技能给学术论文产出**期刊投稿级别**的数据图。技术栈：matplotlib + seaborn + SciencePlots（静态图）+ plotly（交互图）。覆盖**纯数据图**：折线、柱状、散点、箱线/小提琴、热力、误差棒、回归，以及它们的多面板组合。

**不做**：示意图、流程图、架构图、概念图——那是另一类工具的活，本技能不碰。

## 何时使用

满足以下任一情况就该调用：

- 用户在写论文/毕业论文/会议投稿，需要数据图
- 用户提到 Nature/Science/IEEE/Elsevier/PNAS/CCF 等期刊的图表要求
- 用户给了一份数据（CSV/JSON/numpy/pandas）让你出图
- 用户已有一张草图但要"改到合规"（尺寸不对、像素不够、字太小、JPEG 不能投稿等）
- 用户问"中文论文怎么画 matplotlib 图不出方框"
- 用户提到误差棒、显著性标注、配色色盲安全、矢量导出、双栏排版、子图标签

## 工作流程

### Step 0：开画前必须先问清四件事

**不获得这四个答案，不进入下一步。**

1. **目标期刊或使用场景**：Nature？IEEE？中文期刊？毕业论文？答案决定栏宽、字号、字体、DPI。
2. **图类型**：折线 / 柱状 / 散点 / 箱线 / 小提琴 / 热力 / 误差棒 / 多面板。一次画几张？
3. **中英文**：中文图还是英文图？中文图要不要走"宋体 + Times New Roman"混排？
4. **数据来源**：用户提供的文件路径？粘贴的数据？还是 LLM 用合成数据示意？合成数据出图必须显式告知用户"这是占位演示，不是你的真实数据"。

收齐后向用户**口头复述参数**：
> 我将画 **2 张柱状图 + 1 张折线图**，目标 **IEEE 单栏 3.5 in**、英文、
> DPI 600、PDF + PNG 双格式导出。数据来自 `results.csv`。开始？

### Step 1：读规范（按需 view，不要一次全读）

- 不知道目标期刊的栏宽/字号 → 查 `references/journal_specs.md`
- 不知道这种图怎么画 → 查 `references/plot_recipes.md`
- 不知道投稿前还要检查啥 → 查 `references/publication_checklist.md`

### Step 2：配环境

调用 `scripts/setup_style.py` 的 `setup_style(journal=..., lang=..., serif_for_zh=...)`。

```python
from setup_style import setup_style
# Nature 单栏英文
setup_style(journal='nature', lang='en')
# 中文期刊（宋体 + Times New Roman 混排）
setup_style(journal='general', lang='zh', serif_for_zh=True)
```

SciencePlots 装了就自动用，没装就回退到内置等效预设，**不会因为缺它崩溃**。

### Step 3：画图

按 `references/plot_recipes.md` 里对应章节的配方画。

**画图时强制做到**：
- `figsize=(目标宽, 目标高)` 单位英寸——直接设最终尺寸
- 用 `seaborn.color_palette('colorblind')` 或 Okabe-Ito，加冗余编码（不同 marker/linestyle）
- 误差棒/阴影必有图注说明（SD/SEM/95%CI + n）
- 不要在 Word/PPT 里再缩放

### Step 4：导出

调用 `scripts/export_figure.py` 的 `export_figure(...)`。

```python
from export_figure import export_figure
export_figure(
    fig, basename='figs/fig1_main',
    formats=['pdf', 'svg', 'png'],  # 矢量优先，PNG 备一份给 Word 嵌
    size_inches=(3.5, 2.625),       # 单栏 Nature
    dpi=600,                        # 位图分辨率
    grayscale_preview=True,         # 加一张灰度图做色盲检查
)
```

- 数据图禁用 JPEG（有损压缩）
- 矢量首选 PDF/SVG/EPS（线/柱/散点）
- 显微图/照片才用 TIFF/PNG（300-600 DPI）

### Step 5：自检

调用 `scripts/check_figure.py`。

```python
python scripts/check_figure.py figs/*.pdf figs/*.png --min-dpi 300 \
       --width-in 3.5 --height-in 2.625 --strict
```

任意 FAIL 即重新画图 → 不交付。逐条对照 `references/publication_checklist.md` 勾选。

## 五条硬性原则

### 原则 1：按最终尺寸出图，不二次缩放

`figsize` 直接设论文里实际尺寸（Nature 单栏 3.5 in、双栏 7.2 in；IEEE 单栏 3.5 in、双栏 7.16 in）。导出后**绝不在 Word/LaTeX 里 width=0.5\textwidth 这样再缩**。

**为什么重要**：matplotlib 的字号、线宽、marker 大小都是**绝对单位**（pt、inch），你在 Word 里缩 50%，9 pt 字立刻变 4.5 pt——投稿前自检通不过、审稿编辑直接退回。

### 原则 2：矢量优先

折线、柱状、散点、热力（数据网格除外）、误差棒——都导出 PDF / SVG / EPS。显微图、照片、栅格化的复杂图层才用 TIFF/PNG（300-600 DPI）。**绝对不用 JPEG**。

**为什么重要**：矢量在任何缩放下都不糊，文字仍可选；位图放大就糊；JPEG 还有压缩 artifact，期刊 PDF 检查器会直接打回。

### 原则 3：配色对色盲友好

默认用 `seaborn.color_palette('colorblind')` 或 Okabe-Ito（红蓝绿黄紫青棕橙）。**同一张图里不同类别加冗余编码**——不同线型（`-` / `--` / `:`）、不同 marker（`o` / `s` / `^`）。出图前导出灰度版本检查（`export_figure` 的 `grayscale_preview=True`）。

**为什么重要**：约 8% 的男性、0.5% 的女性是色觉异常。一张全靠红绿区分的图对他们完全无法读。审稿人里有色觉异常的，你的图传达力直接归零。

### 原则 4：字号在最终尺寸下可读

正文标签和刻度数字 **7-9 pt**，最小字（如颜色条标注、显著性符号）不小于 **6 pt**。**判断标准是最终尺寸**——你 figsize 设 3.5 in、字号 8 pt，导出后字就是 8 pt；你 figsize 设 10 in、字号 8 pt，导出后被压回 3.5 in 字就是 2.8 pt——糊得没法读。

**为什么重要**：审稿编辑打印出来用尺量字号，<6 pt 直接退回。

### 原则 5：误差必有交代

只要图里出现误差棒、阴影置信区间、箱线图——**图注必须说清**：
- 误差代表什么？SD（标准差）/ SEM（标准误）/ 95% CI（置信区间）/ IQR（四分位距）？
- 样本量 n 是多少？
- 显著性怎么计算的？t-test / Mann-Whitney / ANOVA？校正了吗？

**为什么重要**：SD 和 SEM 差一个根号 n，混淆会让结论彻底反转。审稿人对没写清楚的误差直接判低分。

## 中文支持

中文 matplotlib 出方框的根本原因：默认字体（DejaVu Sans 等）不含 CJK 字符表。`setup_style(lang='zh')` 自动做这两件事：

1. **按优先级查中文字体**：`Noto Sans CJK SC` → `Source Han Sans SC` → `SimHei` → `Microsoft YaHei` → ... 找到第一个可用的就用。
2. **修负号方框**：`plt.rcParams['axes.unicode_minus'] = False`。

如果找不到任何 CJK 字体，会抛出清晰的安装提示（不会让你画完图发现是方框）：
```
Linux:   sudo apt install fonts-noto-cjk
macOS:   brew install --cask font-noto-sans-cjk-sc
Windows: https://github.com/notofonts/noto-cjk/releases 下载安装
```

**中文期刊的"宋体 + 数字 Times New Roman"混排**：传 `serif_for_zh=True`，会优先选 Noto Serif CJK / Source Han Serif / SimSun，西文回退到 Times。

详见 `references/journal_specs.md` 末尾的中文字体安装与中文期刊规范小节。

## 脚本说明

三个脚本都在 `scripts/` 下，按需 view：

| 脚本 | 干啥 | 主入口 |
|---|---|---|
| `setup_style.py` | 应用出版级样式预设；中文字体配置；SciencePlots 包装 | `setup_style(journal, lang, use_sciplots, serif_for_zh)` |
| `export_figure.py` | 统一导出多格式 + 按最终尺寸 + 灰度预览 | `export_figure(fig, basename, formats, dpi, size_inches, grayscale_preview)` |
| `check_figure.py` | 已有图合规自检（格式 / DPI / 字体嵌入） | `check_figure(path, min_dpi, target_inches)` |

## 参考文档说明

`references/` 下三份大文档，**按需 view，不要一次全读**：

| 文档 | 何时读 |
|---|---|
| `journal_specs.md` | 不确定目标期刊的栏宽 / 字号 / DPI / 字体要求 |
| `plot_recipes.md` | 七类图各自的完整配方代码 + 适用场景 + 坑 |
| `publication_checklist.md` | 投稿前最后过一遍合规清单 |

每份文件开头都有目录——先看目录定位，再 view 对应小节。

## 常见任务示例

### 任务 1：投稿级折线图（Nature 单栏英文）

```python
from setup_style import setup_style
from export_figure import export_figure
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

setup_style(journal='nature', lang='en')

# Nature 单栏直接 figsize=(3.5, 2.625)
fig, ax = plt.subplots(figsize=(3.5, 2.625))
x = np.linspace(0, 10, 100)
y = np.sin(x); err = 0.1 * np.ones_like(x)

palette = sns.color_palette('colorblind')
ax.plot(x, y, color=palette[0], linewidth=1.0, label='Condition A')
ax.fill_between(x, y - err, y + err, color=palette[0], alpha=0.2)

ax.set_xlabel('Time (s)'); ax.set_ylabel('Response (a.u.)')
ax.legend(frameon=False, loc='lower right')

export_figure(fig, 'figs/fig1', formats=['pdf', 'svg', 'png'],
              size_inches=(3.5, 2.625), dpi=300, grayscale_preview=True)
# 图注里务必写: shaded band = SD across n=12 mice.
```

### 任务 2：把"草图"改到合规

用户给一张 600×400 px 的 PNG，字模糊、JPEG 压缩 artifact、Excel 默认色。流程：

1. 跑 `check_figure(...)` 列出全部问题
2. 拿到原始数据后**重画**——不要试图 PS 后期补救
3. `setup_style()` 给一套合规预设
4. 重新 `export_figure()` 矢量 + 位图都出一份
5. 再跑 `check_figure --strict` 直到 PASS

### 任务 3：多面板组合图（2×2 子图）

```python
fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.4),     # 双栏 Nature
                         constrained_layout=True)
for ax, label in zip(axes.flat, ['a', 'b', 'c', 'd']):
    # 子图内容...
    ax.text(-0.18, 1.05, label, transform=ax.transAxes,
            fontsize=9, fontweight='bold', va='top')
# 4 个子图字号、配色保持一致——配方见 plot_recipes.md "多面板组合"小节
```

### 任务 4：带显著性标注的统计图

箱线图 + stripplot 显示原始点 + 显著性桥（horizontal bracket with *）。配方见 `plot_recipes.md` 第 4 节。**必须在图注里写清**：误差类型、n、检验方法、p 值。

## 依赖

```
matplotlib>=3.7
seaborn>=0.13
plotly>=5.18
Pillow>=10.0       # check_figure / grayscale preview
SciencePlots>=2.1  # 可选；装了样式更接近期刊
pypdf>=4.0         # 可选；check_figure 字体嵌入检查
```

`SciencePlots` 和 `pypdf` 都是可选，缺失时本技能仍能跑——会优雅降级并提示用户。
