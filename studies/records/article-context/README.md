# Figures in a fictitious article

[Scrolling article](article-context.html) · [Complete sixteen-page PDF proof](all-16-figures-in-article-context.pdf)

All sixteen gallery figures (U1-U3, T1-T3, H1-H4, P1-P2 and M1-M4) are embedded in lorem ipsum prose, one figure per PDF page. Every figure has prose above and below it. The article page is white (#FFFFFF), complete figure blocks are pale blue (#EDF4F9), and plot panels retain #D8E8F4. Figure blocks have 18 pt horizontal padding and matching 13.5 pt top/bottom padding, measured from the title and final note text boxes and no added border or shadow. Titles, subtitles, legends, sources and notes stay inside each block. PDF bookmarks and the HTML figure index identify every example.

The charts are regenerated at shorter heights and embedded without rescaling: single plots remain 6.25 inches wide, and multi-panel charts remain 13 inches wide, preserving 10 pt Arial. The PDF uses common 14 x 14-inch review pages to fit both widths with surrounding prose. The HTML uses the same physical sizes in CSS pixels and scrolls wide figures on smaller screens. Article prose is 11 pt Arial; article headings are larger than figure titles. This typography belongs to the fictitious article, not the plotting style.

The approved chart dimensions from the 75%-height review are unchanged. Source credits and notes are 8 pt Arial Regular; all other figure text remains 10 pt with the documented math-script exception. The outer blue block fits the smaller footer, ending 13.5 pt below the last note to match the top padding. Saved footer space is removed without stretching the plot. Original data, axis limits, colors and line weights are retained. Figure titles and source notes are copied from the current collection; surrounding prose is intentionally fictitious and should not be read as an interpretation of the data. The HTML is self-contained, with SVG figures embedded as data URLs. Review at 100% browser zoom to inspect native text size.

Reproduce: `MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_article_context.py`.
