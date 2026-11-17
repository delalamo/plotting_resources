"""Data-preserving plotting helpers and native-size panel creation."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from .theme import SETTINGS,STYLE,TYPE,LAYOUT,COLORS,BLUE,BRICK,GOLD,MARKERS,apply_theme,style_axes

def figure(rows=1,cols=1,*,width=None,panel_height=None,sharex=False,sharey=False,grid='y',projection=None):
    """Return (figure, 2-D axes array). Sizes are inches; text is never scaled.

    Defaults use a 6.25-inch chart (6.75-inch complete figure) for every layout.
    export() adds the 18-point left/right outer figure padding to this width.
    panel_height controls only the axes, not titles, legends or the footer.
    """
    if rows<1 or cols<1:raise ValueError('rows and cols must be positive')
    apply_theme();single=rows*cols==1
    width=LAYOUT["default_native_chart_width_in"] if width is None else width
    panel_height=panel_height or (2.2 if single else 1.65)
    left,right,bottom,top=.65,.18,.55,.30
    xgap=LAYOUT['panel_horizontal_gap_pt']/72 if sharey else .65
    ygap=SETTINGS['multi_panel']['layouts']['publication_trends']['vertical_gap_in']
    height=rows*panel_height+(rows-1)*ygap+bottom+top
    panel_width=(width-left-right-(cols-1)*xgap)/cols
    if panel_width<=.5:raise ValueError('Increase width or reduce the column count.')
    f,axes=plt.subplots(rows,cols,figsize=(width,height),squeeze=False,
        sharex=sharex,sharey=sharey,subplot_kw={'projection':projection} if projection else None)
    f.subplots_adjust(left=left/width,right=1-right/width,bottom=bottom/height,top=1-top/height,
        wspace=xgap/panel_width,hspace=ygap/panel_height)
    for ax in axes.flat:style_axes(ax,grid)
    return f,axes


def panel_title(ax,title,letter=None):
    if letter is None:return ax.set_title(title,loc='left',fontweight='bold')
    width=ax.get_position().width*ax.figure.get_figwidth()
    t=ax.set_title(title,loc='left',x=.22/width,fontweight='bold')
    ax.text(0,1,str(letter),transform=t.get_transform(),ha='left',va=t.get_verticalalignment(),fontweight='normal')
    return t


def line(ax,x,y,label,*,index=0,color=None,marker=True,**kwargs):
    if color is None and index>=len(COLORS):raise ValueError('Only nine categorical colors are selected; supply a deliberate color mapping.')
    defaults=dict(color=color or COLORS[index],lw=STYLE['line'],
        marker=MARKERS[index%len(MARKERS)] if marker else None,
        ms=STYLE['marker'],mfc=STYLE['panel'],mew=.625,label=label)
    return ax.plot(x,y,**(defaults|kwargs))[0]


def emphasis_lines(ax,x,focus,references,*,focus_label='Selected method',markers=False):
    """references is an ordered mapping {name: y_values}; focus is drawn last."""
    gray=np.rint(np.linspace(119,183,len(references))).astype(int)
    patterns=SETTINGS['emphasis_treatment']['comparison_dash_patterns']
    for i,((label,y),value) in enumerate(zip(references.items(),gray)):
        handle=line(ax,x,y,label,index=i,color='#'+f'{value:02x}'*3,marker=markers,
                    linestyle=(0,tuple(patterns[i%len(patterns)])),alpha=1,zorder=2)
        handle._paper_legend_priority=1
    handle=line(ax,x,focus,focus_label,color=BLUE,marker=markers,linestyle='-',zorder=4)
    handle._paper_legend_priority=0
    return handle


def bars(ax,labels,values,*,errors=None,horizontal=False,highlight=None,color=None,value_format=None):
    """Single-series bars; highlight is a zero-based category index."""
    values=np.asarray(values,dtype=float);x=np.arange(len(labels))
    if values.shape!=(len(labels),):raise ValueError('One value is required for each label.')
    colors=color or ([BLUE if i==highlight else '#979797' for i in range(len(labels))] if highlight is not None else BLUE)
    error_kw=dict(ecolor=STYLE['ink'],elinewidth=STYLE['error'],capthick=STYLE['error'],capsize=STYLE['cap'])
    common=dict(color=colors,edgecolor=STYLE['ink'],lw=STYLE['bar_edge'],error_kw=error_kw)
    if horizontal:
        result=ax.barh(x,values,height=STYLE['bar_width'],xerr=errors,**common)
        ax.set_yticks(x,labels);ax.invert_yaxis();ax.margins(x=.15)
        if np.all(values>=0):ax.set_xlim(left=0)
    else:
        result=ax.bar(x,values,width=STYLE['bar_width'],yerr=errors,**common)
        ax.set_xticks(x,labels);ax.margins(y=.15)
        if np.all(values>=0):ax.set_ylim(bottom=0)
    if value_format is not None:
        ax.bar_label(result,labels=[format(v,value_format) for v in values],padding=3,fontsize=TYPE['labels_pt'])
    return result


def grouped_bars(ax,categories,series,*,errors=None):
    """series and optional errors map series names to one value per category."""
    x=np.arange(len(categories));width=STYLE['bar_width']/len(series)
    for i,(label,values) in enumerate(series.items()):
        if len(values)!=len(categories):raise ValueError('Each series needs one value per category.')
        ax.bar(x+(i-(len(series)-1)/2)*width,values,width,color=COLORS[i],label=label,
            edgecolor=STYLE['ink'],lw=STYLE['bar_edge'],yerr=None if errors is None else errors[label],
            error_kw=dict(ecolor=STYLE['ink'],elinewidth=STYLE['error'],capthick=STYLE['error'],capsize=STYLE['cap']))
    ax.set_xticks(x,categories)
    if all(np.all(np.asarray(v)>=0) for v in series.values()):ax.set_ylim(bottom=0)
    ax.margins(y=.12)


def stacked_bars(ax,categories,series):
    """Preserve the supplied values; never silently normalize percentages."""
    x=np.arange(len(categories));bottom=np.zeros(len(categories))
    for i,(label,values) in enumerate(series.items()):
        values=np.asarray(values,dtype=float)
        if values.shape!=bottom.shape or np.any(values<0):raise ValueError('Stack values must be nonnegative, with one per category.')
        ax.bar(x,values,STYLE['bar_width'],bottom=bottom,color=COLORS[i],label=label,
            edgecolor=STYLE['ink'],lw=STYLE['bar_edge'],alpha=1 if i==0 else STYLE['composition_alpha'])
        bottom+=values
    ax.set_xticks(x,categories);ax.set_ylim(bottom=0)
    return bottom


def area(ax,x,y,label,*,index=0,color=None,alpha=None):
    color=color or COLORS[index]
    handle=line(ax,x,y,label,index=index,color=color,marker=False)
    ax.fill_between(x,0,y,color=color,alpha=STYLE['area_alpha'][index%2] if alpha is None else alpha)
    return handle


def radar(ax,categories,series,*,limits=(0,100),ticks=(25,50,75,100)):
    """Use a common numeric scale. No per-category normalization is performed."""
    if ax.name!='polar':raise ValueError("Create this figure with projection='polar'.")
    theta=np.linspace(0,2*np.pi,len(categories),endpoint=False);closed=np.r_[theta,theta[0]]
    ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1)
    ax.set_xticks(theta,categories);ax.set_ylim(*limits);ax.set_yticks(ticks)
    ax.tick_params(axis='x',pad=8);ax.spines['polar'].set_visible(False)
    for i,(label,values) in enumerate(series.items()):
        values=np.asarray(values,dtype=float)
        if values.shape!=theta.shape:raise ValueError('Each radar series needs one value per category.')
        line(ax,closed,np.r_[values,values[0]],label,index=i)
        ax.fill(closed,np.r_[values,values[0]],color=COLORS[i],alpha=STYLE['radar_alpha'])
    ax.figure.canvas.draw()
    bounds=ax.get_tightbbox(ax.figure.canvas.get_renderer())
    pad=3*ax.figure.dpi/72
    bounds=mpl.transforms.Bbox.from_extents(bounds.x0-pad,bounds.y0-pad,bounds.x1+pad,bounds.y1+pad)
    bounds=bounds.transformed(ax.transAxes.inverted())
    ax.add_patch(Rectangle((bounds.x0,bounds.y0),bounds.width,bounds.height,
        transform=ax.transAxes,facecolor=STYLE['panel'],edgecolor=STYLE['frame_color'],
        lw=STYLE['frame_width'],clip_on=False,zorder=-5))
