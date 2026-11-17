# Current reference gallery

Run `python examples/reference_gallery/render.py` from the repository root after [installation](../../docs/setup.md). Add `--minimal` for white backgrounds and no figure title, subtitle, source or notes. Both modes retain axis/panel labels, legends and all original values. Outputs are separate.

- Styled: `build/reference-gallery/figures4papers-minimal/`
- Minimal: `build/reference-gallery/minimal/figures4papers-minimal/`
- Article PDF inside either root: `article-context/all-16-figures-in-article-context.pdf`
- Article HTML: `article-context/article-context.html`
- Native PDF/PNG/SVG: `reference-review-10pt/figures/`
- Gallery: `gallery.html`; combined reference PDF: `gallery.pdf`

The runner prepares a disposable workspace from versioned source and inputs, then renders four native multi-panel figures, all 16 current references, article proofs and a downloadable gallery. It verifies original data, embedded fonts, text bounds and overlaps. It never needs an old generated export.

Article figures 11 (radar), 12 (post-training) and 16 (publication trends) are now native 6.25-inch charts in 6.75-inch blocks, matching the prose column. The three retained wider examples have explicit readability reasons in the [style guide](../../docs/style-guide.md). Fonts and marks are never reduced by insertion scaling.

The `scripts/` directory preserves the specialized source-data adapters. `_workspace.py` assembles their flat working layout under ignored `build/`. Use the public runner rather than invoking these adapters from their tracked directory.
