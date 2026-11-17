# Math and spacing review

Reviewed against the public Urban Institute guide and its official print-theme source on 2026-11-15.

## Reference check

The [published guide](https://urbaninstitute.github.io/graphics-styleguide/#chart-parts) places legends above charts, orders them to match the data, and calls for left-aligned titles. Its [small-multiple guidance](https://urbaninstitute.github.io/graphics-styleguide/#creating-effective-charts) calls for matching panel dimensions and scales for comparable charts. Its usual PDF figure width is 6.25 inches. It does not prescribe exact gaps for these mixed scientific layouts.

The [official R print theme](https://github.com/UrbanInstitute/urbnthemes/blob/master/R/theme_urbn_print.R) supplies implementation defaults: 6 pt panel spacing; 4 pt x-tick-label margin; 8 pt x-axis-title and 4 pt y-axis-title margins; 10 pt title/subtitle bottom margins; 6 pt top/bottom legend margins. These are defaults, not a complete multi-panel specification.

## What was polished

- Benchmark and composition horizontal panel gaps now use 6 pt. Panel widths remain equal within each grid; the recovered width also separates numeric labels more clearly.
- Legends extend across their associated plotting region, in data order. The concept legend applies only to the left panel.
- Legends sit below the complete plot and its axis labels, with a measured 7.5 pt clearance. Separate legend groups have 4.5 pt between them. This is the user-selected override to Urban's above-chart convention.
- The compact revision uses 6 pt x-title and 4 pt y-title padding, 3 pt x-tick padding and 4 pt y-tick padding. Matplotlib padding is measured from its tick-label box; this is an adaptation of the R margins, not a promise of pixel-identical output.
- Figure titles sit 3 pt above subtitles. Subtitles sit 8.25 pt above the first chart content, including panel headings (6 pt placement gap plus 2.25 pt export padding). Chart height and vertical gaps retain the approved 75%-height layout. Source/notes now use 8 pt, and article blocks fit their content with equal 13.5 pt top and bottom padding, without changing chart geometry. Timeline annotations are staggered to fit.
- The 0.4125-inch composition row gap and 0.615-inch timeline row gap leave space for panel headings and shared axes. The 0.56-inch mixed concept gap remains a local choice.

## Retained project choices

All figures remain 13 inches wide, on 14 x 10-inch booklet pages, to preserve the agreed 10 pt type across the full grids. This differs from Urban's usual print width. Font, weight, palette, backgrounds and four-sided frames remain our selected overrides. These are Urban-informed layouts, not exact Urban reproductions.

## Math correction

Formula strings are restored from the original concept code. [Matplotlib Mathtext](https://matplotlib.org/stable/users/explain/text/mathtext.html) renders subscripts, superscripts, conditional bars, the empty-set symbol and calligraphic manifold symbols. Equations have a 10 pt base; normal subscript/superscript reduction produces 7 pt script glyphs. Letters use Arial/Arial Italic; STIX supplies symbols missing from Arial. Equations are not bold. The concept SVG outlines its glyphs for portable rendering; the other SVGs retain editable text.

## Measured clearances

| Figure | Plot labels to legend below | Minimum adjacent value-label gap |
|---|---:|---:|
| iedb-three-metrics | 7.50 pt | 6.17 pt |
| brute-force-eight-panels | 7.50 pt | 4.12 pt |
| concept-two-panels | 7.50 pt | Not applicable |
| publication-trends-two-panels | 7.50 pt | Not applicable |

`validation.json` records geometry and data checks; `font-verification.json` checks the exported font faces, point sizes, embedding and text bounds.
