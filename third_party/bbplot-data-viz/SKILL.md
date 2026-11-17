---
name: bbplot-data-viz
description: Create, restyle, review, and export consistent BBC-style data visualizations with R ggplot2, bbplot, and cowplot. Use for scientific or editorial charts that need bbplot typography, restrained palettes, small multiples, annotations, shared legends, publication composition, and reliable PNG/SVG output.
---

# BBPlot Data Visualization

Use `bbc_style()` as the visual foundation. Treat it as a theme, not a complete chart specification: choose marks, scales, annotations, and layout from the data and message.

## Workflow

Follow these steps in order.

### Step 1: Identify the message

Determine:

1. The finding or comparison the chart must make visible.
2. The necessary context: reference state, threshold, experimental value, or peer group.
3. The chart family that exposes that relationship with the fewest layers.

Write a short finding-led title before styling. Keep technical definitions and units in the subtitle or axis labels.

### Step 2: Select a bbplot archetype

Inspect `assets/bbplot-example-plots.png` when visual matching matters. Prefer the closest existing archetype:

- Bubble scatter for two continuous measures plus confidence or magnitude.
- Small multiples for repeated measures across proteins, conditions, or cohorts.
- Paired panels for distributions above values sharing the same x-axis.
- Stacked or grouped bars only for genuine part-to-whole comparisons.
- Dot or dumbbell plots for ranked categories and two-point comparisons.

Preserve the data structure. Do not force a histogram, bubble size, or categorical binning merely because an example uses it.

### Step 3: Build the chart

Start with the original data and `ggplot2`. Add `bbc_style()` after geoms and scales, then apply only the scientific overrides required for the chart.

Read `references/ggplot-cowplot.md` before implementing a ggplot or cowplot chart. Reuse its theme wrapper, palettes, and export pattern.

### Step 4: Compose and finalize

Use `cowplot::plot_grid()` for multi-part figures. Align panels explicitly, collect or reproduce only one legend, and keep titles and sources outside dense panels.

Export with an explicit size and DPI. Inspect the rendered PNG or SVG, not only the R plot object.

### Step 5: Validate

Run the checklist below and revise until every item passes.

## Universal rules

### 1. Use bbplot typography

- Use Helvetica or an available metrically similar sans-serif.
- Use a bold, left-aligned title.
- Use a regular-weight subtitle directly below the title.
- Keep facet headings bold and left aligned.
- Keep source text small and left aligned below a thin rule.

Scale type to output dimensions. The original 28/22 pt bbplot sizes target a 640 px news graphic; reduce them for dense scientific small multiples.

### 2. Keep the background and structure quiet

- Use a white plot and panel background.
- Remove panel borders, axis lines, and tick marks by default.
- Keep minor gridlines absent.
- Use light horizontal major gridlines when values must be compared.
- Add vertical gridlines only when both axes carry equally important continuous values.

### 3. Use color for meaning

`bbc_style()` does not supply colors. Choose them deliberately:

- One series: `#007F7F`.
- Two semantic states: teal `#007F7F` and orange `#FA6400`.
- Neutral/reference marks: `#222222`, `#6B6B6B`, or `#CBCBCB`.
- Ordered scientific values: use perceptually uniform viridis or cividis scales.
- Unordered categories: use at most four restrained colors.

Do not convert continuous confidence or depth values into arbitrary bins solely for decoration.

### 4. Put legends at the top

Use one horizontal legend above the plotting area. Remove legend titles when the subtitle already defines the encoding. For two short series, prefer direct labels or a compact inline key.

### 5. Preserve scientific context

Keep relevant thresholds, experimental structures, native states, uncertainty, and units. Draw reference lines in muted gray with a nearby label. Never drop a scientific layer merely to imitate an editorial example.

### 6. Make points restrained

- Default scatter points to 1.2–2.2 mm with moderate alpha.
- Avoid thick black outlines on hundreds of points.
- Use size only when it encodes a variable the reader needs.
- Use shape as a secondary differentiator for accessibility when categories overlap.

### 7. Use finding-led annotations

Annotate one or two notable features: an outlier, threshold crossing, strongest relationship, or experimental reference. Do not label every point.

### 8. Keep titles within the canvas

Set `plot.title.position = "plot"`. Shorten titles before reducing type. Always inspect for clipping at the final export dimensions.

### 9. Use small multiples consistently

- Keep a stable protein/category order.
- Share scales when direct magnitude comparison is essential.
- Use free scales only when shared scales would erase within-panel structure; disclose this in the subtitle.
- Use one shared legend and shared outer axis labels.
- Use whitespace, not boxes, to separate facets.

### 10. Build composite figures with hierarchy

For density-plus-scatter or similar composites:

- Align panels on the shared x-axis.
- Give the primary quantitative panel more height.
- Remove redundant axes and repeated titles.
- Keep series colors identical across every component.
- Use `cowplot` to compose; do not rely on manual SVG edits.

### 11. Finalize without BBC branding

Use the bbplot source-rule and footer pattern, but do not add BBC blocks or imply BBC authorship. Credit the data source and repository instead.

## Chart guidance

| Chart | Default treatment |
|---|---|
| Continuous scatter | Small translucent points; horizontal grid; optional muted regression or threshold; continuous colorbar when needed |
| Faceted scatter | Stable facet order; one shared color scale; free scales only with disclosure; annotate a comparable statistic per facet |
| Density | Thin outline plus low-opacity fill; no y-axis unless density magnitude matters; mark experimental values directly |
| Two-state comparison | Teal and orange across every panel; pair color with shape or labels; keep native structures black |
| Composite | Shared title, subtitle, legend, and source; aligned panels; one dominant panel |
| Bar | Start at zero; direct value labels; no outlines; sort unless order is meaningful |

## Validation checklist

- [ ] The title states the finding or comparison.
- [ ] `bbc_style()` is present and overrides are intentional.
- [ ] The title, subtitle, facets, legend, and source are not clipped.
- [ ] Text remains readable at final output size.
- [ ] No unnecessary panel borders, minor grids, or tick marks remain.
- [ ] Color encodes data consistently and uses no more hues than necessary.
- [ ] Continuous scientific variables remain continuous unless binning is analytically justified.
- [ ] Thresholds, experimental structures, and units remain visible.
- [ ] Small multiples use a stable order and clearly disclose free scales.
- [ ] Composite panels align without manual post-processing.
- [ ] One source line identifies the dataset or publication.
- [ ] PNG/SVG output has been visually inspected at full size.
