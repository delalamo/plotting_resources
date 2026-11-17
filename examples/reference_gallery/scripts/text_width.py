"""Reflow selected source figures at text width without scaling type or marks."""
import numpy as np
from matplotlib.text import Annotation,Text
from matplotlib.transforms import Bbox


def reflow(f,slug,compact):
    old_width,height=f.get_size_inches();width=6.25
    audit=dict(f._layout_audit)
    positions=[a.get_position().frozen() for a in f.axes]
    legends=[dict(handles=lg.legend_handles,labels=[t.get_text() for t in lg.get_texts()]) for lg in f.legends]
    for lg in list(f.legends):lg.remove()
    f.set_size_inches(width,height)
    if slug=='repository-radar':
        ax=f.axes[0];p=positions[0]
        ax.set_position([.26,p.y0,.48,p.height])
        for t in ax.texts:
            if '\n' in t.get_text():
                x,y=t.get_position();t.set_position((.5+(x-.5)/1.75,y))
                t.set_text(t.get_text().replace('Qwen2.5-VL-','Qwen2.5-\nVL-').replace('LLaVA-OneVision-','LLaVA-\nOneVision-').replace('InternVL2.5-','InternVL2.5-\n'))
        f.canvas.draw();r=f.canvas.get_renderer()
        boxes=[t.get_window_extent(r) for t in ax.texts]
        bottom=min(b.y0 for b in boxes)/f.bbox.height-3/72/height
        top=max(b.y1 for b in boxes)/f.bbox.height+3/72/height
        for artist in f.artists:
            artist.set_transform(f.transFigure)
            artist.set_bounds(.015,bottom,.97,top-bottom)
    else:
        for ax,p in zip(f.axes,positions):
            left=p.x0*old_width;right=old_width-p.x1*old_width
            ax.set_position([left/width,p.y0,(width-left-right)/width,p.height])
        if slug=='publication-trends-two-panels':
            for ax in f.axes:
                ax.set_title(ax.get_title(loc='left'),loc='left',x=.22/(ax.get_position().width*width),pad=7.5)
                for t in ax.texts:
                    if isinstance(t,Annotation) and t.get_text().isdigit():
                        t.anncoords=ax.get_yaxis_transform()
                        t.set_position((1.012,t.get_position()[1]))
            for t in f.texts:
                if t.get_text()=='Cumulative publication count':t.set_x(.26/width)
            for ax in f.axes:
                events=[t for t in ax.texts if isinstance(t,Annotation) and not t.get_text().isdigit()]
                # Reserve a distinct lane for each release; arrows keep its true date.
                for t in events:
                    t.set_text(t.get_text().replace('Gemini ','Gemini\n').replace('LlaMA ','LlaMA\n').replace('LlaVA ','LlaVA\n'))
                f.canvas.draw();renderer=f.canvas.get_renderer();placed=[]
                for t in sorted(events,key=lambda t:t.xy[0]):
                    original=t.xy
                    candidates=[]
                    for dy in [12,35,60,85,-20,-45,-70]:
                        for dx in [0,-2,2,-4,4]:
                            x=np.clip(original[0]+dx,1,29);y=np.clip(original[1]+dy,8,99)
                            t.set_position((x,y));box=Text.get_window_extent(t,renderer).expanded(1.10,1.15)
                            if ax.bbox.contains(box.x0,box.y0) and ax.bbox.contains(box.x1,box.y1) and not any(box.overlaps(b) for b in placed):
                                candidates.append((abs(dx)*5+abs(dy)+(20 if dy<0 else 0),x,y,box))
                    if not candidates:raise ValueError(('No annotation space',t.get_text()))
                    _,x,y,box=min(candidates,key=lambda c:c[0]);t.set_position((x,y));placed.append(box)
    for spec in legends:
        cols=2 if slug=='repository-posttraining' else (3 if slug=='repository-radar' else 2)
        f.legend(**spec,loc='upper left',bbox_to_anchor=(.10,.99,.85,0),mode='expand',
                 borderaxespad=0,borderpad=0,ncols=cols,handlelength=1.8,labelspacing=.45,columnspacing=1)
    compact(f,vertical_scale=.75)
    f._layout_audit.update(audit)
    f._layout_audit.update(chart_width_preserved=False,native_width_in=width,text_width_default=True,
        old_chart_width_in=old_width,new_chart_height_pt=f.get_figheight()*72,
        width_reflow_preserves_font_and_marks=True)
