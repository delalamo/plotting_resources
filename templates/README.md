# Reusable plotting starters

**New plots do not need to be rebuilt from scratch.** Copy the nearest starter, replace its data and captions, and run it. The shared [plotting_resources](../src/plotting_resources/) module reads the approved [selected_style.json](../src/plotting_resources/selected_style.json) and handles the styling, figure layout and exports.

[Example gallery](../build/templates/gallery.html) · [Example PDF](../build/templates/template-examples.pdf) · [Portable starter kit](../build/templates/plotting-template-starter-kit.zip)

## Quick start

From the repository root:

```sh
python -m pip install -e '.[examples]'
cp templates/line_plot.py templates/my_plot.py
# Edit the data, axis labels, title, subtitle, source and notes in my_plot.py.
python templates/my_plot.py
```

This creates `my_plot.pdf`, `my_plot.png` and `my_plot.svg` in `build/templates/`, plus a small layout report. The script name determines the output name. Keep a copied starter beside `_common.py`, or import the installed `plotting_resources` package directly in your own script. The starter ZIP contains the package, settings, dependencies and editable examples; extract it and install with `pip install -e '.[examples]'`.

Add `--minimal` to any command to remove the title, subtitle, source and notes and use white figure and plot backgrounds. Axis/panel labels, legends, colors, fonts and marks remain. Minimal output is saved separately under `build/templates/minimal/`. With direct library use, call `plots.export(f, path, minimal=True, ...)`.

**Arial Regular, Bold and Italic must be installed.** The renderer reports a missing font instead of silently substituting one. Fonts are embedded in PDFs. The existing local environment also works:

```sh
MPLCONFIGDIR=/private/tmp/figures4papers-mpl /private/tmp/figures4papers-venv/bin/python templates/line_plot.py
```

## Pick a starter

| File | Use it for | Inputs you replace |
|---|---|---|
| [line_plot.py](line_plot.py) | Several categorical line series | X values; named Y arrays |
| [emphasis_lines.py](emphasis_lines.py) | One blue series against gray baselines | X values; focus array; named comparisons |
| [horizontal_bars.py](horizontal_bars.py) | Ranked bars, optional errors, one highlighted entry | Category labels; values; errors; highlighted index |
| [grouped_bars.py](grouped_bars.py) | Several methods per category | Categories; named value/error arrays |
| [stacked_bars.py](stacked_bars.py) | Composition or probability stacks | Categories; named component arrays |
| [area_plot.py](area_plot.py) | Publication trends or cumulative series | X values; named cumulative arrays |
| [multi_panel.py](multi_panel.py) | A shared-scale panel grid | Row/column count; one dataset per panel |
| [radar_plot.py](radar_plot.py) | Profiles measured on one common scale | Dimension names; named score arrays; limits |
| [custom_panels.py](custom_panels.py) | Diagrams, equations, scatter plots or mixed panels | Ordinary Matplotlib drawing commands inside each panel |

Every starter has clearly named `TITLE`, `SUBTITLE`, `SOURCE` and `NOTES` fields. The samples are synthetic; replace their source and uncertainty descriptions when using real results. For vertical single-series bars, copy `horizontal_bars.py`, use `horizontal=False`, and put the value-axis label on the y axis.

## What is automatic

- Arial at 10 pt for plotting text; bold figure/panel/axis titles; regular 8 pt source and notes.
- Selected R1 colors, cobalt emphasis with gray baselines, `#D8E8F4` plot backgrounds and `#EDF4F9` figure backgrounds.
- Line weights, error-bar caps, marker sizes, bar outlines, four-sided frames and dotted grids.
- A shared legend below the plotted content and axis labels; duplicate legend entries are removed. Legend columns decrease if the labels would exceed the figure width.
- Wrapped headings and footnotes, measured label margins, and equal 13.5 pt top/bottom padding. The canvas fits the content without shrinking the text.
- Native-size vector PDFs, 300 dpi PNGs and SVGs. SVGs containing math use outlined text to preserve glyphs on other systems.

The native chart defaults are 6.25 inches wide with a 2.2-inch-high axes region; multi-panel charts also default to 6.25 inches wide, with 1.65-inch-high panels. The complete exported figure adds 18 pt of padding on each side, making its default total width 6.75 inches, matching the article text column. Use a wider override only when the contents cannot remain readable at text width. These are reusable starting proportions close to the approved compact examples. The prior 75% comparison was relative to specific old figures, not a universal percentage to apply to new datasets. Figure height grows as needed for labels, legends and notes. Override `width` or `panel_height` in `ps.figure(...)` when the content needs more space; text and strokes remain the same physical size.

## Data from a CSV

The arrays in a starter can be loaded instead of typed. For example, replace the `X`/`DATA` definitions in the line starter with:

```python
import csv
from pathlib import Path

with (Path(__file__).parent / "my_data.csv").open(newline="") as file:
    rows = list(csv.DictReader(file))
X = [float(row["step"]) for row in rows]
DATA = {
    "Method A": [float(row["method_a"]) for row in rows],
    "Method B": [float(row["method_b"]) for row in rows],
}
```

Units, appropriate axis limits, the meaning of error bars, statistical calculations and any custom scientific geometry remain your choices. Helpers do not silently normalize data, infer significance or invent uncertainty. Very long labels, unusually many categories, overlapping annotations or dense custom drawings still need a visual review. Use explicit category-to-color mappings for related figures rather than changing category order between them.

## Rebuild and inspect every starter

```sh
python templates/render_all.py
```

This runs all nine starters, checks embedded fonts, sizes and text bounds in their PDFs, and produces a combined PDF, HTML gallery and portable ZIP. It does not regenerate or change the approved reference gallery. Set `PAPER_OUTPUT_DIR` to write exports elsewhere.

## Existing scripts are still useful

| Existing file | Purpose |
|---|---|
| `render_reference_collection.py` | Rebuild all 16 specific reference examples from their saved data |
| `render_multipanel_examples.py` | Rebuild the four original repository multi-panel examples, including the custom concept illustration |
| `render_article_context.py` | Put those saved figures into lorem ipsum article pages |
| `build_gallery.py` | Assemble their downloadable gallery, combined PDF and source archive |
| `figure_height.py` | Reproduce the approved dimensions of the historical reference figures |
| `render_*study.py`, `render_*options.py`, `render_*sweep.py` | Preserve earlier palette, background and typography explorations |

Use these new starters for new data. Keep the existing renderers for exact reproduction of the reviewed examples. `minimal_theme.py` is the old beige/Helvetica theme and is not the current default.
