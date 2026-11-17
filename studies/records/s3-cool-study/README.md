# S3: five cooler palettes

S3 is the selected direction for this comparison. These five **palette candidates** keep its entire non-color treatment fixed; no new palette is selected yet. The earlier B exports and S3 reference are preserved.

[Compare the figures](gallery.html) · [Nine-page comparison](s3-cool-palettes.pdf) · [Line overview](overview.png) · [Nine-category comparison](bars-overview.png)

## What stays fixed

- Panel **#EBF1F5**, white figure margins **#FFFFFF**.
- **Helvetica Regular**: 10 pt axis labels, 8.57 pt ticks/legends, 11.43 pt panel titles; existing dense annotation sizes and DejaVu Sans math retained.
- Curves **1.25 pt**; errors **0.65 pt** with 2 pt caps; hollow markers **3.5 pt**.
- Four-sided **#566C7B** frame at **0.45 pt**; dotted xy grid **#CBD6DF** at **0.45 pt**; 2 pt ticks.
- Bar width 0.70; bar outline 0.35 pt. Concept fill 0.08; trend fill 0.14 / 0.22; radar fill 0.035. Original shapes, dashes, positions, ranges, values and uncertainty remain fixed.
- Text #282828, secondary text #666666, hatches #707070. Only the data palette, including the diagram prior color, varies.

## Research and interpretation

Sources accessed 2026-11-15. These references establish design precedents for hue relationships, not evidence that any palette is unused in science. The palette recommendations and their adaptation to S3 are design judgments. No full source palette is copied; paint names are not represented as calibrated sRGB conversions.

### N. [Nord: Colors and Palettes](https://www.nordtheme.com/docs/colors-and-palettes/)

Frost pairs blue-green, cyan and muted blue with pale blue-gray Snow Storm surfaces. Frost: #8FBCBB, #88C0D0, #81A1C1, #5E81AC.

C1 uses the related-hue idea with substantially darker marks for a light plotting panel.

### I. [IBM Carbon: Data visualization color palettes](https://www.carbondesignsystem.com/building-blocks/data-visualization/color-palettes)

Carbon separates categories with purple, cyan and deep teal, alongside other families; sequence matters. Examples: purple #6929C4, cyan #1192E8, teal #005D5D.

C5 uses this wider cool-hue spacing, with original, quieter colors. It is not the Carbon palette.

### J. [Jotun: Calm blue, fresh and airy bedroom colours](https://www.jotun.com/in-en/decorative/inspiration/indoor/rooms/bedroom/calm-bluefresh-and-airy)

The interior guidance groups blue, lavender, mint and green with white and light gray. Hue families, not paint-to-hex conversions: blue / lavender / mint / green.

C2, C3 and C4 explore these relationships in darker ink-like colors appropriate to small marks.

### U. [USWDS: System color tokens](https://designsystem.digital.gov/design-tokens/color/system-tokens/)

The blue-cool family spans a pale surface through medium and deep blue-green shades. Examples: #E7F2F5 at grade 5; #3A7D95 at 50; #224A58 at 70.

Across the proposals, use depth as well as hue to distinguish marks on a pale blue surface.

## The five proposals

I would start with **C2 Glacial iris**: indigo, deep sea glass and dusty iris give a coherent cool identity with broader hue separation than related blues alone. C1 is quieter, C3 more marine, C4 more violet, and C5 more vivid.

The first three swatches are the core: signature / companion 1 / companion 2. In the line and radar examples these map to VIGIL / DPO / DA-DPO.

| Option | Signature | Companion 1 | Companion 2 | Full six-example gallery |
|---|---|---|---|---|
| C1 Fjord | #274E70 | #216F7A | #71839B | [PDF](fjord/gallery.pdf) |
| C2 Glacial iris | #414F86 | #237F78 | #947AA5 | [PDF](glacial-iris/gallery.pdf) |
| C3 Sea glass | #205B63 | #4B8176 | #668DB4 | [PDF](sea-glass/gallery.pdf) |
| C4 Blue hour | #343E70 | #5974AF | #9581A3 | [PDF](blue-hour/gallery.pdf) |
| C5 Arctic signal | #184D91 | #188C9A | #8055A7 | [PDF](arctic-signal/gallery.pdf) |

### C1 Fjord

Navy, glacier teal and dusty steel; the quietest option.

A restrained blue-gray identity close to the panel color. The related blues rely more on marker shapes and labels.

| Role | Name | Hex |
|---|---|---|
| Signature | Deep fjord | `#274E70` |
| Companion 1 | Glacier teal | `#216F7A` |
| Companion 2 | Dusty steel | `#71839B` |
| Extended 4 | Harbor blue | `#496B8C` |
| Extended 5 | Sea pine | `#487F75` |
| Extended 6 | Storm iris | `#626988` |
| Extended 7 | Supporting category | `#52616E` |
| Extended 8 | Supporting category | `#8A8297` |
| Extended 9 | Supporting category | `#284B53` |
| Diagram prior | Cool neutral | `#74828D` |

Opaque core contrast against S3: 7.649:1, 5.093:1, 3.4:1.

**methods mapping, in original source order**

DPO: `#216F7A`; DA-DPO: `#71839B`; VIGIL (Ours): `#274E70`.

**comparison mapping, in original source order**

Prime-2.1: `#52616E`; NetMHCpan: `#626988`; MHCnuggets: `#8A8297`; MHCflurry: `#496B8C`; DeepNeo: `#216F7A`; BigMHC-EL: `#487F75`; BigMHC-IM: `#284B53`; BigMHC$_\text{retrained}$: `#71839B`; ImmunoStruct (ours): `#274E70`.

**composition mapping, in original source order**

DeepSeek R1 Distill Qwen 1.5B: `#274E70`; DeepSeek R1 Distill Qwen 14B: `#216F7A`; DeepSeek R1 Distill Llama 70B: `#71839B`; deepseek-chat (Deepseek-V3): `#496B8C`; deepseek-reasoner (Deepseek-R1): `#487F75`; gemini-2.5-flash-preview-04-17: `#626988`; OpenAI o3: `#52616E`.


### C2 Glacial iris

Indigo, sea glass and dusty iris; calm with a distinct identity.

My preferred balance of cohesion and category separation. Expanded palettes still need stable labels when many series overlap.

| Role | Name | Hex |
|---|---|---|
| Signature | Indigo ink | `#414F86` |
| Companion 1 | Deep sea glass | `#237F78` |
| Companion 2 | Dusty iris | `#947AA5` |
| Extended 4 | Clear slate | `#527EAA` |
| Extended 5 | Dusk blue | `#526A94` |
| Extended 6 | Blue spruce | `#497C92` |
| Extended 7 | Supporting category | `#677887` |
| Extended 8 | Supporting category | `#725B87` |
| Extended 9 | Supporting category | `#2E5461` |
| Diagram prior | Cool neutral | `#74808D` |

Opaque core contrast against S3: 6.859:1, 4.21:1, 3.3:1.

**methods mapping, in original source order**

DPO: `#237F78`; DA-DPO: `#947AA5`; VIGIL (Ours): `#414F86`.

**comparison mapping, in original source order**

Prime-2.1: `#677887`; NetMHCpan: `#497C92`; MHCnuggets: `#725B87`; MHCflurry: `#527EAA`; DeepNeo: `#237F78`; BigMHC-EL: `#526A94`; BigMHC-IM: `#2E5461`; BigMHC$_\text{retrained}$: `#947AA5`; ImmunoStruct (ours): `#414F86`.

**composition mapping, in original source order**

DeepSeek R1 Distill Qwen 1.5B: `#414F86`; DeepSeek R1 Distill Qwen 14B: `#237F78`; DeepSeek R1 Distill Llama 70B: `#947AA5`; deepseek-chat (Deepseek-V3): `#527EAA`; deepseek-reasoner (Deepseek-R1): `#526A94`; gemini-2.5-flash-preview-04-17: `#497C92`; OpenAI o3: `#677887`.


### C3 Sea glass

Lagoon, muted jade and glazed blue; the greenest cool option.

A soft marine identity with little violet. Adjacent teal/green hues are less distinct in dense categorical plots.

| Role | Name | Hex |
|---|---|---|
| Signature | Deep lagoon | `#205B63` |
| Companion 1 | Mineral jade | `#4B8176` |
| Companion 2 | Glazed blue | `#668DB4` |
| Extended 4 | Ocean blue | `#3A728D` |
| Extended 5 | Weathered aqua | `#6C8992` |
| Extended 6 | Marine slate | `#405C7B` |
| Extended 7 | Supporting category | `#5D6D72` |
| Extended 8 | Supporting category | `#748676` |
| Extended 9 | Supporting category | `#304C56` |
| Diagram prior | Cool neutral | `#72858A` |

Opaque core contrast against S3: 6.732:1, 3.921:1, 3.055:1.

**methods mapping, in original source order**

DPO: `#4B8176`; DA-DPO: `#668DB4`; VIGIL (Ours): `#205B63`.

**comparison mapping, in original source order**

Prime-2.1: `#5D6D72`; NetMHCpan: `#405C7B`; MHCnuggets: `#748676`; MHCflurry: `#3A728D`; DeepNeo: `#4B8176`; BigMHC-EL: `#6C8992`; BigMHC-IM: `#304C56`; BigMHC$_\text{retrained}$: `#668DB4`; ImmunoStruct (ours): `#205B63`.

**composition mapping, in original source order**

DeepSeek R1 Distill Qwen 1.5B: `#205B63`; DeepSeek R1 Distill Qwen 14B: `#4B8176`; DeepSeek R1 Distill Llama 70B: `#668DB4`; deepseek-chat (Deepseek-V3): `#3A728D`; deepseek-reasoner (Deepseek-R1): `#6C8992`; gemini-2.5-flash-preview-04-17: `#405C7B`; OpenAI o3: `#5D6D72`.


### C4 Blue hour

Indigo, periwinkle and ash violet; a more tonal blue-purple look.

A distinctive violet-leaning direction for a small number of series. Dense blue-purple categories need careful labels and ordering.

| Role | Name | Hex |
|---|---|---|
| Signature | Night indigo | `#343E70` |
| Companion 1 | Periwinkle | `#5974AF` |
| Companion 2 | Ash violet | `#9581A3` |
| Extended 4 | Deep denim | `#46658D` |
| Extended 5 | Lake slate | `#597B98` |
| Extended 6 | Smoky iris | `#5A5B8F` |
| Extended 7 | Supporting category | `#69768E` |
| Extended 8 | Supporting category | `#89879B` |
| Extended 9 | Supporting category | `#3E5265` |
| Diagram prior | Cool neutral | `#798293` |

Opaque core contrast against S3: 8.909:1, 4.058:1, 3.1:1.

**methods mapping, in original source order**

DPO: `#5974AF`; DA-DPO: `#9581A3`; VIGIL (Ours): `#343E70`.

**comparison mapping, in original source order**

Prime-2.1: `#69768E`; NetMHCpan: `#5A5B8F`; MHCnuggets: `#89879B`; MHCflurry: `#46658D`; DeepNeo: `#5974AF`; BigMHC-EL: `#597B98`; BigMHC-IM: `#3E5265`; BigMHC$_\text{retrained}$: `#9581A3`; ImmunoStruct (ours): `#343E70`.

**composition mapping, in original source order**

DeepSeek R1 Distill Qwen 1.5B: `#343E70`; DeepSeek R1 Distill Qwen 14B: `#5974AF`; DeepSeek R1 Distill Llama 70B: `#9581A3`; deepseek-chat (Deepseek-V3): `#46658D`; deepseek-reasoner (Deepseek-R1): `#597B98`; gemini-2.5-flash-preview-04-17: `#5A5B8F`; OpenAI o3: `#69768E`.


### C5 Arctic signal

Clear blue, deep cyan and mineral violet; the most vivid option.

More visible color separation and a stronger digital presence. The saturated accents draw more attention than the quieter options.

| Role | Name | Hex |
|---|---|---|
| Signature | Arctic blue | `#184D91` |
| Companion 1 | Deep cyan | `#188C9A` |
| Companion 2 | Mineral violet | `#8055A7` |
| Extended 4 | Glacier blue | `#3D82AE` |
| Extended 5 | Ocean green | `#426F70` |
| Extended 6 | Cold iris | `#5C60A3` |
| Extended 7 | Supporting category | `#5F748B` |
| Extended 8 | Supporting category | `#8A719D` |
| Extended 9 | Supporting category | `#254F66` |
| Diagram prior | Cool neutral | `#6E8092` |

Opaque core contrast against S3: 7.346:1, 3.507:1, 4.883:1.

**methods mapping, in original source order**

DPO: `#188C9A`; DA-DPO: `#8055A7`; VIGIL (Ours): `#184D91`.

**comparison mapping, in original source order**

Prime-2.1: `#5F748B`; NetMHCpan: `#5C60A3`; MHCnuggets: `#8A719D`; MHCflurry: `#3D82AE`; DeepNeo: `#188C9A`; BigMHC-EL: `#426F70`; BigMHC-IM: `#254F66`; BigMHC$_\text{retrained}$: `#8055A7`; ImmunoStruct (ours): `#184D91`.

**composition mapping, in original source order**

DeepSeek R1 Distill Qwen 1.5B: `#184D91`; DeepSeek R1 Distill Qwen 14B: `#188C9A`; DeepSeek R1 Distill Llama 70B: `#8055A7`; deepseek-chat (Deepseek-V3): `#3D82AE`; deepseek-reasoner (Deepseek-R1): `#426F70`; gemini-2.5-flash-preview-04-17: `#5C60A3`; OpenAI o3: `#5F748B`.

## Reading and reuse

The three-color core is the preferred identity. The additional six colors support the existing dense examples; an analogous nine-color palette is not universally distinguishable. Keep labels, spatial positions, marker shapes and dashes. Do not treat these categorical lists as quantitative sequential scales.

All nine opaque category colors exceed 3:1 against the fixed panel. This does not certify small antialiased marks, category-to-category distinction, text, or translucent fills. `validation.json` contains contrast values and normal/protan/deutan/tritan/grayscale distance checks. Close pairs in broad palettes are recorded rather than hidden. Full-figure grayscale and deutan previews are in `simulations/`.

## Reproduce

```sh
MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_s3_cool_study.py
```

Definitions: [s3_cool_palettes.py](../s3_cool_palettes.py). Renderer: [render_s3_cool_study.py](../render_s3_cool_study.py). Exact fixed tokens, category mappings and expanded palettes: [palettes.json](palettes.json).

Thirty individual figures are exported as 300 dpi PNG, embedded-font PDF and editable-text SVG, plus five six-page galleries. The nine-page comparison uses compact proof charts from the same source data; the individual exports preserve the full original geometry. No sphere or manually assembled composites are included.

Figures and data derive from [Chen Liu, figures4papers](https://github.com/ChenLiu-1996/figures4papers), commit `0ddfbd3fc9892e804a3fa01ae46bd0d32617f2aa`, under [CC BY-NC 4.0](../upstream/LICENSE). Original labels and potentially truncated axes are retained for like-for-like comparison. The conceptual examples are illustrative, not new experimental observations.
