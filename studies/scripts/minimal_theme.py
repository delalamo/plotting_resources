"""Approved style: B / light cream #FAF6EE with regular Helvetica.

Cowplot-inspired Matplotlib theme; all strokes and type sizes are in points.

This module is independent of the example data. Call apply_theme() before plotting,
then style_axes(ax) after any plot-specific overrides.
"""
from dataclasses import dataclass

import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Annotation, Text


@dataclass(frozen=True)
class Theme:
    base: float = 10.0
    small: float = 10.0 * 12 / 14
    title: float = 10.0 * 16 / 14
    line: float = 1.15
    error: float = 0.65
    grid: float = 0.45
    outline: float = 0.4
    frame: float = 0.55
    marker: float = 3.5
    ink: str = "#282828"
    muted: str = "#666666"
    grid_color: str = "#E3DCCF"
    background: str = "#FAF6EE"
    frame_color: str = "#000000"
    teal: str = "#246C68"
    rust: str = "#B2674D"
    ochre: str = "#9B8644"
    taupe: str = "#8C8275"
    scatter: str = "#3C8176"


T = Theme()
FONT_FAMILIES = ("Helvetica", "Arial", "Liberation Sans", "DejaVu Sans")

# Ordered by the original method lists; palettes affect appearance only.
PALETTES = {
    "comparison": ["#8F857A", "#C3A35A", "#CB907B", "#A08397", "#B66B4C",
                   "#9BAA85", "#778958", "#54788D", T.teal],
    "composition": ["#8EA6A0", "#5D8E83", "#316E65", "#C58E76", "#A65E45",
                    "#B2954F", "#345D78"],
    "methods": [T.rust, T.ochre, T.teal],
}


def choose_font():
    for family in FONT_FAMILIES:
        try:
            font_manager.findfont(family, fallback_to_default=False)
            return family
        except ValueError:
            pass
    return "DejaVu Sans"


FONT = choose_font()


def apply_theme():
    mpl.rcParams.update({
        "font.family": FONT, "font.size": T.base, "font.weight": "normal",
        "text.color": T.ink, "text.usetex": False,
        "mathtext.fontset": "dejavusans", "mathtext.default": "it",
        "axes.labelsize": T.base, "axes.labelweight": "normal",
        "axes.labelcolor": T.ink, "axes.labelpad": 7,
        "axes.titlesize": T.title, "axes.titleweight": "normal",
        "axes.titlelocation": "left", "axes.titlepad": 10,
        "axes.edgecolor": T.frame_color, "axes.linewidth": T.frame,
        "axes.spines.top": True, "axes.spines.right": True,
        "axes.spines.left": True, "axes.spines.bottom": True,
        "axes.axisbelow": True, "axes.facecolor": T.background,
        "figure.facecolor": "white", "savefig.facecolor": "white",
        "xtick.labelsize": T.small, "ytick.labelsize": T.small,
        "xtick.color": T.ink, "ytick.color": T.ink,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "xtick.minor.visible": False, "ytick.minor.visible": False,
        "xtick.major.pad": 4, "ytick.major.pad": 4,
        "grid.color": T.grid_color, "grid.linewidth": T.grid,
        "grid.linestyle": "-", "lines.linewidth": T.line,
        "lines.markersize": T.marker, "lines.markeredgewidth": T.outline,
        "patch.linewidth": T.outline, "hatch.linewidth": 0.4,
        "legend.frameon": False, "legend.fontsize": T.small,
        "legend.title_fontsize": T.small, "legend.handlelength": 1.8,
        "legend.handletextpad": 0.6, "legend.columnspacing": 1.5,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "svg.hashsalt": "figures4papers-minimal", "savefig.dpi": 300,
    })


def style_axes(ax, grid="y"):
    """Use y grids for bars, xy for relationships, and none for diagrams."""
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(T.frame_color)
        spine.set_linewidth(T.frame)
    ax.set_facecolor(T.background)
    ax.grid(False, which="both")
    ax.set_axisbelow(True)
    for direction in grid:
        if direction in "xy":
            ax.grid(True, axis=direction, which="major", color=T.grid_color,
                    linewidth=T.grid)
    ax.tick_params(axis="both", which="both", length=0, labelsize=T.small)
    for label in (ax.xaxis.label, ax.yaxis.label):
        label.set_fontfamily(FONT)
        label.set_fontweight("normal")
        label.set_fontsize(T.base)


def restyle_diagram(ax):
    """Normalize native upstream artists without changing their coordinates.

    Used for the manifold drawing, which hard-codes sizes and colors.
    Quantitative charts are rendered explicitly with the theme's tokens.
    """
    for artist in ax.findobj():
        if isinstance(artist, Text):
            old = artist.get_fontsize()
            artist.set_fontfamily(FONT)
            artist.set_fontweight("normal")
            artist.set_fontsize(max(7.5, min(T.base, old * 0.37)))
            artist.set_path_effects([])
            if artist.get_bbox_patch() is not None:
                artist.get_bbox_patch().set_facecolor(T.background)
        if isinstance(artist, Line2D):
            artist.set_linewidth(min(T.line, artist.get_linewidth() * 0.4))
            artist.set_markersize(max(2, artist.get_markersize() * 0.4))
            artist.set_markeredgewidth(T.outline)
        if isinstance(artist, FancyArrowPatch):
            artist.set_linewidth(min(T.line, artist.get_linewidth() * 0.4))
            artist.set_mutation_scale(max(5, artist.get_mutation_scale() * 0.45))
        if isinstance(artist, Annotation) and artist.arrow_patch:
            artist.arrow_patch.set_linewidth(T.error)
    for collection in ax.collections:
        widths = collection.get_linewidths()
        collection.set_linewidths([min(T.line, w * 0.4) for w in widths])
        if isinstance(collection, PathCollection):
            collection.set_sizes(collection.get_sizes() * 0.2)
    leg = ax.get_legend()
    if leg:
        leg.set_frame_on(False)
        for label in leg.get_texts():
            label.set_fontsize(T.small)


def recolor_manifold(ax):
    """Map upstream manifold colors to the shared palette, retaining opacity."""
    import numpy as np
    from matplotlib.colors import to_rgba
    mapping = {
        "#2E74B5": T.teal, "#1f77b4": T.scatter,
        "#6F6F6F": T.taupe, "#6b7280": T.taupe, "#D62728": T.rust,
    }
    def recolor(value):
        try:
            rgba = np.asarray(to_rgba(value))
        except (ValueError, TypeError):
            return value
        for old, new in mapping.items():
            if np.allclose(rgba[:3], to_rgba(old)[:3]):
                return (*to_rgba(new)[:3], rgba[3])
        return value
    for line in ax.lines:
        line.set_color(recolor(line.get_color()))
        for getter, setter in ((line.get_markerfacecolor, line.set_markerfacecolor),
                               (line.get_markeredgecolor, line.set_markeredgecolor)):
            setter(recolor(getter()))
    for collection in ax.collections:
        for getter, setter in ((collection.get_facecolors, collection.set_facecolors),
                               (collection.get_edgecolors, collection.set_edgecolors)):
            colors = getter()
            if len(colors):
                setter([recolor(c) for c in colors])
    for text in ax.texts:
        text.set_color(recolor(text.get_color()))
