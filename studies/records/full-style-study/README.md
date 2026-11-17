# Full plotting-style exploration

**Eight complete directions; Helvetica typography fixed.** [Open gallery](gallery.html) · [Visual study PDF](style-exploration.pdf) · [Overview](overview.png)

This expands the earlier palette study to panel and page backgrounds, frame visibility/color/weight, curve and error-bar weights, grids, ticks, markers, bar width/outlines, hatching and fill opacity. The approved default remains in the parent directory.

## Fixed typography and data

Helvetica Regular is used throughout: 10 pt axis labels, 8.57 pt ticks/legends and 11.43 pt panel titles. The original dense-annotation sizes and DejaVu Sans math font are preserved. No font-family, weight or size changes were applied to the six examples. Each example retains its physical canvas size, source values, method order, uncertainty values and axis ranges. Bar widths vary around fixed centers; colors and style do not alter the quantities.

The sphere and original assembled composites remain excluded. All six source examples are available in each style as 300 dpi PNG, native PDF and editable SVG. The overview/profile pages are comparison sheets, not replacement scientific datasets.

## Complete directions

| Style | Panel / figure | Curve | Frame | Grid | Marker |
|---|---|---|---|---|---|
| [S1 Porcelain precision](porcelain/gallery.pdf) | `#FFFFFF` / `#FFFFFF` | 0.85 pt | left-bottom, 0.45 pt | none, 0.45 pt | 3.0 pt, open |
| [S2 Warm editorial](warm-editorial/gallery.pdf) | `#F6F0E4` / `#F6F0E4` | 1.65 pt | box, 0.65 pt | y, 0.4 pt | 4.0 pt, filled |
| [S3 Mineral grid](mineral-grid/gallery.pdf) | `#EBF1F5` / `#FFFFFF` | 1.25 pt | box, 0.45 pt | xy, 0.45 pt | 3.5 pt, open |
| [S4 Sage field](sage-field/gallery.pdf) | `#EBF0E3` / `#F7F9F2` | 1.55 pt | bottom, 0.65 pt | y, 0.8 pt | 4 pt, filled |
| [S5 Rose atlas](rose-atlas/gallery.pdf) | `#F5E9E8` / `#FCF8F5` | 1.4 pt | left-bottom, 0.6 pt | y, 0.4 pt | 4.5 pt, open |
| [S6 Sandstone bold](sandstone/gallery.pdf) | `#EADCC4` / `#EADCC4` | 2.25 pt | box, 1.05 pt | none, 0.45 pt | 5.1 pt, filled |
| [S7 Graphite + one accent](graphite/gallery.pdf) | `#F0F1EF` / `#FFFFFF` | 1.8 pt | none, 0.55 pt | y, 0.9 pt | 4.2 pt, open |
| [S8 Night studio](night-studio/gallery.pdf) | `#202B35` / `#17212A` | 2.0 pt | box, 0.6 pt | y, 0.55 pt | 4.8 pt, open |

## Controlled comparisons

- [Nine backgrounds](backgrounds.png): only the panel color varies; P2 palette, 1.15 pt curves, black frame and typography stay fixed.
- [Six curve weights](line-weights.png): only curve width changes from 0.65 to 2.3 pt. Markers and their outlines stay fixed.
- [Six axes/grid treatments](axes-grids.png): compare boxed, open, bottom-only and frameless treatments.
- [Markers and fills](markers-fills.png): hollow/filled markers crossed with 0%, 12% and 30% area opacity. These overlapping fills are visual proofs, not new uncertainty bands.

## Choosing a direction

S2 is my all-round recommendation; S3 provides a technical look; S5 is a more distinctive light treatment. S6 and S8 explore presentation-oriented extremes. It is reasonable to combine, for example, the S5 background with S2 curve weight and S1 open axes. Recheck contrast after mixing tokens.

### S1 Porcelain precision

White paper, open axes, delicate strokes and hollow markers.

Best use: Compact paper figures and dense technical comparisons. Tradeoff: Fine strokes are less prominent on projected slides.

Core palette (signature, companion 1, companion 2): `#385A7C`, `#984C35`, `#7B8246`.

Extended colors: `#8A6081`, `#337D79`, `#9A773B`, `#6E7882`, `#986D66`, `#596448`.

Text `#282828`; secondary text `#666666`; frame `#000000`; grid `#E3DCCF`; neutral `#827C73`.

Error bars 0.55 pt, caps 1.5 pt; bar width 0.62, bar outline 0 pt. Distribution alpha 0.04; trend fill alphas [0.08, 0.13]; radar alpha 0.

Core contrast on its panel: 7.19:1, 6.14:1, 4.10:1.

[Six examples](porcelain/gallery.pdf) · [Profile](porcelain/profile.png)

### S2 Warm editorial

Continuous warm paper, aubergine accents and medium-weight curves.

Best use: A balanced research identity across papers and talks. Tradeoff: The tinted page is more visible when inserted into a white manuscript.

Core palette (signature, companion 1, companion 2): `#68445F`, `#9B7B30`, `#367B82`.

Extended colors: `#B16F7A`, `#727E4F`, `#55749A`, `#786F78`, `#A46B49`, `#4E6459`.

Text `#282828`; secondary text `#666666`; frame `#000000`; grid `#DED5C5`; neutral `#827A7B`.

Error bars 0.8 pt, caps 2 pt; bar width 0.76, bar outline 0 pt. Distribution alpha 0.12; trend fill alphas [0.2, 0.3]; radar alpha 0.035.

Core contrast on its panel: 7.17:1, 3.51:1, 4.29:1.

[Six examples](warm-editorial/gallery.pdf) · [Profile](warm-editorial/profile.png)

### S3 Mineral grid

Cool blue-gray panels, fine dotted grids and restrained frames.

Best use: Technical comparisons where reading values matters. Tradeoff: The denser grid adds structure but can compete with complex data.

Core palette (signature, companion 1, companion 2): `#385A7C`, `#984C35`, `#7B8246`.

Extended colors: `#8A6081`, `#337D79`, `#9A773B`, `#6E7882`, `#986D66`, `#596448`.

Text `#282828`; secondary text `#666666`; frame `#566C7B`; grid `#CBD6DF`; neutral `#827C73`.

Error bars 0.65 pt, caps 2 pt; bar width 0.7, bar outline 0.35 pt. Distribution alpha 0.08; trend fill alphas [0.14, 0.22]; radar alpha 0.035.

Core contrast on its panel: 6.31:1, 5.39:1, 3.60:1.

[Six examples](mineral-grid/gallery.pdf) · [Profile](mineral-grid/profile.png)

### S4 Sage field

Pale sage fields, white reference lines and an open top edge.

Best use: Soft, distinctive plots and conceptual illustrations. Tradeoff: White gridlines are deliberately subtle; small print needs inspection.

Core palette (signature, companion 1, companion 2): `#5F3C61`, `#9B6135`, `#377264`.

Extended colors: `#986C77`, `#6C7B42`, `#496D8A`, `#737A6C`, `#966651`, `#4F5D49`.

Text `#282828`; secondary text `#666666`; frame `#5B6755`; grid `#FFFFFF`; neutral `#767D6E`.

Error bars 0.75 pt, caps 2 pt; bar width 0.82, bar outline 0 pt. Distribution alpha 0.2; trend fill alphas [0.27, 0.39]; radar alpha 0.055.

Core contrast on its panel: 7.85:1, 4.36:1, 4.82:1.

[Six examples](sage-field/gallery.pdf) · [Profile](sage-field/profile.png)

### S5 Rose atlas

Rose paper, petrol curves, hollow markers and open axes.

Best use: A calm editorial alternative with more color in the surface. Tradeoff: Rose and gold need redundant labels when hues become hard to distinguish.

Core palette (signature, companion 1, companion 2): `#235E63`, `#AD647A`, `#938044`.

Extended colors: `#6F6D98`, `#708355`, `#B16C45`, `#7C7A74`, `#4F7894`, `#87545D`.

Text `#282828`; secondary text `#666666`; frame `#715C61`; grid `#DECBCB`; neutral `#817C75`.

Error bars 0.7 pt, caps 2 pt; bar width 0.72, bar outline 0 pt. Distribution alpha 0.1; trend fill alphas [0.18, 0.28]; radar alpha 0.035.

Core contrast on its panel: 6.21:1, 3.63:1, 3.27:1.

[Six examples](rose-atlas/gallery.pdf) · [Profile](rose-atlas/profile.png)

### S6 Sandstone bold

Deeper sand, strong borders, larger markers and substantial curves.

Best use: Presentations and figures that need presence at a distance. Tradeoff: Heavier strokes and fill can crowd dense radar or composition figures.

Core palette (signature, companion 1, companion 2): `#79343F`, `#365D7A`, `#6C6B35`.

Extended colors: `#8B6038`, `#6F577D`, `#326B5E`, `#6D675F`, `#965C55`, `#48555B`.

Text `#29251F`; secondary text `#655D51`; frame `#393128`; grid `#E3DCCF`; neutral `#766A5B`.

Error bars 1.0 pt, caps 3 pt; bar width 0.84, bar outline 0.4 pt. Distribution alpha 0.25; trend fill alphas [0.3, 0.46]; radar alpha 0.065.

Core contrast on its panel: 6.54:1, 5.17:1, 4.10:1.

[Six examples](sandstone/gallery.pdf) · [Profile](sandstone/profile.png)

### S7 Graphite + one accent

Quiet grayscale comparisons, one plum accent and no enclosing frame.

Best use: Focusing attention on a target method without a nine-color legend. Tradeoff: Dense category plots require numbered positions; gray alone is insufficient.

Core palette (signature, companion 1, companion 2): `#74394F`, `#777A75`, `#454D53`.

Extended colors: `#6B6369`, `#83817B`, `#62686D`, `#858580`, `#5C6264`, `#747A75`.

Text `#282828`; secondary text `#666666`; frame `#000000`; grid `#FFFFFF`; neutral `#858580`.

Error bars 0.8 pt, caps 2 pt; bar width 0.66, bar outline 0 pt. Distribution alpha 0.06; trend fill alphas [0.1, 0.24]; radar alpha 0.035.

Core contrast on its panel: 7.59:1, 3.84:1, 7.60:1.

[Six examples](graphite/gallery.pdf) · [Profile](graphite/profile.png)

### S8 Night studio

Ink-dark surfaces, pale luminous colors and confident curves.

Best use: Dark slides, digital reading and figure presentations. Tradeoff: A presentation variant; it needs a separate light export for conventional print.

Core palette (signature, companion 1, companion 2): `#D5B7DE`, `#E5AA76`, `#80C7CF`.

Extended colors: `#E49AAF`, `#BEC985`, `#AAADE5`, `#B5BABD`, `#D4BD8D`, `#89BFA7`.

Text `#F3EEE5`; secondary text `#B6C1C7`; frame `#71808C`; grid `#42505B`; neutral `#A8B5BD`.

Error bars 0.9 pt, caps 2.5 pt; bar width 0.76, bar outline 0.35 pt. Distribution alpha 0.2; trend fill alphas [0.22, 0.32]; radar alpha 0.07.

Core contrast on its panel: 7.99:1, 7.09:1, 7.54:1.

[Six examples](night-studio/gallery.pdf) · [Profile](night-studio/profile.png)

## Encoding details

DPO, DA-DPO and VIGIL use square, triangle and circle markers. Styles with dashed curves also use dashed, dash-dot and solid lines respectively. Radar keeps solid paths and the three shapes. Open markers use the panel color inside. The gray SFT baseline remains explicitly labeled.

S7 uses a single plum highlight for the target bar and gray comparators. Numbered tick positions and matching legend prefixes identify the otherwise similar gray methods. Its composition figure also uses numbered method positions. Other styles retain the original color-based legends.

For open/frameless styles, the radar keeps its radial reference geometry but loses its enclosing rectangle. All original benchmark-specific radial mappings remain unchanged. Cartesian grid removal does not remove the radar scale guides.

Source bars preserve their truncated y ranges for comparability. The supplied uncertainty values are preserved without reinterpreting them as one uniform type of confidence interval. Concept plots remain conceptual drawings.

## Readability and export checks

The renderer checks source data geometry, fixed font sizes/family/weight, original physical canvas dimensions, and preservation of approved exports. Contrast measurements and approximate Machado color-vision simulations are diagnostic aids, not certification. Extended category sets may converge under color-vision deficiencies; light or transparent fills are not guaranteed to clear a contrast threshold. Native PDFs retain editable text; SVG requires Helvetica on the viewing system.

The complete settings and category assignments are in [styles.json](styles.json); validation results are in [validation.json](validation.json). Existing [palette research](../palette-study/README.md) informed this exploration. No new claim about historical rarity or brand exclusivity is made.

## Reproduce

```sh
python figures4papers-minimal/render_style_exploration.py
```

The same requirements as the parent project suffice. Definitions are in `../style_directions.py`. Source data and drawings: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), CC BY-NC 4.0; parent provenance and license apply.
