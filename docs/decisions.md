# Adopted plotting decisions

The complete specification is in [style-guide.md](style-guide.md); executable
settings are in `src/plotting_resources/selected_style.json`.

| Decision | Selected setting |
|---|---|
| Palette | R1 cobalt, brick and gold, with the recorded categorical extensions |
| Plot background | Option A, `#D8E8F4` |
| Full figure background | `#EDF4F9` |
| Figure typography | Arial, 10 pt; bold figure/panel/axis titles only |
| Sources and notes | Arial Regular, 8 pt, selected 16 November 2026 |
| Outer padding | 18 pt left/right; 13.5 pt above title and below final note |
| Legends | Below plot/axis labels, with 7.5 pt clearance |
| Emphasis | Solid cobalt focus, opaque dashed gray comparisons |
| Reference height | Use the approved compact height; reflow labels when width changes, without shrinking text |
| Default width | 6.25 in native chart; 6.75 in complete padded figure, equal to article text width. Applies to figures 11, 12 and 16. |
| Wide exceptions | M1 dense labeled bars, M2 eight-panel grid, M3 annotated concept schematic |
| Minimal mode | White figure and plot backgrounds; no figure title, subtitle, source or notes; retain axis/panel labels and legends |
| Math | Arial/Arial Italic letters, STIX only for missing symbols; conventional reduced scripts |
| Retained gallery | 16 figures / 27 panels; includes the four native multi-panel figures |
| Exclusions | 3D sphere and manually assembled repository composites |

Earlier beige palettes, cool-only alternatives, above-plot legends, 50%-height
blocks and 6/7 pt footer alternatives are historical studies, not active defaults.
The reference renderers preserve original source arrays and supplied uncertainty.
New starter data are explicitly synthetic. Interactive chart behavior has not
been adopted as a requirement; current production exports are PDF, PNG and SVG.
