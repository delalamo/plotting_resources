# Plotting resources

**Original inspiration: [Chen Liu’s figures4papers](https://github.com/ChenLiu-1996/figures4papers).** This project began by adapting its scientific plotting examples; the retained repository figures and several reference variants below derive from that code and data. We then developed our own typography, palette, layouts and reusable templates. Upstream material retains its [CC BY-NC 4.0 license](third_party/figures4papers/LICENSE); see [provenance and licenses](third_party/README.md).

Reusable scientific plotting templates, a complete style guide, and reproducible examples.
The selected style uses **Arial 10 pt**, bold figure/panel/axis titles, **8 pt source and notes**, the R1 cobalt/brick/gold palette, plot background **#D8E8F4**, and figure background **#EDF4F9**. Legends sit below plots. Complete figures default to **6.75 inches**, matching the article text column.

- [Style guide](docs/style-guide.md): exact colors, typography, marks, dimensions and spacing.
- [Editable starters](templates/README.md): nine scripts for common plot types; replace data and captions.
- [Setup](docs/setup.md) and [adopted decisions](docs/decisions.md).
- [Reference gallery](examples/reference_gallery/README.md): all 16 reviewed figures and lorem ipsum article proofs.
- [Design history](studies/README.md): research, earlier studies and decision records.

![Selected line style](docs/assets/template-posttraining-lines.png)

## All examples

Every example has a **styled** preview using the selected blue backgrounds and a **minimal** preview on white. Minimal mode removes figure titles, subtitles, sources and notes while retaining axis/panel labels and legends. These previews are saved in the repository so the links work on GitHub; the scripts regenerate PDF, PNG and SVG exports.

### Reference figures

The previews show native chart artwork; complete titles, sources and notes accompany the article proofs. The numbering matches the 16-figure article proof. U1–U3 use the Urban Institute’s example data; T1–T2, H1, P1–P2 and M1–M4 adapt the original figures4papers code/data. T3 and H2–H4 are synthetic demonstrations. Original values and supplied uncertainties are preserved in the source-derived references. [Data and source records](examples/data/README.md) identify the inputs.

| Figure / ID | Example | Previews | Renderer |
|---|---|---|---|
| 1 / U1 | Education Accounts for One-Fifth of State and Local Spending | [Styled](docs/assets/examples/references/styled/urban-spending-bars.png) · [Minimal](docs/assets/examples/references/minimal/urban-spending-bars.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 2 / U2 | Trust Fund Depletion Raises Projected Poverty Across Groups | [Styled](docs/assets/examples/references/styled/urban-poverty-paired-bars.png) · [Minimal](docs/assets/examples/references/minimal/urban-poverty-paired-bars.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 3 / U3 | Home-Equity Debt Rebounds but Remains Below Its Earlier Peak | [Styled](docs/assets/examples/references/styled/urban-home-equity-lines.png) · [Minimal](docs/assets/examples/references/minimal/urban-home-equity-lines.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 4 / T1 | VIGIL Maintains the Highest Score After Post-Training | [Styled](docs/assets/examples/references/styled/template-posttraining-lines.png) · [Minimal](docs/assets/examples/references/minimal/template-posttraining-lines.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 5 / T2 | ImmunoStruct Leads the IEDB AUROC Comparison | [Styled](docs/assets/examples/references/styled/template-iedb-bars.png) · [Minimal](docs/assets/examples/references/minimal/template-iedb-bars.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 6 / T3 | A Highlighted Method Can Sit Within the Comparison Group | [Styled](docs/assets/examples/references/styled/template-emphasis-lines.png) · [Minimal](docs/assets/examples/references/minimal/template-emphasis-lines.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 7 / H1 | Original Benchmark | [Styled](docs/assets/examples/references/styled/focus-original-benchmark.png) · [Minimal](docs/assets/examples/references/minimal/focus-original-benchmark.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 8 / H2 | Learning Curves | [Styled](docs/assets/examples/references/styled/focus-learning-curves.png) · [Minimal](docs/assets/examples/references/minimal/focus-learning-curves.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 9 / H3 | A Trajectory in Context | [Styled](docs/assets/examples/references/styled/focus-reference-trajectories.png) · [Minimal](docs/assets/examples/references/minimal/focus-reference-trajectories.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 10 / H4 | Crossing Response Curves | [Styled](docs/assets/examples/references/styled/focus-parameter-response.png) · [Minimal](docs/assets/examples/references/minimal/focus-parameter-response.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 11 / P1 | Method Comparison Across Models and Benchmarks | [Styled](docs/assets/examples/references/styled/repository-radar.png) · [Minimal](docs/assets/examples/references/minimal/repository-radar.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 12 / P2 | Post-Training Performance with the R1 Categorical Palette | [Styled](docs/assets/examples/references/styled/repository-posttraining.png) · [Minimal](docs/assets/examples/references/minimal/repository-posttraining.png) | [Source](examples/reference_gallery/scripts/render_reference_collection.py) |
| 13 / M1 | IEDB Benchmark Comparison | [Styled](docs/assets/examples/references/styled/iedb-three-metrics.png) · [Minimal](docs/assets/examples/references/minimal/iedb-three-metrics.png) | [Source](examples/reference_gallery/scripts/render_multipanel_examples.py) |
| 14 / M2 | Brute-Force Composition Across Prompts and Tasks | [Styled](docs/assets/examples/references/styled/brute-force-eight-panels.png) · [Minimal](docs/assets/examples/references/minimal/brute-force-eight-panels.png) | [Source](examples/reference_gallery/scripts/render_multipanel_examples.py) |
| 15 / M3 | Conditional Distributions and Representation Space | [Styled](docs/assets/examples/references/styled/concept-two-panels.png) · [Minimal](docs/assets/examples/references/minimal/concept-two-panels.png) | [Source](examples/reference_gallery/scripts/render_multipanel_examples.py) |
| 16 / M4 | Publication Trends in Text-Only and Multimodal Work | [Styled](docs/assets/examples/references/styled/publication-trends-two-panels.png) · [Minimal](docs/assets/examples/references/minimal/publication-trends-two-panels.png) | [Source](examples/reference_gallery/scripts/render_multipanel_examples.py) |

Regenerate the references with `python examples/reference_gallery/render.py`, or add `--minimal`. The [reference-gallery instructions](examples/reference_gallery/README.md) explain where to find the combined PDF, individual exports and lorem ipsum article proofs. Figures 11, 12 and 16 use text width; the three dense multi-panel exceptions are documented in the [style guide](docs/style-guide.md).

### Reusable starter templates

These nine examples use illustrative data. Copy the nearest script, replace its data and captions, and run it; the shared library handles the styling and layout. See the [template guide](templates/README.md) for inputs and customization.

| Starter script | Example | Previews |
|---|---|---|
| [line_plot.py](templates/line_plot.py) | Categorical lines | [Styled](docs/assets/examples/templates/styled/line_plot.png) · [Minimal](docs/assets/examples/templates/minimal/line_plot.png) |
| [emphasis_lines.py](templates/emphasis_lines.py) | One blue series against gray references | [Styled](docs/assets/examples/templates/styled/emphasis_lines.png) · [Minimal](docs/assets/examples/templates/minimal/emphasis_lines.png) |
| [horizontal_bars.py](templates/horizontal_bars.py) | Ranked horizontal bars with errors | [Styled](docs/assets/examples/templates/styled/horizontal_bars.png) · [Minimal](docs/assets/examples/templates/minimal/horizontal_bars.png) |
| [grouped_bars.py](templates/grouped_bars.py) | Grouped bar comparisons | [Styled](docs/assets/examples/templates/styled/grouped_bars.png) · [Minimal](docs/assets/examples/templates/minimal/grouped_bars.png) |
| [stacked_bars.py](templates/stacked_bars.py) | Stacked composition bars | [Styled](docs/assets/examples/templates/styled/stacked_bars.png) · [Minimal](docs/assets/examples/templates/minimal/stacked_bars.png) |
| [area_plot.py](templates/area_plot.py) | Cumulative area and line series | [Styled](docs/assets/examples/templates/styled/area_plot.png) · [Minimal](docs/assets/examples/templates/minimal/area_plot.png) |
| [multi_panel.py](templates/multi_panel.py) | Shared-scale panel grid | [Styled](docs/assets/examples/templates/styled/multi_panel.png) · [Minimal](docs/assets/examples/templates/minimal/multi_panel.png) |
| [radar_plot.py](templates/radar_plot.py) | Radar profiles on a common scale | [Styled](docs/assets/examples/templates/styled/radar_plot.png) · [Minimal](docs/assets/examples/templates/minimal/radar_plot.png) |
| [custom_panels.py](templates/custom_panels.py) | Custom equations and scatter panels | [Styled](docs/assets/examples/templates/styled/custom_panels.png) · [Minimal](docs/assets/examples/templates/minimal/custom_panels.png) |

Run `python templates/render_all.py` to rebuild all nine, or add `--minimal` for white backgrounds without captions.

## Start a plot

Install Arial Regular, Bold and Italic on the rendering machine, then:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[examples]'
python templates/line_plot.py
python templates/line_plot.py --minimal
```

Outputs are PDF, PNG and SVG in `build/templates/`. Minimal output goes in `build/templates/minimal/`: white figure and plot backgrounds, no figure title, subtitle, source or notes. Axis/panel labels, legends, typography and data colors remain.

For direct use:

```python
import plotting_resources as plots

fig, axes = plots.figure()
ax = axes[0, 0]
plots.line(ax, [1, 2, 3], [4, 7, 6], 'Observed')
ax.set(xlabel='Step', ylabel='Response')
plots.export(fig, 'build/my-plot', title='An example',
             source='Source: Illustrative values.', notes='Notes: Replace with your data.')
# Add minimal=True to export a caption-free figure on white.
```

## Rebuild the collections

```sh
python -m unittest discover -s tests
python templates/render_all.py
python examples/reference_gallery/render.py
python templates/render_all.py --minimal
python examples/reference_gallery/render.py --minimal
```

The reference runner regenerates original source data at native scale, with font, bounds, overlap and data checks. Figures 11, 12 and 16 use text width. The three dense retained exceptions use an explicitly documented wider layout. No saved export is needed to rebuild the current gallery.

## Repository layout

```text
src/plotting_resources/       Shared theme, chart helpers, measured layout/export, selected_style.json
templates/                   Nine editable starters and the collection runner
examples/reference_gallery/  Reproducible retained-figure renderers
examples/data/               Reference inputs and provenance
docs/                        Style guide, decisions, setup and curated previews
studies/                     Historical research, scripts and small decision records
third_party/                 Attributed upstream code and applicable licenses
tests/                       Data, layout and rendering-mode checks
build/                       Ignored generated figures, review books and local history
```

Full generated galleries, PDFs and environments are excluded from Git; the curated README previews are versioned. Historical local exports are preserved in `build/legacy/`; source, data and decision records are versioned. See [upstream provenance](third_party/README.md): the root MIT license does not replace the licenses attached to upstream examples or data.
