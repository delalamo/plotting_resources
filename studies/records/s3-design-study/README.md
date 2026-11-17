# S3: mixed warm/cool design palettes

This revision responds to the rejected C1-C5 study: the background is a quiet pale blue-gray surface, while plotted colors span warm and cool families. **R1 is selected**: cobalt / brick / gold on S3. See the [current style guide](../README.md). R2-R5 remain comparison alternatives.

[Compare all examples](gallery.html) · [Nine-page comparison PDF](s3-design-palettes.pdf) · [Overview](overview.png) · [Nine-category comparison](bars-overview.png)

## Actual design precedents

Research accessed 2026-11-15. Sources contain pale-blue or blue-gray surroundings and mixed accent colors; none is claimed to use the exact S3 hex. Findings below are sourced; the translation into plotting colors is our design interpretation. No complete brand palette is reproduced, and no paint-to-sRGB match is claimed.

### G. [Gisbert Poppler: Garden Home, reported by Yatzer](https://www.yatzer.com/garden-house-gisbert-poppler)

Design publication with designer interview and project photographs. The project combines light blue, crimson red and mustard yellow; green and orange appear elsewhere.

R1 keeps blue/red/gold as its core and uses the other hue families in the expanded set.

### P. [Pinterest Palette 2026](https://business.pinterest.com/pinterest-palette/)

Primary source: published digital palette. Cool Blue #D7EFFF appears with Plum Noir #351E28, Persimmon #FF5C34, Wasabi #E9F056 and Jade #AEB8A0.

R2 borrows the plum/orange/yellow-green relationship. Orange and citron are darkened for thin marks; the full source palette is not copied.

### T. [Temp Project: Gunia showroom, architect-supplied description](https://www.archdaily.com/1039360/gunia-project-showroom-temp-project)

Primary source: description provided by the architects. The architects describe greens, blues, pale pinks and soft beige alongside retained wooden panels and mahogany cabinets.

R3 uses cocoa, rose and jade on S3, adapting the material/color relationships into darker plotting inks.

### H. [Gunia Project: Hospitality Design project report](https://hospitalitydesign.com/news/gunia-project-store-kyiv-ukraine/183578/)

Design publication: project report. The report specifically identifies chocolate brown with pale blue, and also describes sky blue, green and flower pink.

This supports the pale-blue/brown relationship in R3; rose and jade keep its categories varied.

### B. [Benjamin Moore: complementary color combinations](https://www.benjaminmoore.com/en-us/color-overview/color-insights/complementary-colors-guide)

Primary source: manufacturer design guidance. A blue room illustration opens into orange; another example pairs turquoise tiles with orange-red cabinetry.

R4 shifts that relationship to petrol and coral on a pale blue-gray panel.

### L. [Little Greene: blue walls and yellow woodwork](https://www.littlegreene.com/advice-hub/8-interior-wall-and-skirting-board-colour-combinations)

Primary source: manufacturer design guidance. The blue/yellow example uses Grey Stone and Woad with Sunlight; another combines blue-purple with yellow highlights.

Saffron is the authored third plotting color in R4, drawing on this blue/yellow pairing.

### A. [Benjamin Moore: historical living-room color schemes](https://www.benjaminmoore.com/en-us/benjamin-moore-co-archives/living-room-color-schemes)

Primary source: manufacturer archive. The circa-1930 room has a light blue ceiling, gray-green rug, red upholstery and bright blue bookcases.

R5 interprets those accents as wine, olive and denim. These are original contemporary sRGB choices.

## Fixed background and typography

- Panel **#EBF1F5**, margins **#FFFFFF**. All original non-palette S3 tokens are fixed.
- **Helvetica Regular**, 10 pt axis labels, 8.57 pt ticks/legends, 11.43 pt panel titles. Existing smaller annotations and math settings are retained.
- Data curves **1.25 pt**, errors **0.65 pt**, caps 2 pt, hollow markers **3.5 pt**.
- Four-sided frame **#566C7B**, **0.45 pt**; dotted xy grid **#CBD6DF**, **0.45 pt**; ticks 2 pt.
- Bar width 0.70; bar outlines 0.35 pt. Fill opacities: concepts 0.08, trends 0.14 / 0.22, radar 0.035.
- Text #282828, secondary text #666666, hatches #707070. Source values, uncertainty, labels, axis ranges, geometry and method order remain fixed. Only the data palette, including the diagram prior color, changes.

## Five proposals

| Option | Signature | Companion 1 | Companion 2 | Source references | Six examples |
|---|---|---|---|---|---|
| R1 Cobalt / brick / gold | #285F96 | #B9413A | #A68517 | G | [PDF](cobalt-brick-gold/gallery.pdf) |
| R2 Plum / orange / citron | #6E354F | #BC5430 | #8B9026 | P | [PDF](plum-orange-citron/gallery.pdf) |
| R3 Cocoa / rose / jade | #67463B | #B96588 | #338269 | T, H | [PDF](cocoa-rose-jade/gallery.pdf) |
| R4 Petrol / coral / saffron | #155D68 | #C85745 | #AE811C | B, L | [PDF](petrol-coral-saffron/gallery.pdf) |
| R5 Wine / olive / denim | #863B50 | #6F813B | #5185A6 | A | [PDF](wine-olive-denim/gallery.pdf) |

The core swatches map to VIGIL / DPO / DA-DPO respectively in the line and radar examples. The expanded nine-color lists are categorical, not sequential measurement scales.

### R1 Cobalt / brick / gold

Clear blue with warm brick and mustard-gold.

Garden Home: light blue + crimson + mustard. A confident blue/red/yellow identity with a recognizable warm-cool balance.

Reading tradeoff: Blue and red can have similar grayscale value; retain the marker shapes.

| Role | Name | Hex |
|---|---|---|
| Signature | Cobalt | `#285F96` |
| Companion 1 | Brick red | `#B9413A` |
| Companion 2 | Old gold | `#A68517` |
| Extended 4 | Malachite | `#2B7C70` |
| Extended 5 | Heather rose | `#9E638C` |
| Extended 6 | Violet slate | `#685B80` |
| Extended 7 | Supporting category | `#717B7F` |
| Extended 8 | Supporting category | `#A96E45` |
| Extended 9 | Supporting category | `#5B713C` |
| Diagram prior | Neutral | `#7A7770` |

Opaque core contrast on S3: 5.819:1, 4.751:1, 3.078:1.

**methods, original source order**

DPO: `#B9413A`; DA-DPO: `#A68517`; VIGIL (Ours): `#285F96`.

**comparison, original source order**

Prime-2.1: `#717B7F`; NetMHCpan: `#685B80`; MHCnuggets: `#A96E45`; MHCflurry: `#2B7C70`; DeepNeo: `#B9413A`; BigMHC-EL: `#9E638C`; BigMHC-IM: `#5B713C`; BigMHC$_\text{retrained}$: `#A68517`; ImmunoStruct (ours): `#285F96`.

**composition, original source order**

DeepSeek R1 Distill Qwen 1.5B: `#285F96`; DeepSeek R1 Distill Qwen 14B: `#B9413A`; DeepSeek R1 Distill Llama 70B: `#A68517`; deepseek-chat (Deepseek-V3): `#2B7C70`; deepseek-reasoner (Deepseek-R1): `#9E638C`; gemini-2.5-flash-preview-04-17: `#685B80`; OpenAI o3: `#717B7F`.

### R2 Plum / orange / citron

Deep plum, orange-red and yellow-green; the most adventurous mix.

Pinterest: icy blue + plum + persimmon + yellow-green. The largest shift from S3 without changing its quiet background.

Reading tradeoff: Orange and citron move closer under red-green color-vision simulation.

| Role | Name | Hex |
|---|---|---|
| Signature | Plum wine | `#6E354F` |
| Companion 1 | Persimmon ink | `#BC5430` |
| Companion 2 | Citron | `#8B9026` |
| Extended 4 | Mineral blue | `#417899` |
| Extended 5 | Garden green | `#43775B` |
| Extended 6 | Dahlia | `#B2638A` |
| Extended 7 | Supporting category | `#687B85` |
| Extended 8 | Supporting category | `#806147` |
| Extended 9 | Supporting category | `#8671AA` |
| Diagram prior | Neutral | `#7B716E` |

Opaque core contrast on S3: 8.066:1, 4.143:1, 3.014:1.

**methods, original source order**

DPO: `#BC5430`; DA-DPO: `#8B9026`; VIGIL (Ours): `#6E354F`.

**comparison, original source order**

Prime-2.1: `#687B85`; NetMHCpan: `#B2638A`; MHCnuggets: `#806147`; MHCflurry: `#417899`; DeepNeo: `#BC5430`; BigMHC-EL: `#43775B`; BigMHC-IM: `#8671AA`; BigMHC$_\text{retrained}$: `#8B9026`; ImmunoStruct (ours): `#6E354F`.

**composition, original source order**

DeepSeek R1 Distill Qwen 1.5B: `#6E354F`; DeepSeek R1 Distill Qwen 14B: `#BC5430`; DeepSeek R1 Distill Llama 70B: `#8B9026`; deepseek-chat (Deepseek-V3): `#417899`; deepseek-reasoner (Deepseek-R1): `#43775B`; gemini-2.5-flash-preview-04-17: `#B2638A`; OpenAI o3: `#687B85`.

### R3 Cocoa / rose / jade

Warm cocoa, rose and green against the blue-gray surface.

Gunia showroom: pale blue + dark wood + pink + green. A material-inspired direction that moves the signature color away from blue.

Reading tradeoff: Rose and jade need their distinct markers in grayscale.

| Role | Name | Hex |
|---|---|---|
| Signature | Cocoa | `#67463B` |
| Companion 1 | Rose velvet | `#B96588` |
| Companion 2 | Jade | `#338269` |
| Extended 4 | Glazed blue | `#4E7C9D` |
| Extended 5 | Brass | `#A68234` |
| Extended 6 | Smoked lilac | `#7B6C9D` |
| Extended 7 | Supporting category | `#768072` |
| Extended 8 | Supporting category | `#9E5B4D` |
| Extended 9 | Supporting category | `#44636C` |
| Diagram prior | Neutral | `#80766F` |

Opaque core contrast on S3: 7.327:1, 3.491:1, 4.062:1.

**methods, original source order**

DPO: `#B96588`; DA-DPO: `#338269`; VIGIL (Ours): `#67463B`.

**comparison, original source order**

Prime-2.1: `#768072`; NetMHCpan: `#7B6C9D`; MHCnuggets: `#9E5B4D`; MHCflurry: `#4E7C9D`; DeepNeo: `#B96588`; BigMHC-EL: `#A68234`; BigMHC-IM: `#44636C`; BigMHC$_\text{retrained}$: `#338269`; ImmunoStruct (ours): `#67463B`.

**composition, original source order**

DeepSeek R1 Distill Qwen 1.5B: `#67463B`; DeepSeek R1 Distill Qwen 14B: `#B96588`; DeepSeek R1 Distill Llama 70B: `#338269`; deepseek-chat (Deepseek-V3): `#4E7C9D`; deepseek-reasoner (Deepseek-R1): `#A68234`; gemini-2.5-flash-preview-04-17: `#7B6C9D`; OpenAI o3: `#768072`.

### R4 Petrol / coral / saffron

Deep petrol balances two brighter, warmer accents.

Benjamin Moore + Little Greene: blue/orange and blue/yellow. A lively mix for curves, bars and area fills, with a dark anchor.

Reading tradeoff: The two warm colors are less distinct without hue; keep labels and dashes.

| Role | Name | Hex |
|---|---|---|
| Signature | Petrol | `#155D68` |
| Companion 1 | Coral | `#C85745` |
| Companion 2 | Saffron | `#AE811C` |
| Extended 4 | Ultramarine | `#5469A1` |
| Extended 5 | Orchid | `#9B5C85` |
| Extended 6 | Leaf green | `#6A8142` |
| Extended 7 | Supporting category | `#74818A` |
| Extended 8 | Supporting category | `#7B5643` |
| Extended 9 | Supporting category | `#8874A1` |
| Diagram prior | Neutral | `#7D7970` |

Opaque core contrast on S3: 6.589:1, 3.758:1, 3.095:1.

**methods, original source order**

DPO: `#C85745`; DA-DPO: `#AE811C`; VIGIL (Ours): `#155D68`.

**comparison, original source order**

Prime-2.1: `#74818A`; NetMHCpan: `#6A8142`; MHCnuggets: `#7B5643`; MHCflurry: `#5469A1`; DeepNeo: `#C85745`; BigMHC-EL: `#9B5C85`; BigMHC-IM: `#8874A1`; BigMHC$_\text{retrained}$: `#AE811C`; ImmunoStruct (ours): `#155D68`.

**composition, original source order**

DeepSeek R1 Distill Qwen 1.5B: `#155D68`; DeepSeek R1 Distill Qwen 14B: `#C85745`; DeepSeek R1 Distill Llama 70B: `#AE811C`; deepseek-chat (Deepseek-V3): `#5469A1`; deepseek-reasoner (Deepseek-R1): `#9B5C85`; gemini-2.5-flash-preview-04-17: `#6A8142`; OpenAI o3: `#74818A`.

### R5 Wine / olive / denim

Wine red, olive and denim; an earthy but more varied direction.

Benjamin Moore archive: pale blue + red + gray-green + blue. Closest to the original balance, with a red signature instead of blue.

Reading tradeoff: Wine and olive need redundant encoding for red-green color-vision differences.

| Role | Name | Hex |
|---|---|---|
| Signature | Wine | `#863B50` |
| Companion 1 | Olive leaf | `#6F813B` |
| Companion 2 | Denim | `#5185A6` |
| Extended 4 | Copper | `#B97638` |
| Extended 5 | Deep jade | `#2D706B` |
| Extended 6 | Rosewood | `#9F6C88` |
| Extended 7 | Supporting category | `#776B61` |
| Extended 8 | Supporting category | `#7F709D` |
| Extended 9 | Supporting category | `#A7594A` |
| Diagram prior | Neutral | `#7D786D` |

Opaque core contrast on S3: 6.691:1, 3.778:1, 3.507:1.

**methods, original source order**

DPO: `#6F813B`; DA-DPO: `#5185A6`; VIGIL (Ours): `#863B50`.

**comparison, original source order**

Prime-2.1: `#776B61`; NetMHCpan: `#9F6C88`; MHCnuggets: `#7F709D`; MHCflurry: `#B97638`; DeepNeo: `#6F813B`; BigMHC-EL: `#2D706B`; BigMHC-IM: `#A7594A`; BigMHC$_\text{retrained}$: `#5185A6`; ImmunoStruct (ours): `#863B50`.

**composition, original source order**

DeepSeek R1 Distill Qwen 1.5B: `#863B50`; DeepSeek R1 Distill Qwen 14B: `#6F813B`; DeepSeek R1 Distill Llama 70B: `#5185A6`; deepseek-chat (Deepseek-V3): `#B97638`; deepseek-reasoner (Deepseek-R1): `#2D706B`; gemini-2.5-flash-preview-04-17: `#9F6C88`; OpenAI o3: `#776B61`.

## What the checks mean

All nine opaque category colors exceed 3:1 against the panel. This is not a guarantee of category-to-category separation, small antialiased mark contrast or transparent-fill contrast. Warm/cool contrasts also have red-green color-vision limits. Retain marker shapes, dash patterns, labels and category order. Full-figure deutan/grayscale previews are provided. Numerical screens for normal, protan, deutan, tritan and grayscale appear in `validation.json`; the 0.06 Oklab close-pair flag is an editorial heuristic, not an accessibility standard.

## Files and reproduction

Thirty figures: six original examples for each of five proposals, in 300 dpi PNG, embedded-font PDF and editable-text SVG. Five six-page galleries and the nine-page report supplement those exports. The sphere and manually assembled composites remain excluded.

```sh
MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_s3_design_study.py
```

Source definitions: [s3_design_palettes.py](../s3_design_palettes.py). Renderer: [render_s3_design_study.py](../render_s3_design_study.py). Exact tokens and category mappings: [palettes.json](palettes.json).

Source figures/data: [Chen Liu, figures4papers](https://github.com/ChenLiu-1996/figures4papers), commit `0ddfbd3fc9892e804a3fa01ae46bd0d32617f2aa`, [CC BY-NC 4.0](../upstream/LICENSE). Original data and potentially truncated axes are retained for comparison. Concept examples are illustrative, not new observations.
