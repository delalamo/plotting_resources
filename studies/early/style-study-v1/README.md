# Del Alamo plotting style — study v1

Twelve synthetic-data examples for visual feedback. The starting point is the
`theme_minimal()` + ggplot2 + cowplot style in `delalamo/af2_conformations`.
Selected BBC elements add Helvetica headlines, a title/subtitle hierarchy,
top legends, selective grids, and a source rule. Scientific panel frames,
outlined marks, and bold axis labels deliberately remain.

## Gallery

- [A–D: Relationships and uncertainty](01-relationships.png)
- [E–H: Distributions](02-distributions.png)
- [I–L: Comparisons and structure](03-comparisons.png)
- [All twelve](overview.png)
- Full-size individual images are in `charts/A.png` through `charts/L.png`.

## Style choices to review

- White background; Helvetica; left-aligned bold headings.
- Thin gray panel frames; light major grids only where useful.
- State A: aquamarine `#37B6A6`, circular points.
- State B: orange `#EDA13A`, triangular points.
- Continuous values: cividis, consistently 50–100 in J and K.
- Thin charcoal outlines; transparent dense points and distribution fills.
- Consistent labels, source rule, and cowplot composition.

The chart titles name chart families for this review. A real analysis should
replace these with informative titles appropriate to its findings. The footer
signature is a provisional design element. No biological results are implied.

## Reproduce

Run from the `plotting_resources` project root:

```sh
Rscript style-study-v1/render_gallery.R
```

Required R packages: ggplot2, cowplot, ragg, viridisLite. These were installed
from CRAN into `/private/tmp/plot-gallery-r-lib` for this render. Set
`PLOT_GALLERY_R_LIB` to use another library, or install into your normal R
library. The temporary library may be removed by the operating system.

`theme_delalamo.R` centralizes the appearance and sources the existing local
BBC theme file. `render_gallery.R` generates data with seed 75751 and exports
the figures. `data/` contains every generated dataset, including raw replicates
for the confidence intervals. `session-info.txt` records package versions.

## Data conventions

- A: two simulated similarity measurements and an equality reference.
- B: pointwise t-based 95% confidence intervals for means of 24 independent
  synthetic replicates per step and state; not prediction intervals.
- C: six matched state comparisons with illustrative fixed values.
- D: t-based 95% confidence intervals around means of 30 simulated values.
- E: 55 observations per condition/state; median, IQR, 1.5×IQR whiskers,
  with all observations overlaid rather than duplicated outlier symbols.
- F: the same observations; separate group medians and trimmed densities.
- G: State A pooled over all three conditions; bin width 0.035.
- H: medium condition only; both kernel densities use bandwidth 0.035.
- I: means from E/F, multiplied by 100; axis starts at zero.
- J/K: synthetic confidence, not actual pLDDT; common color scale.
- L: synthetic conformational coordinate with an aligned density/scatter
  composition inspired by the original Figure 3.

Original references:
[AF2 figure scripts](https://github.com/delalamo/af2_conformations/tree/main/figures)
and [BBC bbplot](https://github.com/bbc/bbplot).
