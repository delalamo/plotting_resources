# Cobalt focus with gray context

An optional emphasis treatment for the selected R1/S3 style. [View all samples](gallery.html) · [Six-page PDF](blue-focus-gray-context.pdf) · [Overview](overview.png).

The emphasized entry is **#285F96**, the selected R1 cobalt. Background entries use opaque, neutral gray shades from **#777777** to **#B7B7B7**. Both retain **1.25 pt** strokes: the visual hierarchy comes from hue, a solid focus line, dashed comparison lines, and drawing the focus last. No extra line-weight change is needed.

The panel remains **#EBF1F5** with white margins, **Helvetica Regular**, a **0.45 pt #566C7B** four-sided frame and a **0.45 pt dotted #CBD6DF** grid. Used markers remain 3.5 pt and hollow. All type sizes stay as specified in the [selected guide](../README.md).

| Sample | Data | Purpose |
|---|---|---|
| H1 Original benchmark | Original post-training source values | A cobalt method against three gray baselines |
| H2 Learning curves | Synthetic, deterministic | One focus among five baselines; the focus is not the best performer |
| H3 A trajectory in context | Synthetic, seed 418 | One highlighted trajectory among eight references |
| H4 Crossing response curves | Synthetic, deterministic | Four gray comparisons on a log-scaled x axis |

Three-reference gray set: `#777777`, `#979797`, `#B7B7B7`.

Five-reference gray set: `#777777`, `#878787`, `#979797`, `#A7A7A7`, `#B7B7B7`.

The lightest shades deliberately recede. For close reading of every reference, use fewer, darker grays and explicit labels. Gray shades and dash styles do not uniquely identify arbitrarily many entries. The full-size examples include individual legends; the overview directly labels the blue line.

Exact sample arrays are in [data.json](data.json), and settings are in [settings.json](settings.json). Exports include 300 dpi PNG, embedded-font PDF and editable-text SVG.

```sh
MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_emphasis_examples.py
```

H1 data: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), [CC BY-NC 4.0](../upstream/LICENSE). H2-H4 are illustrative data, not new scientific measurements. The selected R1 exports are unchanged.
