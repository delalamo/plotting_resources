> Historical guide. R1 on S3 is now selected; see [the current guide](README.md).

# Style guide: B / light cream

**Approved style:** option **B**, light cream **`#FAF6EE`**, with **Helvetica Regular**, muted teal and earth-tone colors, and **0.55 pt black borders** on all four sides of every plot panel. This is the default for future figures. The code settings in [minimal_theme.py](minimal_theme.py) implement the specifications below.

Six code-generated examples from [Chen Liu's figures4papers README](https://github.com/ChenLiu-1996/figures4papers), using its original data and drawing functions. The sphere example and manually assembled composites are excluded as requested.

[Open the before/after gallery](gallery.html) · [All six figures, PDF](gallery-beige.pdf) · [Overview](overview.png)

[Explore five researched color-identity proposals](palette-study/gallery.html) · [Research, palette definitions and usage rules](palette-study/README.md). These are candidates on the same B background and Helvetica style; the approved palette above remains the default.

[Explore eight complete plotting styles](full-style-study/gallery.html) · [Background, line-weight, grid and marker comparisons](full-style-study/style-exploration.pdf). This wider study keeps Helvetica typography fixed and varies the remaining visual settings.

[Latest S3 exploration: five mixed warm/cool palettes](s3-design-study/gallery.html) · [Design research and exact colors](s3-design-study/README.md) · [Comparison sheet](s3-design-study/s3-design-palettes.pdf). These R1–R5 proposals use the preferred S3 light blue panel (`#EBF1F5`) with more varied accents, based on actual design precedents. All other S3 settings stay fixed; no replacement palette has been selected.

[Earlier cool-only S3 study](s3-cool-study/gallery.html). C1–C5 were rejected as too cool and homogeneous; retained as historical comparisons.

[Compare five beige options A–E](beige-options/gallery.html) · [Shade comparison sheet](beige-options/comparison.pdf). **B is selected**; C (`#F7F2E8`) is the earlier background. The alternatives are retained for reference. Only the background varies across those proofs. Regenerate this separate comparison with `python figures4papers-minimal/render_beige_options.py`.

## Implementation

Keep Matplotlib and the upstream data; separate presentation into [minimal_theme.py](minimal_theme.py). The source scripts mix data, geometry, and hard-coded styling, so setting `rcParams` alone is insufficient. [render_examples.py](render_examples.py) replaces the quantitative plotting sections with small adapters and normalizes the native artists in the manifold drawing. It does not alter the original source snapshot.

Keep the typography of [cowplot's minimal grid themes](https://wilkelab.org/cowplot/reference/theme_minimal_grid.html), with light cream plot panels (`#FAF6EE`), thin black frames on all four sides, and the exact palettes below. Figure margins are white (`#FFFFFF`). The radar uses a rectangular frame around the radial plot and its spoke labels; the manifold drawing also has a framed light cream panel. Tick marks remain hidden and legends remain frameless. Horizontal grids suit these bar and line examples; the radar keeps its radial guides, while the manifold has none.

## Typography and physical sizes

Use **Helvetica**, **regular / normal weight**, for axis labels, tick labels, legends, titles, and annotations. Use **Arial → Liberation Sans → DejaVu Sans**, in that order, only when Helvetica is unavailable. The checked exports use Helvetica. Mathematical notation uses Matplotlib's **DejaVu Sans math font**, with italic variables; no external LaTeX installation is needed. Keep text charcoal (`#282828`) and secondary annotations gray (`#666666`).

| Element | Setting at export size |
|---|---|
| Font | Helvetica Regular; fallbacks: Arial → Liberation Sans → DejaVu Sans |
| Axis labels | 10 pt, regular |
| Tick labels and legends | 8.57 pt (`base × 12/14`) |
| Panel titles | 11.43 pt (`base × 16/14`), regular |
| Data curves | 1.15 pt, approximately 0.41 mm |
| Error bars | 0.65 pt; 2 pt caps |
| Plot background | B / light cream `#FAF6EE`, fully opaque |
| Figure background / margins | White `#FFFFFF`, fully opaque |
| Plot border | 0.55 pt black `#000000`, all four sides |
| Major grids | 0.45 pt, approximately 0.16 mm; warm gray `#E3DCCF` |
| Bar / hatch outlines | 0.4 pt; no outlines on comparison bars |
| Markers | 3.5 pt diameter on line charts |
| Export | 300 dpi PNG, PDF with embedded fonts, SVG with editable text |

This is an intentionally lighter adaptation, not a literal port of cowplot's default 14 pt text and 0.5 mm grid. The font ratios follow cowplot. Fonts and strokes are specified in points; canvas size is specified in inches. Re-render at the intended publication size instead of shrinking an exported figure and making every label smaller. Dense annotations use 6.7–8 pt, and diagram annotations use 7.5–10 pt.

## Exact colors

Use these hexadecimal sRGB colors. Keep a category's assigned color consistent across panels and figures; the order in `PALETTES` is meaningful. Set opacity separately from the base color.

| Role | Color | Hex |
|---|---|---|
| Plot panel and annotation backing | Light cream B | `#FAF6EE` |
| Figure margins | White | `#FFFFFF` |
| Panel border | Black | `#000000` |
| Primary text and error bars | Charcoal | `#282828` |
| Secondary text / annotations | Gray | `#666666` |
| Major grid lines | Warm gray | `#E3DCCF` |
| Reference / SFT baseline | Medium gray | `#888888` |
| Hatch lines and composition outlines | Gray | `#707070` |
| Primary series / visual conditioning | Teal | `#246C68` |
| Comparison series / blind conditioning | Terracotta | `#B2674D` |
| Third series | Ochre | `#9B8644` |
| Prior / textual manifold | Taupe | `#8C8275` |
| Multimodal scatter accent | Soft teal | `#3C8176` |

### Three-method palette: line and radar figures

`PALETTES["methods"]`, in this order:

| Method | Color | Hex |
|---|---|---|
| DPO | Terracotta | `#B2674D` |
| DA-DPO | Ochre | `#9B8644` |
| VIGIL (Ours) | Teal | `#246C68` |

### Nine-method palette: quantitative bars

`PALETTES["comparison"]`, in this order:

| Method | Color | Hex |
|---|---|---|
| Prime-2.1 | Stone | `#8F857A` |
| NetMHCpan | Honey | `#C3A35A` |
| MHCnuggets | Clay pink | `#CB907B` |
| MHCflurry | Mauve | `#A08397` |
| DeepNeo | Burnt sienna | `#B66B4C` |
| BigMHC-EL | Sage | `#9BAA85` |
| BigMHC-IM | Olive | `#778958` |
| BigMHC retrained | Slate blue | `#54788D` |
| ImmunoStruct (ours) | Teal | `#246C68` |

### Seven-method palette: composition bars

`PALETTES["composition"]`, in this order:

| Method | Color | Hex |
|---|---|---|
| DeepSeek R1 Distill Qwen 1.5B | Mist teal | `#8EA6A0` |
| DeepSeek R1 Distill Qwen 14B | Sage teal | `#5D8E83` |
| DeepSeek R1 Distill Llama 70B | Deep teal | `#316E65` |
| deepseek-chat (Deepseek-V3) | Soft clay | `#C58E76` |
| deepseek-reasoner (Deepseek-R1) | Rust | `#A65E45` |
| gemini-2.5-flash-preview-04-17 | Antique gold | `#B2954F` |
| OpenAI o3 | Slate blue | `#345D78` |

For publication trends, use terracotta `#B2674D` for evaluation/application and teal `#246C68` for methodological contribution, with fill alpha **0.28** and **0.40**, respectively. Use opaque data curves. Radar fills use alpha **0.035**; conceptual distribution fills use **0.10**. In composition plots, the first segment is opaque and the other segments use **0.80**. The background and black frame remain fully opaque throughout.

## Examples

| README example | Restyled output | Upstream source |
|---|---|---|
| Quantitative bars | [PNG](figures/bars_comparison_IEDB.png) · [SVG](figures/bars_comparison_IEDB.svg) | `figure_ImmunoStruct/plot_bars.py` + `raw_data.py` |
| Composition bars | [PNG](figures/brute_force.png) · [SVG](figures/brute_force.svg) | `figure_Brainteaser/plot_brute_force.py` |
| Radar | [PNG](figures/comparison_radar.png) · [SVG](figures/comparison_radar.svg) | `figure_VIGIL/plot_comparison_radar.py` |
| Line plot | [PNG](figures/comparison_posttraining.png) · [SVG](figures/comparison_posttraining.svg) | `figure_VIGIL/plot_posttraining.py` |
| Concept plots | [PNG](figures/concept.png) · [SVG](figures/concept.svg) | `figure_VIGIL/plot_concept.py` |
| Trends | [PNG](figures/trend_by_month.png) · [SVG](figures/trend_by_month.svg) | `figure_ophthal_review/plot_trend.py` |

Each also has an individual PDF in `figures/`. All six examples retain native vector plot elements in PDF and SVG. `gallery.pdf` is refreshed with the same contents as `gallery-beige.pdf`; stale sphere exports have been removed. The untouched upstream snapshot remains available for provenance. SVG text requires the selected font on the receiving computer; the PDFs embed fonts.

## What is preserved, and what changes

- All quantitative arrays, method ordering, composition categories, and original uncertainty values are preserved. `data.json` exports those exact arrays and retains the original source color metadata; the active palette is separately defined in `minimal_theme.py` and recorded in `render-info.json`. The upstream field named `std` mixes supplied values with `/sqrt(5)` adjustments for PPVn; this adaptation does not reinterpret it as a uniform confidence interval.
- Comparison bars retain the source's truncated y ranges for visual comparability. For future scientific use, consider zero-based bars or point-and-interval plots instead.
- Composition keeps all eight panels, seven methods, four hatch categories, and 56 numeric labels. Text halos are replaced with small beige-backed labels at the first-segment boundaries; math and logic rows are named explicitly. Totals are not renormalized when source rounding gives 0.999 or 1.001.
- Radar values retain the original per-benchmark radial mapping: POPE 75–91, MathVista 30–61, MMBench 40–85. These scales are not interchangeable across spokes.
- Post-training curves retain every vertex and the SFT baseline; uniform line opacity replaces the decorative gradient.
- The concept drawing reuses the exact illustrative functions and seeded KDE/manifold generation (`42`); these are conceptual illustrations, not measured observations.
- Trend plots retain monthly counts, cumulative curves, and the events actually rendered upstream. The y limits gain annotation headroom, and panel labels replace redundant hatching. The upstream event dictionary overwrites “Bard” with “LlaMA 1”, skips non-padded `2023-9`, and places GPT-5 outside the available month range; those source behaviors are preserved rather than inventing replacement events.

## Reproduce or reuse

With Python 3.12 or later:

```sh
python3 -m venv .venv
.venv/bin/pip install -r figures4papers-minimal/requirements.txt
.venv/bin/python figures4papers-minimal/render_examples.py
.venv/bin/python figures4papers-minimal/build_gallery.py
```

For a new plot:

```python
from minimal_theme import T, PALETTES, apply_theme, style_axes
import matplotlib.pyplot as plt

apply_theme()
fig, ax = plt.subplots(figsize=(5.8, 4.6))
ax.plot(x, y, color=T.teal, linewidth=T.line, marker="o", markersize=T.marker)
ax.set(xlabel="Condition", ylabel="Response")
style_axes(ax, grid="y")
fig.savefig("result.pdf")
```

Import `minimal_theme.py` from this directory or add it to your project. Adjust the `Theme` dataclass and `PALETTES` mapping to change the full collection. `render-info.json` records the actual font, software versions, and physical export dimensions. `validation.json` records data, geometry, and export checks.

## Attribution and provenance

Original code, data, and figures: **Chen Liu**, [figures4papers](https://github.com/ChenLiu-1996/figures4papers), snapshot `0ddfbd3fc9892e804a3fa01ae46bd0d32617f2aa`, retrieved 2026-11-15. The source snapshot and derived examples retain the upstream **CC BY-NC 4.0** license; see [upstream/LICENSE](upstream/LICENSE). Styling and layout modifications are described above. `provenance.json` records SHA-256 hashes for the copied sources and original images.

Visual reference: Claus O. Wilke's [cowplot themes](https://wilkelab.org/cowplot/articles/themes.html). No R implementation was copied.
