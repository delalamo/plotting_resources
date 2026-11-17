# Complete current-style reference review

[Complete PDF](reference-figures-r1-s3-arial-10pt.pdf) · [Page gallery](gallery.html) · [Figures and source](reference-figures-source.zip)

Sixteen reference figures across thirteen pages: six Urban/template examples, four blue-and-gray samples, two additional repository figures and four multi-panel figures. Current R1/S3 styling is applied throughout. The full figure and page background is #EDF4F9, a paler blue behind titles, subtitles, legends and source notes; plot panels retain #D8E8F4. Prior palette/background explorations are excluded.

Figure text uses 10 pt Arial, except source credits and notes, which use 8 pt Arial Regular. Figure/panel/axis titles are bold; other text is regular. Math uses Arial letters and Arial Italic variables, with STIX symbols only where Arial lacks the glyph. Math has a 10 pt base with conventional 7 pt scripts. The exact fonts in each exported PDF page are recorded in font-verification.json.

Every page is 14 x 10 inches. Single references are paired at native 6.25-inch width; larger repository charts are 13 inches wide. No chart is rescaled when placed in the document. Legends sit below the plots with 7.5 pt clearance from axis labels and 4.5 pt between separate legend groups. Titles and subtitles have a 3 pt gap; subtitles sit 8.25 pt above the chart content. Native chart dimensions retain the approved 75%-height layout. Complete article blocks now fit 8 pt source/notes with equal 13.5 pt top and bottom padding; chart geometry, widths and mark sizes remain fixed. PDF fonts are embedded, PNGs are 300 dpi, and SVGs containing math use outlined glyphs. Other SVGs retain editable text.

Sources, original arrays, synthetic-data disclosures and display adaptations accompany the figures and appear in data-and-sources.json. The Urban workbook is retained; all earlier sample arrays are checked. The radar retains benchmark-specific radial scales. Original repository code/data remain under CC BY-NC 4.0.

Reproduce with `MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_reference_collection.py`. Dependencies: Matplotlib, NumPy, SciPy, PyMuPDF, Pillow and installed Arial Regular/Bold/Italic. The renderer imports render_urban_samples.py and render_multipanel_examples.py; source archives contain all required data and the upstream concept code.
