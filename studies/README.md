# Design history

- `scripts/`: earlier palette, background, emphasis and typography experiments,
  plus the original beige-theme adapters.
- `records/`: saved study settings, data, source notes, measurements and decisions.
  Historical settings are snapshots, not the current default.
- `early/`: the earlier R/style investigations preserved in their original form.

The current authoritative settings are
`src/plotting_resources/selected_style.json`; the current guide is
`docs/style-guide.md`.

The main Python study scripts expect the legacy flat working directory. Prepare
it with the reference-gallery runner, then execute the chosen copied study script
inside `build/reference-gallery/figures4papers-minimal/`. Some studies depend on
earlier study outputs and their original settings. Their README files are
historical records; old absolute/local paths and relative export links are not
the current installation instructions. Use `docs/setup.md` for current setup.

Full historical PDF/image/ZIP exports remain in the local ignored
`build/legacy/` snapshot. They are not required to create new figures or rebuild
the current reference gallery.
