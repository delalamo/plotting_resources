# Setup and regeneration

Python 3.10 or newer is required. Arial Regular, Bold and Italic must be installed
on the machine; the renderer fails clearly if they are missing. Arial font files
are not bundled with the repository. PDFs embed the fonts used in each figure.

From the repository root:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[examples]'
python -m unittest discover -s tests
python templates/render_all.py
python examples/reference_gallery/render.py
python templates/render_all.py --minimal
python examples/reference_gallery/render.py --minimal
```

On Windows, activate with `.venv\Scripts\activate` instead. The `examples` extra
adds PDF review, image and scientific dependencies; the library itself needs
Matplotlib and NumPy. The template and reference runners select a headless
backend. In a headless custom script, use `MPLBACKEND=Agg` or select that backend
before importing plotting helpers.

Outputs:

| Command | Output |
|---|---|
| `python templates/line_plot.py` | `build/templates/line_plot.pdf`, `.png`, `.svg` and layout report |
| `python templates/render_all.py` | All nine examples, combined PDF, HTML gallery and portable source ZIP in `build/templates/` |
| `python examples/reference_gallery/render.py` | Current 16-figure gallery and article proof in `build/reference-gallery/figures4papers-minimal/` |

Set `PAPER_OUTPUT_DIR` to change the template export directory. The library can
also be installed in another project with `pip install /path/to/plotting_resources`.
The JSON style file is packaged with the library. Editable installation makes
changes to the checked-out package and settings available immediately.

Minimal mode removes figure title, subtitle, source and notes, and uses white figure and plot backgrounds. Outputs go into `build/templates/minimal/` or `build/reference-gallery/minimal/figures4papers-minimal/`. Styled outputs are retained.
