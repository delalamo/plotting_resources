# Source and notes font-size comparison

**Selected on 16 November 2026: 8 pt Arial Regular.** The current guide also trims the footer to equal 13.5 pt top/bottom padding. This comparison preserves the earlier fixed-height blocks; its 10 pt control was the previous default.

[Interactive comparison](comparison.html) · [PDF comparison](source-notes-size-comparison.pdf)

Candidates: **6, 7 and 8 pt Arial Regular**, with the current **10 pt** as a control. Only source credits and notes change. Figure titles, subtitles, axes, ticks, legends, annotations and values retain their existing type. Colors and source data are unchanged.

The approved 75%-height figure blocks and native chart dimensions stay fixed. The source starts at the same position; notes retain a 6 pt gap after the source. Smaller text wraps naturally, leaving any saved space at the bottom of the fixed-height block. This isolates type size from figure geometry.

The first PDF page compares all four sizes side by side at native scale. The next nine pages show the three candidates in lorem ipsum context for T1 (line chart), U1 (bar chart with longer notes) and M2 (eight-panel composition). The HTML provides footer comparisons and switches the full examples between sizes. Review at 100% zoom; fitting the entire review sheet to a window reduces the apparent font size.

This is the historical comparison used to select 8 pt. The current guide and gallery apply the selected size and balanced padding. Reproduce with `python figures4papers-minimal/render_note_size_study.py` using the existing plotting environment.
