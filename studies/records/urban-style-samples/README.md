# Urban layout samples with R1 / S3

[Gallery](gallery.html) · [PDF booklet](urban-r1-samples.pdf) · [Native charts](charts/)

These six samples use the selected Arial typography with bold axis titles. U1-U3 reproduce data behind examples in the [Urban Institute guide](https://urbaninstitute.github.io/graphics-styleguide/). T1-T3 adapt existing templates.

## Explicit settings and exceptions

**Typography.** Arial Regular; axis titles use Arial Bold. Sizes remain 11.43 / 10 / 8.57 pt for plot titles / axis titles / ticks and legends. Figure numbers and notes are 8 pt; direct bar values are 8.5 pt.

**Palette and emphasis.** Keep R1 category colors and S3 #EBF1F5. The emphasis example retains cobalt, five neutral grays, equal 1.25 pt strokes, dashed references and blue drawn last.

**Frame, grid and marks.** Keep the .45 pt frame, .45 pt dotted grid, 3.5 pt open markers, .70 bar width, .35 pt bar edges and .65 pt error bars with 2 pt caps. Omit grids on directly labeled bars.

**Labels and arrangement.** Apply Urban's title/sentence capitalization, zero-based bars, right-aligned horizontal categories, above-chart legends and direct series labels where feasible.

**Output and spacing.** Chart width is Urban's 6.25 in print width. The 4.35 in chart height, .5 in page margins, label clearances and annotation routing are local layout choices where the guide gives no exact measurement.

**Data and identity.** U1 expands a shortened education label. U3 uses the actual 2023 year from column A, correcting the repeated 2022 tick in the source image. No Urban logo is used on these adapted figures.

## Data and provenance

The original public workbook and reference PNGs are preserved in `sources/`. Every array, source link and adaptation is recorded in `data-and-sources.json`. No data are estimated from pixels. The IEDB sample selects AUROC from the original three metrics and preserves every method and standard deviation. The last example is synthetic.

Urban typography and color are replaced by the selected settings. The Urban logo is omitted because these are adaptations. Numeric axes and grids are removed on directly labeled bars under Urban's bar-chart rule; the selected frame remains. Source and notes are separate from the chart artwork in the booklet.

## Regenerate

`MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_urban_samples.py`

Python dependencies: Matplotlib, NumPy, PyMuPDF and Pillow. Source arrays from Chen Liu's repository remain subject to [CC BY-NC 4.0](../upstream/LICENSE).
