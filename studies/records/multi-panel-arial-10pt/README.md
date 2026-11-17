# Multi-panel figures: 10 pt Arial, R1 and S3

[Gallery](gallery-math-fixed.html) · [Corrected four-page PDF](multipanel-r1-arial-10pt-math-fixed.pdf) · [Native PNG/PDF/SVG files](figures/) · [Urban spacing review](SPACING_REVIEW.md)

The four native multi-panel figures in the retained README examples are remade here. Numeric arrays and uncertainty values are preserved. The concept drawing retains the source generator, seed and coordinates. Native chart dimensions retain the approved 75%-height layout. Outer article blocks fit 8 pt source/notes with equal 13.5 pt top and bottom padding; chart geometry, widths and mark sizes remain fixed.

## Existing style applied

Figure text uses 10 pt Arial; source credits and notes use 8 pt Arial Regular. Figure titles, panel titles and axis titles are bold. Panel letters, tick labels, legends, value labels, annotations, subtitles, sources and notes are regular weight. Equations use a 10 pt base with conventional reduced subscripts/superscripts, Arial letters and STIX fallback symbols. Only source credits and notes use the smaller 8 pt size; plot annotations remain 10 pt. S3 plot panels are #D8E8F4. The full figure/page background is the matching paler blue #EDF4F9, including titles, subtitles, legends, source notes, margins and gutters. Frames are #566C7B at 0.45 pt; grids are dotted #CBD6DF at 0.45 pt. Curves are 1.25 pt and error bars 0.65 pt with 2 pt caps. All agreed R1 method-color mappings are retained. Concepts use 0.08 fill opacity; publication areas retain 0.14 / 0.22 opacity.

## Layout choices for this collection

Panel letters run left-to-right, then top-to-bottom in regular weight. Shared legends sit below their associated panels, 7.5 pt beneath the lowest axis label; separate legend groups have 4.5 pt between them. Title-to-subtitle spacing is 3 pt and subtitle-to-chart-content spacing is 8.25 pt. Outer titles, subtitles, sources and notes are separate page text in the booklet. Shared axes suppress redundant labels; bold titles identify the measured quantity. The spacing review distinguishes defaults taken from Urban's R theme from local layout choices.

| Figure | Layout | Full chart size | Panel gap |
|---|---|---|---|
| IEDB comparison | 1 x 3 | 13.00 x 2.91 in | 6 pt horizontal |
| Brute-force composition | 2 x 4 | 13.00 x 5.16 in | 6 pt horizontal; 0.4125 in vertical |
| Concept illustration | 1 x 2 | 13.00 x 3.19 in | 0.56 in horizontal |
| Publication trends | 2 x 1 | 13.00 x 5.21 in | 0.615 in vertical |

All native figures are 13 inches wide; all booklet pages are 14 x 10 inches and embed charts at native scale. The gallery displays all figures with the same scale factor. PNGs are 300 dpi; PDF fonts are embedded. The concept SVG uses outlined glyphs to preserve mathematical rendering on other computers; other SVGs retain editable text. Formula labels use actual mathematical notation, including subscripts, superscripts and calligraphic symbols.

## Data and comparison decisions

- Benchmark bars start at zero, share 0-1.04 limits and retain every supplied mean and standard deviation. Three-decimal labels replace numeric ticks and grids. The original method order and nine-category palette are preserved.
- Composition retains all eight panels and 224 segments. Numbered model keys, shared probability scales and 10 pt value labels keep the complete source data visible. Stack totals of 0.999-1.001 reflect source rounding and are not normalized.
- Concept panel edges align; the schematic receives more width. Its 5,200 source points and original trajectories are preserved. Its annotations and arrows are repositioned or resized only for readability.
- Publication panels use the same 0-125 count scale. All 132 monthly counts and their cumulative sums are unchanged. Source events without an exact match in the original month vector remain omitted; the omissions are listed in validation.json. Event labels are historical source content, not independently verified release dates.

## Reproduce

`MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_multipanel_examples.py`

Dependencies: Matplotlib, NumPy, SciPy, PyMuPDF and Pillow; Arial Regular and Arial Bold must be installed. Original code and data: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), [CC BY-NC 4.0](../upstream/LICENSE).
