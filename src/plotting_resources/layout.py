"""Measured headings, legends and footers; PDF/PNG/SVG exports."""
from pathlib import Path
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text
from .theme import STYLE,TYPE,LAYOUT

def _white_backgrounds(f):
    """Replace only background-colored fills; retain data colors and opacity."""
    import numpy as np
    backgrounds=[mpl.colors.to_rgba(STYLE[k]) for k in ('canvas','panel')]
    def is_background(color):
        try: return any(np.allclose(mpl.colors.to_rgba(color),bg) for bg in backgrounds)
        except (ValueError,TypeError): return False
    f.set_facecolor('white')
    for ax in f.axes:
        ax.set_facecolor('white')
        for line in ax.lines:
            if is_background(line.get_markerfacecolor()):line.set_markerfacecolor('white')
        for collection in ax.collections:
            colors=collection.get_facecolors().copy()
            for i,color in enumerate(colors):
                if is_background(color):colors[i]=mpl.colors.to_rgba('white')
            if len(colors):collection.set_facecolors(colors)
    for text in f.findobj(Text):
        box=text.get_bbox_patch()
        if box is not None and is_background(box.get_facecolor()):box.set_facecolor('white')
    for artist in f.findobj():
        if isinstance(artist,mpl.patches.Patch) and is_background(artist.get_facecolor()):artist.set_facecolor('white')


def _wrap(body,width,size,weight='normal'):
    renderer=RendererAgg(10,10,72);font=FontProperties(family=TYPE['font'],size=size,weight=weight)
    lines=[]
    for paragraph in str(body).split('\n'):
        current=''
        for word in paragraph.split():
            candidate=(current+' '+word).strip()
            if current and renderer.get_text_width_height_descent(candidate,font,ismath=False)[0]>width:
                lines.append(current);current=word
            else:current=candidate
        lines.append(current)
    return '\n'.join(lines)


def _bounds(f):
    f.canvas.draw();renderer=f.canvas.get_renderer()
    boxes=[ax.get_tightbbox(renderer) for ax in f.axes]
    boxes.extend(t.get_window_extent(renderer) for t in f.texts if t.get_visible() and t.get_text())
    return mpl.transforms.Bbox.union([b for b in boxes if b is not None])


def _legend(f,cols):
    handles={}
    for ax in f.axes:
        hs,labels=ax.get_legend_handles_labels()
        for h,label in zip(hs,labels):handles.setdefault(label,h)
        if ax.get_legend() is not None:ax.get_legend().remove()
    ordered=sorted(handles.items(),key=lambda pair:getattr(pair[1],'_paper_legend_priority',2))
    if not ordered:return None
    available=f.get_figwidth()*72
    cols=min(cols,len(ordered));legend=None
    while cols:
        if legend is not None:legend.remove()
        rows=(len(ordered)+cols-1)//cols
        order=[i for col in range(cols) for row in range(rows) if (i:=row*cols+col)<len(ordered)]
        legend=f.legend([ordered[i][1] for i in order],[ordered[i][0] for i in order],
            loc='upper left',bbox_to_anchor=(0,0),ncols=cols,borderpad=0,borderaxespad=0,
            handlelength=1.8,labelspacing=.45,columnspacing=1.4)
        f.canvas.draw();box=legend.get_window_extent(f.canvas.get_renderer())
        if box.width*72/f.dpi<=available:return legend
        cols-=1
    raise ValueError('A legend label is wider than the figure; shorten or wrap it, or increase width.')


def finish(f,*,title='',subtitle='',source='',notes='',legend=True,legend_cols=None,minimal=False):
    """Add headings/footer and place a shared legend below the actual axis labels.

    Trim the outer canvas to equal top/bottom padding, preserving axes height.
    Call once, after adding all data, labels, annotations and panel titles.
    """
    if getattr(f,'_paper_finished',False):raise ValueError('Figure is already finished; export it without finishing twice.')
    if minimal:
        title=subtitle=source=notes=''
        _white_backgrounds(f)
    width,old_height=f.get_size_inches();pad_x=LAYOUT['article_figure_block_horizontal_padding_pt']
    pad_y=LAYOUT['article_figure_block_vertical_padding_pt'];text_width=width*72
    chart_pad=LAYOUT['chart_export_padding_pt']
    # Expand label margins without changing physical type or axes heights.
    for _ in range(5):
        b=_bounds(f);left=max(0,chart_pad-b.x0*72/f.dpi);right=max(0,b.x1*72/f.dpi-(width*72-chart_pad))
        if max(left,right)<.1:break
        positions=[ax.get_position(original=True).frozen() for ax in f.axes]
        lo=min(p.x0 for p in positions);hi=max(p.x1 for p in positions)
        scale=1-(left+right)/(width*72*(hi-lo))
        if scale<.3:raise ValueError('Labels leave too little plot width; wrap them or increase figure width.')
        for ax,p in zip(f.axes,positions):
            ax.set_position([lo+left/(width*72)+(p.x0-lo)*scale,p.y0,p.width*scale,p.height])
    b=_bounds(f);low,high=b.y0/f.dpi,b.y1/f.dpi
    positions=[ax.get_position().frozen() for ax in f.axes]
    figure_text=[(t,*t.get_position()) for t in f.texts]
    lg=_legend(f,legend_cols or (3 if width<10 else 4)) if legend else None
    legend_height=lg.get_window_extent(f.canvas.get_renderer()).height*72/f.dpi if lg else 0
    descriptors=[]
    def measure(body,size,bold=False):
        wrapped=_wrap(body,text_width,size,'bold' if bold else 'normal')
        t=f.text(0,1,wrapped,ha='left',va='top',fontsize=size,fontweight='bold' if bold else 'normal',linespacing=1.3)
        f.canvas.draw();height=t.get_window_extent(f.canvas.get_renderer()).height*72/f.dpi;t.remove()
        return wrapped,height
    y=pad_y
    for role,body,size,bold,gap in [
        ('title',title,TYPE['titles_pt'],True,0),
        ('subtitle',subtitle,TYPE['base_text_pt'],False,LAYOUT['title_to_subtitle_pt'])]:
        if body:
            if descriptors:y+=gap
            wrapped,height=measure(body,size,bold);descriptors.append((role,wrapped,size,bold,y));y+=height
    if descriptors:y+=LAYOUT['subtitle_to_chart_content_pt']
    chart_top=y;y+=(high-low)*72
    legend_top=None
    if lg:y+=LAYOUT['plot_labels_to_legend_pt'];legend_top=y;y+=legend_height
    footer_top=None
    for role,body,size,gap in [('source',source,TYPE['sources_pt'],LAYOUT['source_gap_after_chart_pt']),
        ('notes',notes,TYPE['notes_pt'],LAYOUT['source_to_notes_gap_pt'] if source else LAYOUT['source_gap_after_chart_pt'])]:
        if body:
            y+=gap
            if footer_top is None:footer_top=y
            wrapped,height=measure(body,size);descriptors.append((role,wrapped,size,False,y));y+=height
    content_bottom=y;new_height=(y+pad_y)/72
    shift=new_height-chart_top/72-high
    full_width=width+2*pad_x/72
    f.set_size_inches(full_width,new_height)
    for ax,p in zip(f.axes,positions):ax.set_position([(p.x0*width+pad_x/72)/full_width,
        (p.y0*old_height+shift)/new_height,p.width*width/full_width,p.height*old_height/new_height])
    for t,x,old_y in figure_text:t.set_position(((x*width+pad_x/72)/full_width,(old_y*old_height+shift)/new_height))
    if lg:lg.set_bbox_to_anchor((pad_x/(full_width*72),1-legend_top/(new_height*72)),transform=f.transFigure)
    for role,body,size,bold,top in descriptors:
        f.text(pad_x/(full_width*72),1-top/(new_height*72),body,ha='left',va='top',fontsize=size,
            fontweight='bold' if bold else 'normal',color=STYLE['muted'] if role=='notes' else STYLE['ink'],linespacing=1.3)
    f._paper_finished=True
    f._paper_layout=dict(width_in=full_width,native_chart_width_in=width,height_in=new_height,top_padding_pt=pad_y,bottom_padding_pt=pad_y,
        content_bottom_pt=content_bottom,footer_top_pt=footer_top,legend_top_pt=legend_top,
        source_notes_font_pt=TYPE['notes_pt'],base_font_pt=TYPE['base_text_pt'],font=TYPE['font'],minimal=minimal)
    f.canvas.draw()
    return f


def export(f,path,*,formats=('pdf','png','svg'),close=True,**captions):
    """Write a complete, native-size figure with embedded PDF fonts and 300 dpi PNG."""
    if not getattr(f,'_paper_finished',False):finish(f,**captions)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    renderer=f.canvas.get_renderer();outside=[];undrawn_ticks=set()
    # Locators retain ticks outside the view interval; Matplotlib does not draw
    # those labels, even though the Text object's visible property is true.
    for ax in f.axes:
        for axis in (ax.xaxis,ax.yaxis):
            lo,hi=sorted(axis.get_view_interval());tolerance=max(1,hi-lo)*1e-9
            for tick in [*axis.get_major_ticks(),*axis.get_minor_ticks()]:
                if not lo-tolerance<=tick.get_loc()<=hi+tolerance:
                    undrawn_ticks.update([tick.label1,tick.label2])
    for t in f.findobj(Text):
        if not t.get_visible() or not t.get_text():continue
        if t in undrawn_ticks:continue
        # Matplotlib keeps invisible tick-label children on shared axes.
        if t.axes is not None and not t.axes.get_visible():continue
        b=t.get_window_extent(renderer)
        if b.x0<-.5 or b.y0<-.5 or b.x1>f.bbox.width+.5 or b.y1>f.bbox.height+.5:outside.append(t.get_text())
    if outside:raise ValueError('Text outside the figure: '+repr(outside))
    math=any('$' in t.get_text() for t in f.findobj(Text))
    result={}
    for extension in formats:
        if extension not in ('pdf','png','svg'):raise ValueError('Supported formats: pdf, png, svg')
        target=path.with_suffix('.'+extension)
        with mpl.rc_context({'svg.fonttype':'path' if math else 'none'}):f.savefig(target,dpi=300,facecolor=f.get_facecolor())
        result[extension]=target
    path.with_suffix('.layout.json').write_text(json.dumps(f._paper_layout,indent=2)+'\n')
    if close:plt.close(f)
    return result
