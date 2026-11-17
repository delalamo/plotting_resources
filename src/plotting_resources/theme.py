"""Approved plotting tokens, font setup and axes styling."""
from pathlib import Path
import json
import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

ROOT=Path(__file__).resolve().parent
SETTINGS=json.loads((ROOT/'selected_style.json').read_text())
STYLE=SETTINGS['style']; TYPE=SETTINGS['typography']; LAYOUT=SETTINGS['layout']
COLORS=STYLE['palette']['colors']+STYLE['palette']['extra']
BLUE,BRICK,GOLD=COLORS[:3]
MARKERS=['o','s','^','D','v','P','X','<','>']


def apply_theme():
    """Use the approved fonts and physical point sizes; never substitute Arial."""
    for weight,style in [('normal','normal'),('bold','normal'),('normal','italic')]:
        try:
            font_manager.findfont(FontProperties(family=TYPE['font'],weight=weight,style=style),fallback_to_default=False)
        except ValueError as error:
            raise RuntimeError('Install Arial Regular, Bold and Italic before rendering these templates.') from error
    mpl.rcParams.update({
        'font.family':TYPE['font'],'font.size':TYPE['base_text_pt'],'font.weight':'normal',
        'text.color':STYLE['ink'],'text.usetex':False,'text.hinting':'none',
        'mathtext.fontset':'custom','mathtext.default':'it','mathtext.rm':'Arial',
        'mathtext.it':'Arial:italic','mathtext.bf':'Arial:bold','mathtext.bfit':'Arial:italic:bold',
        'mathtext.sf':'Arial','mathtext.tt':'Arial','mathtext.cal':'STIXNonUnicode:italic','mathtext.fallback':'stix',
        'axes.labelsize':TYPE['labels_pt'],'axes.labelweight':'bold','axes.labelcolor':STYLE['ink'],
        'axes.titlesize':TYPE['titles_pt'],'axes.titleweight':'bold','axes.titlelocation':'left',
        'axes.titlepad':7.5,'axes.axisbelow':True,'axes.facecolor':STYLE['panel'],
        'axes.prop_cycle':mpl.cycler(color=COLORS),
        'xtick.labelsize':TYPE['ticks_legends_pt'],'ytick.labelsize':TYPE['ticks_legends_pt'],
        'xtick.color':STYLE['ink'],'ytick.color':STYLE['ink'],
        'xtick.major.pad':LAYOUT['x_tick_label_pad_pt'],'ytick.major.pad':LAYOUT['y_tick_label_pad_pt'],
        'legend.frameon':False,'legend.fontsize':TYPE['ticks_legends_pt'],
        'lines.linewidth':STYLE['line'],'lines.markersize':STYLE['marker'],
        'lines.markerfacecolor':STYLE['panel'],'lines.markeredgewidth':.625,
        'figure.facecolor':STYLE['canvas'],'savefig.facecolor':STYLE['canvas'],
        'hatch.color':STYLE['hatch_color'],'hatch.linewidth':STYLE['hatch_width'],
        'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','svg.hashsalt':'paper-style',
        'savefig.dpi':300,
    })


def style_axes(ax,grid='y'):
    ax.set_facecolor(STYLE['panel']);ax.set_axisbelow(True);ax.grid(False,which='both')
    for spine in ax.spines.values():
        spine.set_visible(True);spine.set_color(STYLE['frame_color']);spine.set_linewidth(STYLE['frame_width'])
    for direction in grid:
        if direction not in 'xy':raise ValueError("grid must be '', 'x', 'y' or 'xy'")
        ax.grid(True,axis=direction,color=STYLE['grid_color'],lw=STYLE['grid_width'],ls=STYLE['grid_style'])
    ax.tick_params(length=STYLE['ticks'],width=STYLE['frame_width'])
    ax.xaxis.labelpad=LAYOUT['x_axis_title_pad_pt'];ax.yaxis.labelpad=LAYOUT['y_axis_title_pad_pt']
    return ax
