# Multi-panel figures: Arial, R1 and S3

[Gallery](gallery.html) · [Four-page PDF](multipanel-r1-arial-bold-axes.pdf) · [Native PNG/PDF/SVG files](figures/)

The four native multi-panel figures in the retained README examples are remade here. Numeric arrays and uncertainty values are preserved. The concept drawing retains the source generator, seed and geometry.

## Existing style applied

Arial Regular; 10 pt bold axis titles; 8.57 pt ticks and legends; 11.43 pt regular panel headings. S3 panels are #EBF1F5. Frames are #566C7B at 0.45 pt; grids are dotted #CBD6DF at 0.45 pt. Curves are 1.25 pt and error bars 0.65 pt with 2 pt caps. All agreed R1 method-color mappings are retained. Concepts use 0.08 fill opacity; publication areas retain 0.14 / 0.22 opacity.

## Layout choices for this collection

These are documented implementation choices, not new claims about Urban Institute specifications. Panel letters run left-to-right, then top-to-bottom, in the same regular 11.43 pt face as panel headings. A legend serves the entire figure and sits above the panels. Outer titles, subtitles, sources and notes are separate page text in the booklet. Shared axes suppress redundant labels; bold titles identify the measured quantity.

| Figure | Layout | Full chart size | Panel gap |
|---|---|---|---|
| IEDB comparison | 1 x 3 | 12.5 x 4.6 in | 0.45 in horizontal |
| Brute-force composition | 2 x 4 | 13.0 x 7.5 in | 0.30 in horizontal; 0.55 in vertical |
| Concept illustration | 1 x 2 | 12.0 x 4.75 in | 0.56 in horizontal |
| Publication trends | 2 x 1 | 11.5 x 7.5 in | 0.82 in vertical |

Full-grid widths preserve the agreed point sizes at native export dimensions. PNGs are 300 dpi; PDF fonts are embedded and SVG text is editable. The concept retains the existing DejaVu Sans math setting, including its STIX symbol fallback.

## Data and comparison decisions

- Benchmark bars start at zero, share 0-1.04 limits and retain every supplied mean and standard deviation. Three-decimal labels replace numeric ticks and grids. The original method order and nine-category palette are preserved.
- Composition retains all eight panels and 224 segments. Numbered model keys, shared probability scales and 7.5 pt dense value labels keep the complete source data visible. Stack totals of 0.999-1.001 reflect source rounding and are not normalized.
- Concept panel edges align; the schematic receives more width. Its 5,200 source points and original trajectories are preserved. Its annotations and arrows are repositioned or resized only for readability.
- Publication panels use the same 0-125 count scale. All 132 monthly counts and their cumulative sums are unchanged. Source events without an exact match in the original month vector remain omitted; the omissions are listed in validation.json. Event labels are historical source content, not independently verified release dates.

## Reproduce

`MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_multipanel_examples.py`

Dependencies: Matplotlib, NumPy, SciPy, PyMuPDF and Pillow; Arial Regular and Arial Bold must be installed. Original code and data: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), [CC BY-NC 4.0](../upstream/LICENSE).
