# Plotting style guide: R1 palette, S3 structure, option A backgrounds

**Selected on 15 November 2026.** The plot background is **`#D8E8F4` (option A)** and the full figure background is **`#EDF4F9`**. Use the R1 cobalt/brick/gold palette and **10 pt Arial**, with bold figure, panel and axis titles. **Source credits and notes use 8 pt Arial Regular**, selected on 16 November 2026. This document consolidates the decisions adopted during the reference-figure reviews. [selected-style.json](../src/plotting_resources/selected_style.json) records the corresponding machine-readable settings.

[Complete figure gallery](../build/reference-gallery/figures4papers-minimal/gallery.html) · [Complete gallery PDF](../build/reference-gallery/figures4papers-minimal/gallery-r1-option-a.pdf) · [Reference page gallery](../build/reference-gallery/figures4papers-minimal/reference-review-10pt/gallery.html) · [Multi-panel gallery](../build/reference-gallery/figures4papers-minimal/multi-panel-arial-10pt/gallery-math-fixed.html) · [All 16 figures in article context](../build/reference-gallery/figures4papers-minimal/article-context/all-16-figures-in-article-context.pdf) · [Scrolling article](../build/reference-gallery/figures4papers-minimal/article-context/article-context.html)

## 1. Backgrounds and visual structure

| Surface or element | Approved setting |
|---|---|
| Plot area, inside axes | **`#D8E8F4`**, fully opaque |
| Entire figure | **`#EDF4F9`**, fully opaque |
| Figure-background coverage | Titles, subtitles, axis labels, legends, source notes, outer margins and gaps between panels |
| Article page outside the figure | White, `#FFFFFF`, in the article proofs |
| Plot frame | All four sides; `#566C7B`, 0.45 pt |
| Coordinate grid | Dotted; `#CBD6DF`, 0.45 pt; use only where appropriate to the chart |
| Main text | `#282828` |
| Secondary text | `#666666` |

Option A is the **first page of the [eight-option background study](../build/legacy/figures4papers-minimal/blue-background-sweep/blue-backgrounds-in-article.pdf)**. [View the selected article example](../build/legacy/figures4papers-minimal/blue-background-sweep/previews/option-A.png). Match the exact hex values; neither background is a transparent blue overlay on white. Both backgrounds are part of the exported figure.

In article context, use one continuous pale-blue block behind the chart and all its figure text. The current proof uses **18 pt horizontal padding and equal 13.5 pt top and bottom padding**, with **no extra outer border or shadow**. The thin four-sided border belongs to the plot area. Measure the top gap from the figure edge to the title text box and the bottom gap from the final source/note text box to the figure edge. Let the outer block fit its content; do not reserve the space previously occupied by 10 pt source/notes. For multi-panel figures, the gutters remain the lighter figure color.

## 2. Typography and mathematical notation

| Text role | Font | Size at final figure dimensions | Weight |
|---|---|---|---|
| Figure title | Arial | 10 pt | Bold |
| Panel title | Arial | 10 pt | Bold |
| Axis title | Arial | 10 pt | Bold |
| Subtitle, ticks, legend, direct labels, values, annotations | Arial | 10 pt | Regular |
| Panel letters | Arial | 10 pt | Regular |
| Source credits and notes | Arial | **8 pt** | Regular |
| Equation base | Arial / Arial Italic, with documented symbol fallback | 10 pt | Non-bold |
| Mathematical subscripts and superscripts | Same equation font system | Conventional reduced size; 7 pt in these examples | Non-bold |

**Source credits and notes are the only smaller prose exception: 8 pt.** Keep subtitles, panel letters, ticks, legends, annotations and data labels at 10 pt; reposition or wrap them as needed. Keep panel letters regular even when the adjacent panel titles are bold. Titles, subtitles, sources and notes are left aligned; the figure text blocks use 1.3 line spacing.

Use actual Arial faces and embed them in PDF exports. Fail clearly if Arial is unavailable instead of silently substituting another family. Font sizes and stroke widths apply at the final physical export dimensions. Do not shrink an exported figure into a smaller page slot and still call its type 10 pt; regenerate at the intended size.

Use Matplotlib Mathtext for formulas. Roman letters use Arial; variables use Arial Italic. STIX supplies mathematical symbols Arial lacks, including the required calligraphic symbols. This is a specific math-symbol exception, not a replacement prose font. Render subscripts, superscripts, conditional bars and other symbols correctly; raw LaTeX commands and underscores must not appear as visible text. Formula text remains non-bold. Math-heavy SVGs use outlined glyphs for portable rendering.

Article prose is separate from figure typography: the lorem ipsum proofs use 11 pt Arial body text and larger article headings. Those headings do not establish new plotting font sizes.

## 3. R1 categorical palette

| Role | Name | Hex |
|---|---|---|
| Signature | Cobalt | `#285F96` |
| Companion 1 | Brick red | `#B9413A` |
| Companion 2 | Old gold | `#A68517` |
| Extended 4 | Malachite | `#2B7C70` |
| Extended 5 | Heather rose | `#9E638C` |
| Extended 6 | Violet slate | `#685B80` |
| Extended 7 | Supporting gray | `#717B7F` |
| Extended 8 | Supporting brown | `#A96E45` |
| Extended 9 | Supporting olive | `#5B713C` |
| Diagram prior | Neutral | `#7A7770` |

The blue signature is balanced by warm brick and gold. Use stable category mappings throughout a figure and across related figures. These are categorical colors; they are not a sequential scale. Retain labels, marker shapes and dash distinctions so meaning does not depend solely on hue. The emphasis treatment below is a separate way to use these colors when one entry matters most.

### Fixed method mappings

| Method | Color |
|---|---|
| DPO | `#B9413A` |
| DA-DPO | `#A68517` |
| VIGIL (Ours) | `#285F96` |

### Fixed benchmark mappings

| Method | Color |
|---|---|
| Prime-2.1 | `#717B7F` |
| NetMHCpan | `#685B80` |
| MHCnuggets | `#A96E45` |
| MHCflurry | `#2B7C70` |
| DeepNeo | `#B9413A` |
| BigMHC-EL | `#9E638C` |
| BigMHC-IM | `#5B713C` |
| BigMHC retrained | `#A68517` |
| ImmunoStruct (ours) | `#285F96` |

### Fixed composition mappings

| Model | Color |
|---|---|
| DeepSeek R1 Distill Qwen 1.5B | `#285F96` |
| DeepSeek R1 Distill Qwen 14B | `#B9413A` |
| DeepSeek R1 Distill Llama 70B | `#A68517` |
| deepseek-chat (Deepseek-V3) | `#2B7C70` |
| deepseek-reasoner (Deepseek-R1) | `#9E638C` |
| gemini-2.5-flash-preview-04-17 | `#685B80` |
| OpenAI o3 | `#717B7F` |

## 4. Lines, markers, bars and fills

| Element | Setting |
|---|---|
| Data curves | 1.25 pt |
| Error-bar stems and caps | 0.65 pt; cap size 2 pt |
| Ordinary line markers | 3.5 pt, open; 0.625 pt edge in the current templates |
| Open-marker interior | Match the plot background; no white fill |
| Marker shapes and dashes | Preserve distinctions used by the source/reference template |
| Ticks | 2 pt length; 0.45 pt width; 3 pt x-tick and 4 pt y-tick label padding |
| Bars | Width 0.70 of the category unit; 0.35 pt outline |
| Concept fills | Alpha 0.08 |
| Publication-trend fills | Alpha 0.14 for evaluation / brick; 0.22 for method / cobalt |
| Radar fills | Alpha 0.035 |
| Composition stacks | First component opaque; subsequent components alpha 0.80 |
| Hatching | `#707070`, 0.4 pt strokes |

These defaults describe the quantitative marks. Dense concept point clouds and their source-specific annotations retain the geometry and size adjustments documented in the example renderer. The manifold has no coordinate grid; the radar uses radial guides. Directly labeled benchmark bars omit grids and numeric ticks.

## 5. Optional emphasis: one blue series, gray comparisons

Use **cobalt `#285F96`** for the focus and opaque neutral grays from **`#777777` through `#B7B7B7`** for the comparison entries. Keep both at **1.25 pt**. Draw the blue series last with a solid line; draw the references with dashed lines. The focus need not be the highest-valued series.

| Number of gray references | Gray values |
|---|---|
| Three | `#777777`, `#979797`, `#B7B7B7` |
| Five | `#777777`, `#878787`, `#979797`, `#A7A7A7`, `#B7B7B7` |
| Other counts | Evenly space the integer RGB values from 119 to 183, rounding to the nearest integer |

The current reference dash cycle is `(4, 2)`, `(3, 1.5, 1, 1.5)`, `(1, 2)`, `(6, 2)`, `(3, 2, 1, 2)`, each at zero offset in Matplotlib. These are the on/off sequences passed to Matplotlib, which retains its default scaling with linewidth. Gray shades and repeated dashes do not uniquely identify arbitrarily many series; use the labels and existing keys.

Keep the selected backgrounds, frame and type rules. H1-H4 show this treatment; T3 shows the direct-label variant. [Current examples appear on pages 4-6 of the reference collection](../build/reference-gallery/figures4papers-minimal/reference-review-10pt/reference-figures-r1-s3-arial-10pt.pdf). The [earlier emphasis study](../build/legacy/figures4papers-minimal/emphasis-examples/gallery.html) preserves the previous background and Helvetica for historical comparison.

## 6. Titles, legends, sources and spacing

| Relationship | Current specification |
|---|---|
| Figure title to subtitle | 3 pt |
| Subtitle to first visible chart content, including panel headings | 8.25 pt |
| Native chart export padding | 2.25 pt; placement adds 6 pt to make the 8.25 pt clearance |
| Legend placement | **Below** the plot and its axis labels |
| Lowest plot/axis-label content to legend | 7.5 pt, measured from actual text bounds |
| Separate legend groups | 4.5 pt between groups |
| X-axis title padding | 6 pt |
| Y-axis title padding | 4 pt |
| Tick-label padding | 3 pt on x; 4 pt on y |
| Chart export to source line | 7.5 pt in article and full-width layouts; 10.5 pt in paired reference-book layouts |
| Source line to notes | 6 pt |
| Article figure-block padding | 18 pt horizontal; 13.5 pt vertical |

Do not leave a second unused top margin inside an exported chart; that was the cause of overly distant titles and subtitles in earlier drafts. The compact revision changes the vertical aspect of the axes while retaining their data and limits; trim unused canvas space around the content.

Use a shared legend when panels share an encoding. Keep legend order consistent with the plotted categories and size the legend to its associated plotting region. Multiple legend groups may be stacked below the axes. T1 and T3 retain direct endpoint labels and omit a redundant legend. The source and explanatory notes remain inside the pale-blue figure block, below the chart and its legend.

The overall approach is informed by the [Urban Institute guide](https://urbaninstitute.github.io/graphics-styleguide/), with adopted project overrides. **Below-plot legends**, 10 pt Arial with 8 pt source/notes, bold titles, the R1 palette, blue backgrounds and four-sided frames are our choices. The exact spacing above is the approved project implementation; it is not a claim that Urban prescribes every value. See the [recorded math and spacing review](../studies/records/multi-panel-arial-10pt/SPACING_REVIEW.md) for the distinction between published guidance, official-theme defaults and local layout choices.

## 7. Multi-panel figures

Use regular-weight panel letters in reading order: left to right, then top to bottom. Panel titles remain bold. Comparable panels use equal dimensions and matching axis limits; preserve category colors and suppress redundant interior labels. Arrange panels in a meaningful order. A heterogeneous concept figure can use unequal widths while aligning the panel edges.

| Retained template | Arrangement | Panel spacing | Current native chart size |
|---|---|---|---|
| IEDB comparison | 1 x 3 | 6 pt horizontal | 13.00 x 2.91 in |
| Brute-force composition | 2 x 4 | 6 pt horizontal; 0.4125 in vertical | 13.00 x 5.16 in |
| Concept illustration | 1 x 2 | 0.56 in horizontal; wider right schematic | 13.00 x 3.19 in |
| Publication trends | 2 x 1 | 0.615 in vertical | 6.25 in wide; labels reflowed at 10 pt |

These vertical and mixed-panel gaps allow room for the headings and shared axes in these particular templates. They are not universal spacing rules for every future arrangement. The concept legend applies only to its left panel. The current figure sizes are rounded here; the validation files record the precise geometry.

The multi-panel booklet uses 14 x 10-inch pages with charts placed at native size. Gallery figures use one common display scale. Avoid making each differently sized source image fill the same display box, which makes nominally identical fonts look inconsistent.

## 8. Chart-specific decisions and data integrity

- **Bars:** Start at zero. The three-panel benchmark retains the source method order, every mean and standard deviation, common 0-1.04 limits, and three-decimal labels instead of numeric ticks and grids. T2 is the existing ranked horizontal-bar variant, highlighting the selected method in cobalt against gray.
- **Lines:** Preserve the original steps, values and scales for reference remakes. T1 names series at the right endpoint; the full categorical P2 variant uses a below-plot legend. Keep the SFT-only reference at its original value of 22.
- **Composition:** Retain all eight panels, 224 segments, model keys and shared probability scales. Source totals of 0.999-1.001 are rounding in the supplied data; do not silently renormalize them.
- **Concept:** Retain the source generator, seed, 5,200 points and trajectories. Correct the math rendering and adjust annotation placement for readability without changing source coordinates; the compact layout changes the displayed vertical aspect.
- **Publication trends:** Retain all 132 monthly values and their cumulative sums, with matching 0-125 scales. Source events absent from the original month vector remain omitted and documented in the validation file. Event labels are historical source content, not independently verified release dates.
- **Radar:** Retain the 12 spokes, all 36 values and the benchmark-specific scales: POPE 75-91, MathVista 30-61, MMBench 40-85. The normalized polygon areas are not comparable across benchmarks. Keep the radar circular, with one labeled radial scale per benchmark group and all 12 spokes.
- **Synthetic examples:** Explicitly identify H2-H4 and the T3 derivative as illustrative, not experimental results. Selecting a focus does not imply it is the best performer.

All original numeric arrays and supplied uncertainty values are preserved. Source credits and explanatory notes accompany styled figures; minimal exports retain this metadata in the saved records and require attribution in the surrounding article. The review includes **current-style references only**: 16 figures, 27 panels, including all four native repository multi-panel figures. The **3D sphere** and **manually assembled repository composites** remain excluded; the later request to include native multi-panel plots is retained.

## 9. Dimensions, exports and review context

**Approved chart height:** Preserve the native chart dimensions established by the 75%-height review. That review fitted complete blocks with 10 pt source/notes to 75% of their originals. The subsequent 8 pt source/notes decision trims the outer block to its new content, with **13.5 pt above the title and 13.5 pt below the final note**. Do not stretch the plot or retain the saved footer space to force the entire block back to exactly 75%. The later text-width decision supersedes the earlier wide layout for figures 11, 12 and 16. Reflow those charts at native 6.25-inch width, preserving data, 10 pt type, strokes and markers. Keep approved heights where the new label layout permits. White article pages remain 14 x 14 inches. [figure-height-baseline.json](../examples/data/inputs/figure-height-baseline.json) preserves the original measurements used to reproduce the approved chart sizes.

Reflow long labels and reduce redundant tick labels where needed to avoid collisions; keep all original observations and axis limits. Direct labels may use thin leaders. The radar retains a circular grid. These adjustments preserve readability at the fixed font size.

| Output | Specification |
|---|---|
| Default: single and multi-panel figures | Native chart width 6.25 in; complete padded figure 6.75 in (486 pt), matching article text |
| Explicit wide exceptions | Native 13 in only when needed for readable dense content |
| Reference and multi-panel booklets | 14 x 10 in pages |
| Mixed-width article-context proof | 14 x 14 in pages; charts placed at native size |
| Background-selection article proof | US Letter, 8.5 x 11 in; same native 6.25-inch chart on every page |
| Production PNG | 300 dpi |
| PDF | Vector artwork where applicable; embedded Arial faces and the documented math-symbol fallback |
| SVG | Editable ordinary text; outlined glyphs for portable math-heavy figures |
| Background opacity | Opaque figure and plot colors |
| Web galleries | Static figures; self-contained article HTML embeds SVGs |

The page dimensions are review formats, not required publication page sizes. Regenerate charts at their intended final dimensions to maintain the 10 pt specification. In the article HTML, keep the native chart width and scroll a wide figure on a narrow screen instead of shrinking its type. Use 100% browser zoom for checking the native text size. The color-sweep chart PNGs are 240 dpi comparison assets; that study does not change the production 300 dpi default.

The current implementation is Python/Matplotlib, with NumPy/SciPy and PyMuPDF used by the renderers. Interactive web charts were discussed but have **not** been implemented or adopted as a required output. The current galleries have no data tooltips or interactive legend toggles.

Check the exported artifact, not only its code: verify font faces, sizes, weights and embedding; math rendering; data preservation; matching panel scales; legend clearance; text overlaps and clipping; and the actual figure/plot colors. Inspect rendered PDF pages at the intended size. Color-vision and grayscale previews from the palette studies inform the palette use but do not guarantee that every possible new chart is accessible.

## 10. Authoritative settings and regeneration

**For a new plot, start with [the reusable templates](../templates/README.md).** Nine starters cover lines, blue-and-gray emphasis, horizontal/grouped/stacked bars, areas, radar, shared-axis grids and custom scientific panels. Copy a starter and replace its data and captions. [plotting_resources](../src/plotting_resources/) reads the selected settings and handles the fonts, palette, below-plot legend, wrapped headings, 8 pt sources/notes, equal outer padding and PDF/PNG/SVG exports. The template defaults provide compact starting proportions; adjust panel height for new content instead of applying a historical percentage to arbitrary data.

The commands below reproduce the specific reviewed gallery examples from their saved data.

Use this guide with [selected-style.json](../src/plotting_resources/selected_style.json) for new work. The selection is **R1 colors + S3 structural settings + option A backgrounds + 10 pt Arial**. The option-A approval supersedes the earlier background values. The 75%-height revision establishes the current chart dimensions and vertical spacing. The later 8 pt source/notes decision supersedes the former 10 pt footer and fixed outer-block height; all other typography, palette and mark sizes remain fixed.

Run from the repository root after following [setup.md](setup.md):

```sh
python templates/render_all.py
python examples/reference_gallery/render.py
python templates/render_all.py --minimal
python examples/reference_gallery/render.py --minimal
```

The nine editable starters use the installed package. The reference runner builds all 16 saved examples, the four native multi-panel figures, PDF/PNG/SVG exports, a combined review book, and a sixteen-page lorem ipsum article proof. Generated files live in ignored `build/`; no prior generated file is required. See [setup.md](setup.md) for paths. Historical explorations remain in [studies](../studies/); their former beige-theme defaults are not current defaults.

**Width policy:** Use the article's 486 pt text width for the complete figure. The chart itself is 450 pt wide and receives 18 pt padding on each side. This is the default for both single and multi-panel templates. Figures 11 (radar), 12 (post-training) and 16 (publication trends) now follow it. Wider figures require a concrete readability need. The retained exceptions are M1 (27 numeric bar labels and uncertainties), M2 (eight panels with seven categories each), and M3 (dense annotated scientific schematic beside equations). They use native 13-inch charts. Never shrink their text by scaling a finished export into a narrower slot; redesign or reflow the panels instead.

**Minimal mode:** Pass `--minimal` to any starter, the starter collection, or the reference-gallery runner. For direct library use, pass `minimal=True` to `finish()` or `export()`. It removes the figure title, subtitle, source and notes. Both the entire figure and plot backgrounds become opaque white (`#FFFFFF`), including background-colored marker interiors and annotation boxes. Axis titles and labels, panel titles and letters, data annotations, legends, palette, fonts and stroke sizes remain. Blank caption space is removed; legends remain below axes. Minimal output goes in a separate `minimal/` build folder and does not overwrite styled output. Source data and credits remain available in metadata; place necessary credits and synthetic-data explanations in the manuscript caption.

The guide consolidates adopted decisions; it does not declare unfinished exploratory work approved. Universal sequential/diverging heatmap scales, standard map/table styles and every possible category-count palette subset have not been selected. Multi-panel gap values above are the established templates, not a newly invented universal rule set.

## 11. Selection history and provenance

| Earlier decision | Current disposition |
|---|---|
| B / cream background `#FAF6EE` | Superseded by the blue scheme |
| Original S3 plot `#EBF1F5` on white | Superseded; historical S3/R1 studies retain it |
| First full-figure tint `#F5F8FA` | Superseded by `#EDF4F9` |
| Interim plot blue `#DCEAF4` | Superseded by **option A `#D8E8F4`** |
| Early black 0.55 pt frame | Superseded by selected S3 slate `#566C7B`, 0.45 pt, still on all four sides |
| Helvetica and mixed-size text | Superseded by 10 pt Arial and the explicit math exception |
| Above-plot legends and loose top margins | Superseded by the below-plot legends and measured spacing above |
| Original and 50% figure-block heights | Superseded by the approved 75%-height chart layout |
| 10 pt source/notes and reserved footer height | Superseded by 8 pt source/notes and equal 13.5 pt top/bottom padding |
| Cool-only palette alternatives | Not selected; R1 cobalt, brick and gold remains selected |

[Background decision study](../studies/records/blue-background-sweep/README.md) · [R1 palette research](../studies/records/s3-design-study/README.md) · [Design history](../studies/README.md) · [Earlier B guide](../studies/records/STYLE_GUIDE_B_ARCHIVE.md)

Historical studies and their original exports remain available as records of the choices; they are not current defaults. Original example code and data: [Chen Liu, figures4papers](https://github.com/ChenLiu-1996/figures4papers), under [CC BY-NC 4.0](../third_party/figures4papers/LICENSE). Urban-derived examples retain their own source credits in the reference collection.
