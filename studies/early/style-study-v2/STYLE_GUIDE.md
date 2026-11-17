# Del Alamo paper figures: layout rules v2

This is a reviewable starting specification, not a claim that one layout works
for every dataset. The examples preserve the original theme_minimal/cowplot
approach, outlined marks, thin panel frames and aquamarine/orange states.
BBC influence is limited to clear hierarchy, restrained grids and concise keys.
All examples reuse the synthetic data from v1.

## 1. Start with the actual manuscript width

The official NeurIPS 2026 style sets `textwidth=5.5in`, not 6.5 inches.
The author instructions state a 5.5-by-9-inch text rectangle. Both requested
6.5-inch and NeurIPS 5.5-inch versions are supplied. Treat 6.5 inches as a custom
manuscript preset, not a compliant NeurIPS width.

Sources, checked 7 September 2026:
[Official call for papers](https://neurips.cc/Conferences/2026/CallForPapers),
[official template archive](https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip).
Inside the archive: `neurips_2026.sty` sets `textwidth=5.5in`; the `.tex`
instructions specify the text rectangle and require legible figures.

For total figure width W, n panels and an inter-panel gap g:

    panel width = (W - (n - 1) * g) / n

Use `g = 0.14 in` (about 10 typographic points) as the initial outer gutter.
Panel width includes all axes, labels, legends and margins. It is not merely
the data rectangle. Do not subtract axis labels again after calculating width.

| Size | Panels across | W = 6.5 in | W = 5.5 in |
|---|---:|---:|---:|
| Compact | 4 | 1.520 in | 1.270 in |
| Small | 3 | 2.073 in | 1.740 in |
| Medium | 2 | 3.180 in | 2.680 in |
| Large | 1 | 6.500 in | 5.500 in |

The compact preset is a stress test, not the default. Prefer three across if
category labels, uncertainty or dense marks cannot be read comfortably.
Proof sheets show the different widths at their true relative sizes. They are
review pages, sometimes taller than a manuscript page. The individual panel
assets are the objects intended for use in a paper.

## 2. Keep type and strokes in physical units

| Element | Initial rule | Why |
|---|---|---|
| Tick labels | 7.5 pt Helvetica | Same readable text across all panel widths |
| Axis titles | 8 pt bold Helvetica | Slight hierarchy without dominating the data |
| Legend labels | 7.5 pt | Match tick readability; abbreviate states to A/B |
| Facet labels | 8 pt bold | Identify panels without large headlines |
| Optional assembly letters | 8.5 pt bold | Place outside the data frame, aligned consistently |
| Point diameter | 0.85 / 1.0 / 1.2 / 1.4 mm | Compact / small / medium / large; modest, bounded adjustment |
| Point stroke | 0.20 mm | Keep outlines visible without heavy black borders |
| Frame and ticks | 0.18 mm | Subordinate to marks, but still printable |
| Grid | 0.13 mm, light gray | Reading aid rather than dominant structure |
| Main lines | 0.40 mm | Legible at the final export size |

These are proposed design defaults, not NeurIPS-mandated font sizes. Never
scale a large export down to create the small version: an 8 pt label shrunk
from 6.5 to 1.52 inches becomes about 1.9 pt. Re-render at the target width.
Check the physical PDF at 100%; chat previews are not reliable size rulers.

## 3. Budget whitespace deliberately

| Relationship | Starting value |
|---|---:|
| Outer padding | 3 pt on each side |
| Tick length | 2 pt |
| Tick to label | 2 pt |
| Tick labels to axis title | 4 pt |
| Key to data area | About 4 pt including key margins |
| Independent figure panels | 0.14 in |
| Facets within one chart | 6-8 pt |
| Minimum left axis assembly | 0.40 in, expand for longer labels |
| Right end-label reserve | Half the widest x tick label + 3 pt |

The right reserve is measured from rendered font metrics. Fixed tiny right
margins clip the final tick (for example 1.0 or 100) in small panels. The
renderer adds space to the outside of the data panel rather than truncating
the label. The left reserve is a minimum, not an instruction to hide long labels.

Align data rectangles, not image edges, when comparing adjacent panels.
For a repeated row with shared scales, remove redundant interior y labels
and use one outer axis title and one legend. Recompute the internal allocation
at the same final total width. Do not stretch a cropped figure afterward.

## 4. Choose ticks from available space

1. Subtract the measured axis assemblies from the complete panel width.
2. Propose evenly spaced, interpretable breaks. The current implementation
   aims for about 0.40 inches between horizontal ticks and 0.28 inches vertically,
   then uses extended nice-number breaks. These are density targets, not rigid
   minimum distances; nice-number algorithms can return an extra tick.
   Require at least two ticks within the limits; when an axis crosses zero,
   retain labeled values on both sides of zero.
3. Format labels before measuring them. Retain leading zeros and consistent
   precision within each axis. Avoid precision unsupported by the measurement.
4. Check adjacent rendered label bounds. Aim for at least 4 pt clear space
   between neighboring labels; increase the interval if they collide.
5. Preserve meaningful reference ticks such as zero and interpretable log powers.
   Fewer ticks must not change data limits, binning, smoothing or color limits.

Never rotate numeric ticks simply to fit more of them. For long category
labels, prefer horizontal plots, wrap at a meaningful phrase boundary, use
defined abbreviations, or allocate a larger panel. Do not make text smaller
than the chosen paper minimum as the first response.
The compact category examples use L/M/H for Low/Medium/High, defined on their
proof sheets. Carry those definitions into the manuscript caption.

## 5. Set height from chart structure

The standard starting heights are 1.65, 1.80, 2.05 and 2.65 inches for compact,
small, medium and large. Width and height are separate decisions. A one-panel
figure does not need text or whitespace three times as large as a three-panel row.

- Scatter: use a rectangular panel for relationships. If equal physical x/y
  distance is analytically important (geometry, spatial coordinates, distances),
  use an equal-aspect coordinate system and allocate the required height or span.
- Horizontal categories: allocate enough height for every row; target at least
  12 pt per row after accounting for the legend and x-axis assembly.
- Heatmap: retain all rows and columns. Increase height when row labels or cell
  annotations require it. If square cells carry meaning, calculate height from
  row/column count instead of accepting the generic aspect ratio.
- Facets: compact/small uses four vertically stacked panels (4.15 inches total);
  medium/large uses a 2-by-2 layout. Facet count changes layout before font size.
- Density plus scatter: reserve a small fixed legend band; align x limits and
  panel bounds, hide density axes, and give the scatter most of the remaining height.

## 6. Keep statistical and color meaning stable

The same observations, smoothing, binning and uncertainty calculations are
used at every size. All synthetic boxplot observations remain visible.
White violin dots are per-state medians. Grouped bars start at zero.
Trajectory bands and point intervals are t-based 95% confidence intervals for
means, not prediction intervals. Descriptions belong in a shared caption.

State A uses aquamarine `#38AE9F` and circles; State B uses orange `#E69B35`
and triangles. References use gray/charcoal. J/K use cividis with shared
50-100 limits for synthetic confidence. Color is supplemented by shapes when
states overlap. Heatmap cell colors must remain quantitative; a categorical
brand palette is not a replacement for a sequential scale.

Remove large news headlines, subtitles, author signatures and source footers
from individual paper panels. Put figure-level explanation in the manuscript
caption. The study-page headers and notes are only review aids.

## 7. Procedure for an unfamiliar chart or new constraint

1. Identify the comparison and invariant information: units, reference, scales,
   uncertainty, category order and any required aspect ratio.
2. Set the document width, number of panels and gutter; solve the width equation.
3. Measure labels at 7.5-8 pt, reserve their space, and calculate the remaining
   data rectangle. Reject a layout if labels leave an unusable data area.
4. Choose height based on rows, facet count, density of marks and aspect needs.
5. Choose ticks and a compact legend. Preserve data rather than hiding records
   or changing statistical parameters to make the graphic fit.
6. Resolve overflow in this order: shorten/wrap labels; simplify ticks; share
   redundant axes/keys; reflow facets; increase height; use fewer panels across.
7. Render at final physical dimensions. Check all text bounds, overlaps, reference
   marks and panel alignment. Inspect the PDF as well as the PNG.

## Files and reproduction

`paper_theme.R` stores physical tokens and the width calculator.
`render_sizes.R` builds all twelve chart families and exports PDF/300 dpi PNG
at compact, small, medium and large sizes. Each preset has `panels/`, `proofs/`
and `dimensions.csv`. The two final booklets include the guide and one proof
page for each chart type.

Run from the project root:

```sh
Rscript style-study-v2/render_sizes.R 6.5
Rscript style-study-v2/render_sizes.R 5.5
python3 style-study-v2/assemble_booklets.py
```

Use an R library containing ggplot2, cowplot, ragg and viridisLite. The render
script detects the temporary library from v1 or `PLOT_GALLERY_R_LIB`. On macOS
it uses Quartz PDF to embed the actual Helvetica font; other systems use Cairo.
The Python assembly script needs reportlab, pypdf and pdfplumber. Runtime
package versions and exact dimensions are recorded with the exports.

These proof sheets demonstrate width behavior; they do not by themselves
guarantee every future dataset will fit. The reflow and validation rules are
the mechanism for extending the style responsibly.
