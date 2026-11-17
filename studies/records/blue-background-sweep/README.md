# Blue plot-background sweep

[Eight-page PDF in article context](blue-backgrounds-in-article.pdf) / [Scrolling comparison](gallery.html) / [Overview](overview.png)

Eight proposed plot backgrounds, ordered from lighter to darker. The outer figure background is fixed at **#EDF4F9**, and the article page is white. **Option A (#D8E8F4) is selected.** It is now the default in [the style guide](../README.md) and [selected-style.json](../selected-style.json). The other options remain as comparison artifacts.

| Option | Plot background |
|---|---|
| **A - selected** | `#D8E8F4` |
| B | `#D3E5F2` |
| C | `#CEE1F0` |
| D | `#C9DEED` |
| E | `#C4DBEA` |
| F | `#BFD8E7` |
| G | `#BAD4E4` |
| H | `#B5D1E1` |

Each page repeats the same T1 line plot and lorem ipsum prose. The original chart is 6.25 inches wide, placed without rescaling on a US Letter page. Plot and figure text remains 10 pt Arial, with bold figure and axis titles; other figure text is regular. The existing directly labeled series retain their R1 colors, line widths, markers, values and spacing. Direct labels mean this particular chart needs no legend. Article body text is 11 pt Arial, and its headline is 19 pt Arial bold.

All figure headings, sources and notes sit inside an #EDF4F9 block with 18 pt padding. The title-to-subtitle gap is 4 pt, and subtitle-to-visible-chart-content clearance is 11 pt. The illustration is repeated intentionally to isolate the background change. Source credits and the existing data are preserved; lorem ipsum prose makes no claim about the data.

The PDF embeds Arial and preserves vector charts. Native PNG/PDF/SVG files are in `figures/`. The HTML embeds all SVGs and preserves native chart width, with horizontal scrolling on narrow displays. Review at 100% zoom.

Reproduce with `MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_blue_background_sweep.py`.
