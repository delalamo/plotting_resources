"""Fit unchanged-size type and marks into a selected article-block height."""
from pathlib import Path
import json
import numpy as np
from matplotlib.text import Text, Annotation
from matplotlib.transforms import Bbox

ROOT=Path(__file__).resolve().parent
BASELINE_DOC=json.loads((ROOT/'figure-height-baseline.json').read_text())
BASELINE=BASELINE_DOC['figures']


def block_dimensions(slug,factor,vertical_scale):
    baseline=BASELINE[slug]
    block_height=baseline['old_block_height_pt']*factor
    external_height=baseline['old_external_text_and_spacing_height_pt']
    saved_spacing=BASELINE_DOC['original_scalable_vertical_spacing_pt']*(1-vertical_scale)
    return block_height,block_height-external_height+saved_spacing


def fit_block(f,slug,compact,factor,vertical_scale):
    baseline=BASELINE[slug]
    target_block,target_chart=block_dimensions(slug,factor,vertical_scale)
    target=target_chart/72
    f.canvas.draw();fw,fh=f.get_size_inches()
    assert abs(fh*72-baseline['old_native_chart_height_pt'])<.1,(slug,fh*72,baseline)
    positions=[ax.get_position(original=True).frozen() for ax in f.axes]
    bands=[]
    for p in sorted(positions,key=lambda p:p.y0):
        lo,hi=p.y0*fh,p.y1*fh
        if bands and lo<bands[-1][1]-.001:bands[-1][1]=max(hi,bands[-1][1])
        else:bands.append([lo,hi])
    figure_text=[(t,*t.get_position()) for t in f.texts]
    artists=[(a,a.get_window_extent(f.canvas.get_renderer()).transformed(f.dpi_scale_trans.inverted())) for a in f.artists]
    for lg in f.legends:lg.labelspacing*=vertical_scale
    for ax in f.axes:
        ax.xaxis.labelpad=8*vertical_scale
        ax.tick_params(axis='x',pad=4*vertical_scale)
        title=ax.get_title(loc='left')
        if title:
            heading=ax.set_title(title,loc='left',pad=10*vertical_scale)
            for text in ax.texts:
                if len(text.get_text())==1 and text.get_text().isupper():text.set_transform(heading.get_transform())
    if slug=='urban-spending-bars':
        ax=f.axes[0]
        labels=[t.get_text().replace('\n',' ') for t in ax.get_yticklabels()]
        ax.set_yticks(ax.get_yticks(),labels)
        p=positions[0]
        positions[0]=Bbox.from_bounds(p.x0+6.5/72/fw,p.y0,p.width,p.height)
    if slug=='urban-home-equity-lines':f.axes[0].set_yticks([0,400,800,1200])
    if slug=='focus-parameter-response':f.axes[0].set_yticks([60,70,80])
    if slug in ['focus-learning-curves','focus-reference-trajectories']:
        ax=f.axes[0];ax.set_ylabel(ax.get_ylabel().replace(' ','\n',1),fontweight='bold',labelpad=4)
    radar_names=[]
    if slug=='repository-radar':
        radar_names=[(t,*t.get_position()) for t in f.axes[0].texts if '\n' in t.get_text()]
        # Four spokes share each benchmark's scale. Label one spoke per group
        # instead of repeating the same three ticks on all twelve spokes.
        tick_angles=[2*np.pi-j*np.pi/6 for j in (1,5,9)]
        for t in list(f.axes[0].texts):
            if t.get_text().isdigit() and not any(abs(t.get_position()[0]-a)<1e-6 for a in tick_angles):
                t.remove()
    end_labels={}
    if slug=='publication-trends-two-panels':
        for ax in f.axes:
            labels=[]
            for t in list(ax.texts):
                if t.get_text().isdigit():
                    x,y=t.get_position()
                    a=ax.annotate(t.get_text(),xy=(x-.38,y),xytext=(x,y),ha='left',va='center',
                                  fontsize=10,color=t.get_color(),
                                  arrowprops=dict(arrowstyle='-',color=t.get_color(),lw=.45,shrinkA=1,shrinkB=1))
                    labels.append(a);t.remove()
            end_labels[ax]=sorted(labels,key=lambda t:t.xy[1])

    def place(k):
        def ymap(y):
            low=bands[0][0]
            if y<=low:return low+(y-low)*vertical_scale
            value=low
            for i,(a,b) in enumerate(bands):
                if y<=b:return value+(y-a)*k
                value+=(b-a)*k
                end=bands[i+1][0] if i+1<len(bands) else y
                if y<=end:return value+(y-b)*vertical_scale
                value+=(end-b)*vertical_scale
            return value
        f.set_size_inches(fw,fh)
        for ax,p in zip(f.axes,positions):
            lo=ymap(p.y0*fh);hi=ymap(p.y1*fh)
            ax.set_position([p.x0,lo/fh,p.width,(hi-lo)/fh])
        for text,x,y in figure_text:text.set_position((x,ymap(y*fh)/fh))
        for a,box in artists:
            a.set_transform(f.transFigure)
            a.set_bounds(box.x0/fw,ymap(box.y0)/fh,box.width/fw,(ymap(box.y1)-ymap(box.y0))/fh)
        f.canvas.draw()
        renderer=f.canvas.get_renderer()
        if slug=='brute-force-eight-panels':
            ticks=[t.get_window_extent(renderer).y0 for ax in f.axes for t in ax.get_xticklabels() if t.get_visible()]
            label=next(t for t in f.texts if t.get_text()=='Model (see numbered color key)')
            label.set_va('top');label.set_y((min(ticks)-8*vertical_scale*f.dpi/72)/f.bbox.height)
        if slug=='concept-two-panels':
            ax=f.axes[1];height=ax.bbox.height*72/f.dpi
            for t in ax.texts:
                if t.get_text().startswith('$z_\\text{mm}'):
                    t.set_transform(ax.transAxes);t.set_position((.035,.965-13/height));t.set_va('top')
                elif t.get_text().startswith('$z_\\text{t}'):
                    t.set_transform(ax.transAxes);t.set_position((.035,.035+13/height));t.set_va('bottom')
        if slug=='publication-trends-two-panels':
            for ax in f.axes:
                height=ax.bbox.height*72/f.dpi;ymin,ymax=ax.get_ylim();span=ymax-ymin
                events=[t for t in ax.texts if isinstance(t,Annotation) and t not in end_labels[ax]]
                for i,t in enumerate(events):
                    th=Text.get_window_extent(t,renderer).height*72/f.dpi
                    y=min(t.xy[1]+(9 if i%2==0 else 23)/height*span,ymax-(th+3)/height*span)
                    t.set_position((t.xy[0],y))
                previous=None
                for t in end_labels[ax]:
                    y=max(t.xy[1],ymin+6/height*span)
                    if previous is not None:y=max(y,previous+11.5/height*span)
                    t.set_position((t.xy[0]+.38,y));previous=y
        if slug=='template-emphasis-lines':
            ax=f.axes[0];labels=sorted([t for t in ax.texts if isinstance(t,Annotation)],key=lambda t:t.xy[1])
            height=ax.bbox.height*72/f.dpi;ymin,ymax=ax.get_ylim();gap=11.5/height*(ymax-ymin)
            top=ymax-6/height*(ymax-ymin)
            for i,t in enumerate(labels):t.set_position((t.get_position()[0],top-(len(labels)-1-i)*gap))
        if radar_names:
            ax=f.axes[0]
            for t,angle,radius in radar_names:
                x,y=ax.transData.transform((angle,radius))
                x,y=ax.transAxes.inverted().transform((x,y))
                spread=1+3*(1-vertical_scale)
                t.set_transform(ax.transAxes);t.set_position((.5+(x-.5)*spread,y))
        compact(f,vertical_scale=vertical_scale)
        return f.get_figheight()

    lo,hi=.005,1.0
    small=place(lo);large=place(hi)
    if small>target+.002:raise ValueError((slug,'fixed-size content is too tall',small*72,target*72))
    for _ in range(16):
        mid=(lo+hi)/2;got=place(mid)
        if got<target:lo=mid
        else:hi=mid
    got=place((lo+hi)/2)
    assert abs(got-target)*72<.02,(slug,got*72,target*72)
    f._layout_audit.update(full_block_height_factor=factor,vertical_spacing_factor=vertical_scale,
        chart_width_preserved=True,font_sizes_preserved=True,
        stroke_widths_preserved=True,old_chart_height_pt=baseline['old_native_chart_height_pt'],
        new_chart_height_pt=got*72,target_block_height_pt=target_block,
        plot_geometry_preserved=False,vertical_axis_scale=(lo+hi)/2,
        x_axis_title_pad_pt=8*vertical_scale,y_axis_title_pad_pt=4,
        x_tick_label_pad_pt=4*vertical_scale,y_tick_label_pad_pt=4)
