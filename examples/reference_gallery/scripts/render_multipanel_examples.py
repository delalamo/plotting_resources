"""Rebuild the four native multi-panel README figures in selected R1/S3 style.

All quantitative values come from data.json. The concept illustration uses the
upstream Gaussian curves and seed-42 manifold generator without changing geometry.
Run from any directory; no network access or TeX installation is needed.
"""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/figures4papers-mpl')
import hashlib
import html
import importlib.util
import json
import shutil
import string
import zipfile
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.font_manager import FontProperties, findfont, get_font
from matplotlib.patches import Patch, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection
from matplotlib.text import Text, Annotation
from matplotlib.colors import to_rgba, to_rgb
from matplotlib.transforms import Affine2D
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'multi-panel-arial-10pt'
CHARTS = OUT / 'figures'
PREVIEWS = OUT / 'previews'
TEMP = OUT / 'tmp'
BOOK_NAME = 'multipanel-r1-arial-10pt-math-fixed.pdf'
SELECTED = json.loads((ROOT/'selected-style.json').read_text())
S = SELECTED['style']; T = SELECTED['typography']
MINIMAL=SELECTED.get('rendering',{}).get('minimal',False)
DATA = json.loads((ROOT/'data.json').read_text())
FONT = T['font']; SMALL = T['ticks_legends_pt']; TITLE = T['titles_pt']
INK, MUTED, BG = S['ink'], S['muted'], S['panel']
BLUE, BRICK, GOLD = S['palette']['colors'][:3]
NEUTRAL = S['palette']['neutral']
UPSTREAM = 'https://github.com/ChenLiu-1996/figures4papers'
AUDIT = []
FONT_PT = T['base_text_pt']
PAGE_W, PAGE_H = 14*72, 10*72


def setup():
    for p in (OUT, CHARTS, PREVIEWS, TEMP): p.mkdir(parents=True, exist_ok=True)
    for weight in ('normal','bold'):
        assert get_font(findfont(FontProperties(family=FONT, weight=weight), fallback_to_default=False)).family_name == FONT
    mpl.rcParams.update({
        'font.family': FONT, 'font.size': 10, 'font.weight': 'normal',
        'text.usetex': False, 'text.parse_math': True, 'text.hinting': 'none', 'text.color': INK,
        'mathtext.fontset': 'custom', 'mathtext.default': 'it',
        'mathtext.rm': 'Arial', 'mathtext.it': 'Arial:italic',
        'mathtext.bf': 'Arial:bold', 'mathtext.bfit': 'Arial:italic:bold',
        'mathtext.sf': 'Arial', 'mathtext.tt': 'Arial',
        'mathtext.cal': 'STIXNonUnicode:italic', 'mathtext.fallback': 'stix',
        'axes.labelsize': T['labels_pt'], 'axes.labelweight': T['axis_title_weight'],
        'axes.labelcolor': INK, 'axes.labelpad': 7,
        'axes.titlesize': TITLE, 'axes.titleweight': 'bold', 'axes.titlepad': 10,
        'axes.titlelocation': 'left', 'axes.axisbelow': True,
        'xtick.labelsize': SMALL, 'ytick.labelsize': SMALL,
        'xtick.color': INK, 'ytick.color': INK, 'xtick.major.pad': 4, 'ytick.major.pad': 4,
        'legend.frameon': False, 'legend.fontsize': SMALL,
        'figure.facecolor': S['canvas'], 'savefig.facecolor': S['canvas'],
        'hatch.color': S['hatch_color'], 'hatch.linewidth': S['hatch_width'],
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'svg.hashsalt': 'multipanel-r1-arial', 'savefig.dpi': 300,
    })


def style_axes(ax, grid='xy'):
    ax.set_axis_on(); ax.set_facecolor(BG); ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color(S['frame_color']); sp.set_linewidth(S['frame_width'])
    ax.grid(False, which='both')
    for direction in grid:
        ax.grid(True, axis=direction, color=S['grid_color'], lw=S['grid_width'], ls=S['grid_style'])
    ax.tick_params(length=S['ticks'], width=S['frame_width'])
    for label in (ax.xaxis.label, ax.yaxis.label):
        label.set_fontfamily(FONT); label.set_fontsize(T['labels_pt']); label.set_fontweight('bold')
    ax.xaxis.labelpad=8
    ax.yaxis.labelpad=4


def add_axes(f, x, y, w, h, grid='xy'):
    fw, fh = f.get_size_inches()
    ax = f.add_axes([x/fw,y/fh,w/fw,h/fh]); style_axes(ax,grid)
    return ax


def panel(ax, letter, title):
    width=ax.get_position().width*ax.figure.get_figwidth()
    heading=ax.set_title(title, loc='left', x=.22/width, fontsize=FONT_PT, fontweight='bold')
    ax.text(0,1,letter,transform=heading.get_transform(),ha='left',va=heading.get_verticalalignment(),
            fontsize=FONT_PT,fontweight='normal',clip_on=False)


def row_major_handles(handles, cols):
    rows=(len(handles)+cols-1)//cols
    return [handles[i] for col in range(cols) for row in range(rows)
            if (i:=row*cols+col)<len(handles)]


def content_bounds(f):
    """Visible plotting content, excluding legends, measured in display pixels."""
    f.canvas.draw(); r=f.canvas.get_renderer()
    boxes=[a.get_tightbbox(r) for a in f.axes]
    boxes += [t.get_window_extent(r) for t in f.texts if t.get_visible() and t.get_text()]
    boxes += [a.get_window_extent(r) for a in f.artists if a.get_visible()]
    return min(b.y0 for b in boxes),max(b.y1 for b in boxes)


def _compact_layout(f, vertical_scale=1):
    """Keep plot geometry and type size; put legends below measured axis labels.

    Resize only the surrounding canvas. Three-point export padding gives the
    booklet an actual 11-point subtitle-to-artwork gap, without hidden margins.
    """
    f.canvas.draw();r=f.canvas.get_renderer();fw,fh=f.get_size_inches()
    legends=list(f.legends)+[a.get_legend() for a in f.axes if a.get_legend() is not None]
    specifications=[]
    for lg in legends:
        box=lg.get_window_extent(r)
        specifications.append(dict(handles=lg.legend_handles,labels=[t.get_text() for t in lg.get_texts()],
            ncols=lg._ncols,x=box.x0/f.dpi,width=box.width/f.dpi-2*lg.borderpad*FONT_PT/72,
            height=box.height/f.dpi-2*lg.borderpad*FONT_PT/72,
            handlelength=lg.handlelength,handletextpad=lg.handletextpad,
            labelspacing=lg.labelspacing,columnspacing=lg.columnspacing))
        lg.remove()
    low,high=content_bounds(f);low/=f.dpi;high/=f.dpi
    pad=3/72*vertical_scale;gap=10/72*vertical_scale;between=6/72*vertical_scale
    legend_height=sum(s['height'] for s in specifications)+between*max(0,len(specifications)-1)
    shift=pad+(legend_height+gap if legends else 0)-low
    height=high-low+2*pad+(legend_height+gap if legends else 0)
    positions=[a.get_position().frozen() for a in f.axes]
    plot_sizes=[(a.bbox.width/f.dpi,a.bbox.height/f.dpi) for a in f.axes]
    f.set_size_inches(fw,height)
    for ax,p in zip(f.axes,positions):
        ax.set_position([p.x0,(p.y0*fh+shift)/height,p.width,p.height*fh/height])
    for t in f.texts:
        x,y=t.get_position();t.set_position((x,(y*fh+shift)/height))
    for artist in f.artists:
        artist.set_transform(Affine2D().scale(1,fh/height).translate(0,shift/height)+f.transFigure)
    legend_top=pad+legend_height
    for s in specifications:
        opts={k:s[k] for k in ('handles','labels','ncols','handlelength','handletextpad','labelspacing','columnspacing')}
        f.legend(**opts,loc='upper left',bbox_to_anchor=(s['x']/fw,legend_top/height,s['width']/fw,0),
                 mode='expand',borderaxespad=0,borderpad=0)
        legend_top-=s['height']+between
    f.canvas.draw();r=f.canvas.get_renderer();low,high=content_bounds(f)
    assert np.allclose(plot_sizes,[(a.bbox.width/f.dpi,a.bbox.height/f.dpi) for a in f.axes])
    boxes=[lg.get_window_extent(r) for lg in f.legends]
    clearance=(low-max(b.y1 for b in boxes))*72/f.dpi if boxes else None
    if boxes:assert clearance>=10*vertical_scale-.1,('legend clearance',clearance)
    f._layout_audit=dict(legend_position='below',legend_count=len(boxes),
        plot_labels_to_legend_pt=round(clearance,2) if boxes else None,
        top_export_padding_pt=round((f.bbox.height-high)*72/f.dpi,2),
        legend_group_gap_pt=6*vertical_scale if len(boxes)>1 else None,plot_geometry_preserved=True)


def compact_layout(f, slug=None):
    _compact_layout(f)
    revision=SELECTED.get('height_revision',{})
    if slug and revision.get('block_height_factor',1)!=1:
        from figure_height import fit_block
        fit_block(f,slug,_compact_layout,revision['block_height_factor'],revision['vertical_spacing_factor'])
    if slug in SELECTED.get('width_revision',{}).get('narrowed_figures',[]):
        from text_width import reflow
        reflow(f,slug,_compact_layout)


def benchmark():
    d=DATA['comparison_IEDB']; means=np.array(d['mean']); sd=np.array(d['std'])
    colors=S['assignments']['comparison']
    f=plt.figure(figsize=(13,4.6)); axes=[]
    gap=6/72
    w=(13-.70-.18-2*gap)/3
    for j,metric in enumerate(d['metrics']):
        ax=add_axes(f,.70+j*(w+gap),.39,w,3.10,grid=''); axes.append(ax)
        bars=ax.bar(np.arange(9),means[:,j],width=S['bar_width'],color=colors,
                    edgecolor=INK,lw=S['bar_edge'],yerr=sd[:,j],
                    error_kw=dict(ecolor=INK,elinewidth=S['error'],capsize=S['cap'],capthick=S['error']))
        assert np.array_equal([b.get_height() for b in bars],means[:,j])
        segments=bars.errorbar.lines[2][0].get_segments()
        assert np.allclose([v[:,1] for v in segments], np.column_stack([means[:,j]-sd[:,j],means[:,j]+sd[:,j]]))
        for x,(v,e) in enumerate(zip(means[:,j],sd[:,j])):
            ax.text(x,v+e+.025,f'{v:.3f}',ha='center',va='bottom',fontsize=FONT_PT)
        ax.set(xlim=(-.6,8.6),ylim=(0,1.04),xticks=[],yticks=[])
        panel(ax,string.ascii_uppercase[j],metric)
        if j==0:ax.set_ylabel('Score')
    handles=[Patch(facecolor=c,edgecolor=INK,lw=.35,label=n.replace('BigMHC$_\\text{retrained}$','BigMHC retrained'))
             for n,c in zip(d['methods'],colors)]
    f.legend(handles=row_major_handles(handles,3),loc='upper left',bbox_to_anchor=(.70/13,.99,(13-.70-.18)/13,0),
             mode='expand',borderaxespad=0,borderpad=0,ncols=3,handlelength=1.3,columnspacing=3.0,labelspacing=.55)
    info=dict(layout='1 x 3',panel_size_inches=[w,3.10],horizontal_gap_inches=gap,
              identical_y_limits=[0,1.04],bar_baselines_zero=True,values_and_SD_preserved=True,
              category_order=d['methods'],all_data_labels=True,
              adaptation='Zero-based axes replace the earlier cropped bar axes; direct values replace numeric ticks and grids.')
    return f,info


def composition():
    gap=6/72
    f=plt.figure(figsize=(13.0,7.5)); w=(13-.90-.20-3*gap)/4; h=2.50
    colors=S['assignments']['composition']; hatches=['///','\\\\\\','','xx']
    descriptors=['Only model brute force','Only human brute force','Neither brute force','Both brute force']
    arrays=[]; placed=[]
    for row,key in enumerate(('brute_force_math','brute_force_logic')):
        d=DATA[key]
        for col,prompt in enumerate(d['prompts']):
            y=3.75 if row==0 else .70
            ax=add_axes(f,.90+col*(w+gap),y,w,h,grid='y')
            values=np.array(d['result'][prompt]); bottom=np.zeros(7)
            for k in range(4):
                bars=ax.bar(np.arange(7),values[:,k],bottom=bottom,width=S['bar_width'],color=colors,
                            hatch=hatches[k],edgecolor=S['hatch_color'],lw=S['bar_edge'],
                            alpha=1 if k==0 else S['composition_alpha'])
                assert np.allclose([b.get_height() for b in bars],values[:,k],rtol=0,atol=1e-15)
                assert np.allclose([b.get_y() for b in bars],bottom,atol=1e-15)
                bottom+=values[:,k]
            for x,v in enumerate(values[:,0]):
                ax.text(x,v+.014,f'{v:.3f}',ha='center',va='bottom',fontsize=FONT_PT,color=INK,
                        bbox=dict(facecolor=BG,edgecolor='none',pad=.35,alpha=.98))
            ax.set(xlim=(-.6,6.6),ylim=(0,1.035),xticks=range(7),xticklabels=[str(i+1) for i in range(7)],
                   yticks=[0,.25,.5,.75,1],yticklabels=['0','0.25','0.50','0.75','1.00'])
            panel(ax,string.ascii_uppercase[row*4+col],prompt.replace('Prompt','prompt'))
            if col==0:ax.set_ylabel(('Math' if row==0 else 'Logic')+'\nProbability')
            else:ax.tick_params(labelleft=False)
            if row==0:ax.tick_params(labelbottom=False)
            arrays.append(values);placed.append(ax)
    # Two rows of labeled color keys, relocated below the complete grid at export; original method names retained.
    names=DATA['brute_force_math']['methods']
    handles=[Patch(facecolor=c,edgecolor=INK,lw=.35,label=f'{i+1}  {name}') for i,(name,c) in enumerate(zip(names,colors))]
    f.legend(handles=row_major_handles(handles,4),loc='upper left',bbox_to_anchor=(.90/13,.99,(13-.90-.20)/13,0),
             mode='expand',borderaxespad=0,borderpad=0,ncols=4,fontsize=SMALL,handlelength=1.05,columnspacing=1.7,labelspacing=.55)
    f.legend(handles=[Patch(facecolor=BG,edgecolor=S['hatch_color'],hatch=h,lw=.35,label=n)
                      for h,n in zip(hatches,descriptors)],loc='upper left',bbox_to_anchor=(.90/13,.907,(13-.90-.20)/13,0),
             mode='expand',borderaxespad=0,borderpad=0,ncols=4,handlelength=1.5,columnspacing=2.5)
    f.text(.51,.025,'Model (see numbered color key)',ha='center',fontsize=10,fontweight='bold')
    info=dict(layout='2 x 4',panel_size_inches=[w,h],horizontal_gap_inches=gap,vertical_gap_inches=.55,
              shared_x_limits=[-.6,6.6],shared_y_limits=[0,1.035],source_values_preserved=True,
              segment_count=224,minimum_stack_total=float(min(a.sum(1).min() for a in arrays)),
              maximum_stack_total=float(max(a.sum(1).max() for a in arrays)),
              dense_value_label_size_pt=FONT_PT,
              adaptation='All eight panels and all seven model colors are retained. Small rounding deviations in stack totals are preserved.')
    return f,info


def geometry(ax):
    result=[]
    for line in ax.lines:
        result.append(np.asarray(line.get_xydata(),dtype=float).tobytes())
    for collection in ax.collections:
        if isinstance(collection,PathCollection):result.append(np.asarray(collection.get_offsets(),dtype=float).tobytes())
        else:
            for path in collection.get_paths():result.append(np.asarray(path.vertices,dtype=float).tobytes())
    return hashlib.sha256(b''.join(result)).hexdigest()


def concept():
    spec=importlib.util.spec_from_file_location('upstream_concept',ROOT/'upstream/figure_VIGIL/plot_concept.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    f=plt.figure(figsize=(13.0,4.75))
    left=add_axes(f,.68,.60,4.70,3.40)
    right=add_axes(f,5.94,.60,6.83,3.40,grid='')
    x=np.linspace(0,1,1000)
    values=[module._gauss(x,.30,.07),.30*module._gauss(x,.30,.12)+.22,module._gauss(x,.72,.07)]
    labels=[r'$P(y\mid x_t)$',r'$P(y\mid x_v^{\emptyset},x_t)$',r'$P(y\mid x_v,x_t)$']
    for y,c,label in zip(values,[NEUTRAL,BRICK,BLUE],labels):
        ln,=left.plot(x,y,color=c,lw=S['line'],label=label)
        assert np.array_equal(ln.get_ydata(),y)
        left.fill_between(x,0,y,color=c,alpha=S['fill_alpha'],lw=0)
    star=.72;lo=np.interp(star,x,values[1]);hi=np.interp(star,x,values[2])
    left.vlines(star,0,1,lw=.65,ls=':',color=MUTED)
    left.annotate('',xy=(star,hi),xytext=(star,lo),arrowprops=dict(arrowstyle='<->',color=INK,lw=.65))
    left.text(star+.045,(lo+hi)/2,'VIG',fontsize=SMALL,va='center')
    left.set(xlim=(0,1.05),ylim=(0,1.08),xticks=[0,.5,1],xticklabels=['-1','0','1'],
             yticks=[0,.2,.4,.6,.8,1],xlabel='Answer space (arbitrary units)',ylabel='Probability')
    panel(left,'A','Conditional distributions')
    f.legend(*left.get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.68/13,.99,4.70/13,0),
             mode='expand',borderaxespad=0,borderpad=0,ncols=3,handlelength=1.8,columnspacing=1.4)
    module.plot_manifold(right)
    before=geometry(right)
    mappings={'#2E74B5':BLUE,'#1f77b4':BLUE,'#6F6F6F':NEUTRAL,'#6b7280':NEUTRAL,'#D62728':BRICK,'#000000':INK}
    def recolor(color):
        v=np.array(to_rgba(color))
        for a,b in mappings.items():
            if np.allclose(v[:3],to_rgb(a)):return (*to_rgb(b),v[3])
        return v
    for ln in right.lines:
        ln.set_color(recolor(ln.get_color()))
        ln.set_linewidth(S['line'] if len(ln.get_xdata())>2 else .65)
        ln.set_markersize(min(S['marker'],ln.get_markersize()*.5))
        if ln.get_marker()=='o':ln.set_markerfacecolor(BG);ln.set_markeredgewidth(.625)
    for coll in right.collections:
        for getter,setter in ((coll.get_facecolors,coll.set_facecolors),(coll.get_edgecolors,coll.set_edgecolors)):
            colors=getter()
            if len(colors):setter([recolor(c) for c in colors])
        coll.set_linewidths(np.minimum(S['line'],np.array(coll.get_linewidths())*.4))
        if isinstance(coll,PathCollection):coll.set_sizes(coll.get_sizes()*.20)
    for txt in right.texts:
        txt.set_parse_math(True)
        txt.set_fontfamily(FONT);txt.set_fontweight('normal');txt.set_fontsize(SMALL)
        txt.set_color(INK)
        if txt.get_bbox_patch():txt.get_bbox_patch().set_facecolor(BG)
        if isinstance(txt,Annotation) and txt.arrow_patch:
            txt.arrow_patch.set_linewidth(.65);txt.arrow_patch.set_mutation_scale(6)
    xmin,xmax=right.get_xlim();right.set_xlim(xmin-.8,xmax+2.0)
    for txt in right.texts:
        if txt.get_text().startswith('Multimodal manifold'):
            txt.set_transform(right.transAxes);txt.set_position((.035,.965));txt.set_va('top')
        elif txt.get_text().startswith('Textual manifold'):
            txt.set_transform(right.transAxes);txt.set_position((.035,.035));txt.set_va('bottom')
        elif txt.get_text() in ('grounded','prior-dominated'):
            txt.set_x(right.get_xlim()[1]-.35);txt.set_ha('right')
    style_axes(right,grid='');right.set_xticks([]);right.set_yticks([])
    panel(right,'B','Illustrative representation space')
    assert before==geometry(right)
    return f,dict(layout='1 x 2',panel_size_inches=[[4.70,3.4],[6.83,3.4]],horizontal_gap_inches=.56,
                  distribution_points=3000,manifold_seed=42,manifold_points=5200,
                  source_manifold_geometry_sha256=before,geometry_preserved=True,
                  adaptation='Panels share top and bottom edges; the wider schematic retains the original deterministic geometry. Original formulas use Mathtext at a 10 pt base, Arial letters, STIX symbols and conventional reduced subscripts/superscripts.')


def trends():
    d=DATA['trends'];monthly=np.array(d['pub_by_month']);cumulative=np.cumsum(monthly,axis=1)
    count=monthly.shape[1]
    months=[f'{2022+(10+i)//12}-{(10+i)%12+1:02}' for i in range(count)]
    f=plt.figure(figsize=(13,7.5)); axs=[]; events_shown=[]; skipped=[]
    x=np.arange(count)
    for row,key in enumerate(('dates_llm','dates_vlm')):
        ax=add_axes(f,.85,4.07 if row==0 else .60,11.90,2.65);axs.append(ax)
        method=cumulative[row*2];evaluation=cumulative[row*2+1]
        ax.fill_between(x,0,evaluation,color=BRICK,alpha=S['area_alpha'][0],lw=0)
        ax.fill_between(x,0,method,color=BLUE,alpha=S['area_alpha'][1],lw=0)
        for y,c,name in [(evaluation,BRICK,'Evaluation / application'),(method,BLUE,'Methodological contribution')]:
            ln,=ax.plot(x,y,color=c,lw=S['line'],label=name)
            assert np.array_equal(ln.get_ydata(),y)
        ax.set(xlim=(-1.2,33.2),ylim=(0,125),yticks=[0,25,50,75,100,125])
        ticks=list(range(2,count,6))
        ax.set_xticks(ticks,[months[i] for i in ticks])
        if row==0:ax.tick_params(labelbottom=False)
        else:ax.set_xlabel('Month')
        panel(ax,'A' if row==0 else 'B','Text-only' if row==0 else 'Multimodal')
        # Preserve the source's effective event selection. Labels are moved, dates are not.
        events=[]
        for date,label in d[key].items():
            if date in months:events.append((months.index(date),date,label.replace('*','')))
            else:skipped.append(dict(group=key,date=date,label=label,reason='Not an exact date in the source month vector'))
        events.sort()
        for i,(idx,date,label) in enumerate(events):
            offset=13 if i%2==0 else 27
            target=min(float(evaluation[idx])+offset,114)
            ax.annotate(label,xy=(idx,evaluation[idx]),xytext=(idx,target),ha='center',va='bottom',
                        fontsize=FONT_PT,color=INK,linespacing=1.1,
                        arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=.55,mutation_scale=5,shrinkA=2,shrinkB=1))
            events_shown.append(dict(group=key,date=date,label=label,index=idx,value=int(evaluation[idx])))
        # Both series carry direct ending values without repeating their full names.
        ax.text(count-1+.38,evaluation[-1],str(evaluation[-1]),color=INK,va='center',fontsize=SMALL)
        ax.text(count-1+.38,method[-1],str(method[-1]),color=BLUE,va='center',fontsize=SMALL)
    f.text(.024,.49,'Cumulative publication count',ha='center',va='center',rotation=90,fontsize=10,fontweight='bold')
    f.legend(*axs[0].get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.85/13,.99,11.90/13,0),
             mode='expand',borderaxespad=0,borderpad=0,ncols=2,columnspacing=3,handlelength=2.0)
    assert axs[0].get_ylim()==axs[1].get_ylim()
    return f,dict(layout='2 x 1',panel_size_inches=[11.90,2.65],vertical_gap_inches=.82,
                  common_y_limits=[0,125],common_x_limits=[-1.2,33.2],monthly_values_preserved=True,
                  cumulative_values=cumulative.tolist(),months=months,events_shown=events_shown,
                  events_omitted_as_in_source=skipped,
                  adaptation='Both rows now share a 0-125 count scale; the earlier separate row scales are removed. Source event selection and every monthly count are preserved.')


EXAMPLES=[
    dict(slug='iedb-three-metrics',title='IEDB Benchmark Comparison',subtitle='Three metrics, nine methods; means with supplied standard deviations',
         source='Source: Chen Liu, figures4papers / figure_ImmunoStruct/raw_data.py. CC BY-NC 4.0.',
         note='AUROC, AUPRC and mean PPVn retain all original values. All bars start at zero and use the same scale. Values are shown above their error bars.',
         old='bars_comparison_IEDB',builder=benchmark),
    dict(slug='brute-force-eight-panels',title='Brute-Force Composition Across Prompts and Tasks',
         subtitle='Four prompt conditions for math and logic; seven models in every panel',
         source='Source: Chen Liu, figures4papers / figure_Brainteaser/plot_brute_force.py. CC BY-NC 4.0.',
         note='Numbers within panels label the only-model-brute-force segment. Small source rounding differences in total probability are preserved. Every panel has the same scale.',
         old='brute_force',builder=composition),
    dict(slug='concept-two-panels',title='Conditional Distributions and Representation Space',
         subtitle='Original conceptual curves and seed-42 manifold illustration',
         source='Source: Chen Liu, figures4papers / figure_VIGIL/plot_concept.py. CC BY-NC 4.0.',
         note='Both panels are illustrative, not new measurements. The original curves, point coordinates and trajectories are retained; colors, typography and annotation placement are restyled.',
         old='concept',builder=concept),
    dict(slug='publication-trends-two-panels',title='Publication Trends in Text-Only and Multimodal Work',
         subtitle='Cumulative counts from the repository, November 2022-July 2025',
         source='Source: Chen Liu, figures4papers / figure_ophthal_review/plot_trend.py. CC BY-NC 4.0.',
         note='Both panels share the same count scale. All monthly counts are retained. Release annotations follow the effective dates and labels in the source code.',
         old='trend_by_month',builder=trends),
]


def wrap(text,width_pt,size):
    renderer=RendererAgg(10,10,72);props=FontProperties(family=FONT,size=size)
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if line and renderer.get_text_width_height_descent(candidate,props,ismath=False)[0]>width_pt:
            lines.append(line);line=word
        else:line=candidate
    lines.append(line);return '\n'.join(lines)


def booklet_page(chart_path,spec,index):
    if MINIMAL:return fitz.open(chart_path)
    with fitz.open(chart_path) as d:
        cw,ch=d[0].rect.width,d[0].rect.height
    pw,ph=PAGE_W,PAGE_H
    f=plt.figure(figsize=(pw/72,ph/72))
    def text(top,body,size=FONT_PT,color=INK,weight='normal'):
        return f.text(36/pw,1-top/ph,wrap(body,cw,size),va='top',ha='left',fontsize=size,color=color,fontweight=weight,linespacing=1.3)
    def after(artist,gap=10):
        f.canvas.draw()
        return ph-artist.get_window_extent(f.canvas.get_renderer()).y0*72/f.dpi+gap
    tag=text(15,f'MULTI-PANEL {index}  /  R1 + S3  /  10 PT ARIAL',color=BLUE)
    title=text(after(tag,8),spec['title'],weight='bold')
    subtitle=text(after(title,3),spec['subtitle'],10)
    chart_top=after(subtitle,6)
    source=text(chart_top+ch+7.5,spec['source'],size=T['sources_pt'])
    note=text(after(source,6),spec['note'],size=T['notes_pt'],color=MUTED)
    assert after(note,0)<681,(spec['slug'],'booklet overflow')
    path=TEMP/f'{spec["slug"]}-page.pdf';f.savefig(path);plt.close(f)
    page=fitz.open(path)
    with fitz.open(chart_path) as chart:page[0].show_pdf_page(fitz.Rect(36,chart_top,36+cw,chart_top+ch),chart,0)
    return page


def validate(f,spec,info):
    f.canvas.draw();r=f.canvas.get_renderer();outside=[];bold=[]
    assert np.allclose(f.get_facecolor(),to_rgba(S['canvas']))
    bold_text={ax.get_title(loc='left') for ax in f.axes}
    bold_text.update(t.get_text() for ax in f.axes for t in [ax.xaxis.label,ax.yaxis.label])
    bold_text.update(['Model (see numbered color key)','Cumulative publication count'])
    for txt in f.findobj(Text):
        if not txt.get_visible() or not txt.get_text():continue
        assert txt.get_fontsize()==10,(spec['slug'],txt.get_text(),txt.get_fontsize())
        assert txt.get_fontfamily()==['Arial'],(spec['slug'],txt.get_text(),txt.get_fontfamily())
        assert txt.get_fontweight()==('bold' if txt.get_text() in bold_text else 'normal'),(spec['slug'],txt.get_text(),txt.get_fontweight())
        box=txt.get_window_extent(r)
        if box.x0 < -1 or box.y0 < -1 or box.x1>f.bbox.width+1 or box.y1>f.bbox.height+1:
            outside.append(txt.get_text())
    assert not outside,(spec['slug'],outside)
    for ax in f.axes:
        assert np.allclose(ax.get_facecolor()[:3],to_rgb(BG))
        assert all(sp.get_visible() and sp.get_linewidth()==.45 for sp in ax.spines.values())
        for t in [ax.xaxis.label,ax.yaxis.label]:
            if t.get_text():
                assert t.get_fontweight()=='bold' and t.get_fontfamily()==[FONT]
                bold.append(t.get_text())
    scale=72/f.dpi
    legends=[lg.get_window_extent(r) for lg in f.legends]
    legend_clearance=(content_bounds(f)[0]-max(b.y1 for b in legends))*scale
    compact_height=f._layout_audit.get('full_block_height_factor',1)!=1
    vertical_scale=f._layout_audit.get('vertical_spacing_factor',1)
    assert legend_clearance>=10*vertical_scale-.1,(spec['slug'],'legend too close',legend_clearance)
    for lg in f.legends:
        boxes=[t.get_window_extent(r) for t in lg.get_texts()]
        assert not any(a.overlaps(b) for i,a in enumerate(boxes) for b in boxes[i+1:]),spec['slug']
    numeric_gaps=[]
    for ax in f.axes:
        vals=[t for t in ax.texts if t.get_text().startswith('0.')]
        for a,b in zip(vals,vals[1:]):
            numeric_gaps.append((b.get_window_extent(r).x0-a.get_window_extent(r).x1)*scale)
    if numeric_gaps:assert min(numeric_gaps)>=4,(spec['slug'],'value labels too close',min(numeric_gaps))
    info['spacing_audit']={
        **f._layout_audit,
        'minimum_value_label_horizontal_gap_pt':round(min(numeric_gaps),2) if numeric_gaps else None,
        'x_axis_title_pad_pt':8*vertical_scale,'y_axis_title_pad_pt':4,
        'x_tick_label_pad_pt':4*vertical_scale,
        'legend_text_overlap':False,
    }
    if compact_height:
        sizes=[[a.bbox.width/f.dpi,a.bbox.height/f.dpi] for a in f.axes]
        info['panel_size_inches']=sizes if isinstance(info['panel_size_inches'][0],list) else sizes[0]
        if 'vertical_gap_inches' in info:info['vertical_gap_inches']*=vertical_scale
    AUDIT.append(dict(slug=spec['slug'],panels=len(f.axes),canvas_inches=f.get_size_inches().tolist(),
                      font=FONT,base_text_size_pt=10,math_scripts_reduced=spec['slug']=='concept-two-panels',only_titles_bold=True,axis_titles_bold=True,
                      axis_titles=bold,all_text_inside_canvas=True,
                      canvas_color=S['canvas'],panel_color=BG,**info))


def gallery():
    cards=[]
    for spec in EXAMPLES:
        slug=spec['slug'];links=' '.join(f'<a href="figures/{slug}.{e}">{e.upper()}</a>' for e in ['png','pdf','svg'])
        with fitz.open(CHARTS/f'{slug}.pdf') as chart:cw,ch=chart[0].rect.width,chart[0].rect.height
        cards.append(f'<section><h2>{html.escape(spec["title"])}</h2><p>{html.escape(spec["subtitle"])}</p>'
                     f'<a href="figures/{slug}.png"><img width="{cw*96/72:.6f}" height="{ch*96/72:.6f}" src="figures/{slug}.png" alt="{html.escape(spec["title"]+". "+spec["note"])}"></a>'
                     f'<nav>{links}<a href="../s3-design-study/cobalt-brick-gold/{spec["old"]}.png">Earlier R1 version</a></nav>'
                     f'<p class="note">{html.escape(spec["note"])}</p></section>')
    (OUT/'gallery.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Multi-panel figures - Arial, R1 and S3</title>
<style>*{box-sizing:border-box}body{margin:0;background:'''+S['canvas']+''';color:#282828;font:10pt/1.5 Arial,sans-serif}main{max-width:calc(13in + 64px);margin:auto;padding:32px}h1,h2{font-size:10pt;font-weight:700}h1{margin:0 0 10px}a{color:#285F96}p{max-width:13in}nav{display:flex;flex-wrap:wrap;gap:22px}section{border-top:1px solid #CBD6DF;margin-top:35px;padding-top:12px}section{overflow-x:auto}img{max-width:none;display:block;border:1px solid #CBD6DF;margin:16px 0}.note{color:#666;font-size:8pt}@media(max-width:800px){main{padding:20px}}</style>
<main><h1>Four multi-panel figures: corrected math and refined spacing</h1><p>Figure text uses 10 pt Arial; source credits and notes use 8 pt Arial Regular. Figure, panel and axis titles are bold; other text is regular. Equations use a 10 pt base with conventional subscripts and superscripts and STIX fallback symbols. R1 categorical colors and the #D8E8F4 S3 plot panels sit on a lighter #EDF4F9 full-figure background, including titles, legends and source notes. Publication trends use 6.25-inch text-width artwork; three dense examples retain documented 13-inch exceptions. All are displayed at native scale. All original quantitative values are preserved.</p>
<nav><a href="'''+BOOK_NAME+'''">Corrected four-page PDF</a><a href="multipanel-r1-arial-source.zip">Charts and source code</a><a href="README.md">Layout specifications</a><a href="SPACING_REVIEW.md">Urban spacing review</a></nav>'''+''.join(cards)+'''<footer><p class="note">Source: Chen Liu / figures4papers, CC BY-NC 4.0. These are the four native multi-panel figures from the retained README examples.</p></footer></main></html>''')
    if MINIMAL:
        import re
        path=OUT/'gallery.html';contents=path.read_text()
        contents=re.sub(r'<section><h2>.*?</h2><p>.*?</p>', '<section>',contents,flags=re.S)
        contents=re.sub(r'<p class="note">.*?</p>', '',contents,flags=re.S)
        path.write_text(contents)
    shutil.copyfile(OUT/'gallery.html',OUT/'gallery-math-fixed.html')


def verify_exported_fonts():
    reports=[]
    for path in [OUT/BOOK_NAME,*sorted(CHARTS.glob('*.pdf'))]:
        with fitz.open(path) as d:
            fonts=set();sizes=set();count=0;script_count=0
            for page in d:
                for font in page.get_fonts():
                    assert len(d.extract_font(font[0])[-1])>0
                for b in page.get_text('dict')['blocks']:
                    for line in b.get('lines',[]):
                        for span in line['spans']:
                            count+=1;size=round(span['size'],3);sizes.add(size);fonts.add(span['font'])
                            assert size in ((7,10) if path.parent==CHARTS else (7,8,10)),(path,span)
                            if size==8:assert span['font']=='ArialMT',span
                            if size==7:script_count+=1
                            assert span['font'] in ('ArialMT','Arial-BoldMT','Arial-ItalicMT','STIXGeneral-Regular','STIXNonUnicode-Italic'),(path,span)
                            box=fitz.Rect(span['bbox'])
                            assert box.x0>=-1 and box.y0>=-1 and box.x1<=page.rect.width+1 and box.y1<=page.rect.height+1
                if path.parent==OUT and not MINIMAL:assert tuple(page.rect)==(0,0,PAGE_W,PAGE_H)
            if path.name=='concept-two-panels.pdf':assert script_count>0
            elif path.parent==CHARTS:assert sizes=={10}
            reports.append(dict(file=path.name,pages=len(d),text_spans=count,fonts=sorted(fonts),sizes_pt=sorted(sizes),
                                base_size_pt=10,conventional_script_spans=script_count,all_fonts_embedded=True,text_inside_canvas=True))
    (OUT/'font-verification.json').write_text(json.dumps(reports,indent=2)+'\n')


def spacing_review():
    review='''# Math and spacing review

Reviewed against the public Urban Institute guide and its official print-theme source on 2026-11-15.

## Reference check

The [published guide](https://urbaninstitute.github.io/graphics-styleguide/#chart-parts) places legends above charts, orders them to match the data, and calls for left-aligned titles. Its [small-multiple guidance](https://urbaninstitute.github.io/graphics-styleguide/#creating-effective-charts) calls for matching panel dimensions and scales for comparable charts. Its usual PDF figure width is 6.25 inches. It does not prescribe exact gaps for these mixed scientific layouts.

The [official R print theme](https://github.com/UrbanInstitute/urbnthemes/blob/master/R/theme_urbn_print.R) supplies implementation defaults: 6 pt panel spacing; 4 pt x-tick-label margin; 8 pt x-axis-title and 4 pt y-axis-title margins; 10 pt title/subtitle bottom margins; 6 pt top/bottom legend margins. These are defaults, not a complete multi-panel specification.

## What was polished

- Benchmark and composition horizontal panel gaps now use 6 pt. Panel widths remain equal within each grid; the recovered width also separates numeric labels more clearly.
- Legends extend across their associated plotting region, in data order. The concept legend applies only to the left panel.
- Legends sit below the complete plot and its axis labels, with a measured 7.5 pt clearance. Separate legend groups have 4.5 pt between them. This is the user-selected override to Urban's above-chart convention.
- The compact revision uses 6 pt x-title and 4 pt y-title padding, 3 pt x-tick padding and 4 pt y-tick padding. Matplotlib padding is measured from its tick-label box; this is an adaptation of the R margins, not a promise of pixel-identical output.
- Figure titles sit 3 pt above subtitles. Subtitles sit 8.25 pt above the first chart content, including panel headings (6 pt placement gap plus 2.25 pt export padding). Chart height and vertical gaps retain the approved 75%-height layout. Source/notes now use 8 pt, and article blocks fit their content with equal 13.5 pt top and bottom padding, without changing chart geometry. Timeline annotations are staggered to fit.
- The 0.4125-inch composition row gap and 0.615-inch timeline row gap leave space for panel headings and shared axes. The 0.56-inch mixed concept gap remains a local choice.

## Retained project choices

Text width is the default. The timeline is 6.25 inches wide; the dense benchmark, eight-panel composition and annotated concept examples retain explicit 13-inch exceptions. This differs from Urban's usual print width. Font, weight, palette, backgrounds and four-sided frames remain our selected overrides. These are Urban-informed layouts, not exact Urban reproductions.

## Math correction

Formula strings are restored from the original concept code. [Matplotlib Mathtext](https://matplotlib.org/stable/users/explain/text/mathtext.html) renders subscripts, superscripts, conditional bars, the empty-set symbol and calligraphic manifold symbols. Equations have a 10 pt base; normal subscript/superscript reduction produces 7 pt script glyphs. Letters use Arial/Arial Italic; STIX supplies symbols missing from Arial. Equations are not bold. The concept SVG outlines its glyphs for portable rendering; the other SVGs retain editable text.

## Measured clearances

| Figure | Plot labels to legend below | Minimum adjacent value-label gap |
|---|---:|---:|
'''
    for entry in AUDIT:
        a=entry['spacing_audit'];gap=a['minimum_value_label_horizontal_gap_pt']
        review+=f"| {entry['slug']} | {a['plot_labels_to_legend_pt']:.2f} pt | {f'{gap:.2f} pt' if gap is not None else 'Not applicable'} |\n"
    review+='\n`validation.json` records geometry and data checks; `font-verification.json` checks the exported font faces, point sizes, embedding and text bounds.\n'
    (OUT/'SPACING_REVIEW.md').write_text(review)


def main():
    setup();book=fitz.open()
    for i,spec in enumerate(EXAMPLES,1):
        f,info=spec['builder']();compact_layout(f,spec['slug']);validate(f,spec,info)
        for ext in ('png','pdf','svg'):
            # Outline the concept SVG so specialized math glyphs are portable.
            with mpl.rc_context({'svg.fonttype':'path' if spec['slug']=='concept-two-panels' else 'none'}):
                f.savefig(CHARTS/f'{spec["slug"]}.{ext}',dpi=300)
        plt.close(f)
        page=booklet_page(CHARTS/f'{spec["slug"]}.pdf',spec,i)
        page[0].get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(PREVIEWS/f'{spec["slug"]}.png')
        book.insert_pdf(page);page.close()
        print('Rendered',spec['slug'],flush=True)
    book.set_metadata({'title':'Multi-panel R1 / S3 - corrected math and spacing, 10 pt base','author':'Adapted from Chen Liu, figures4papers'})
    book.save(OUT/BOOK_NAME,garbage=4,deflate=True);book.close()
    shutil.copyfile(OUT/BOOK_NAME,OUT/'multipanel-r1-arial-10pt.pdf')
    verify_exported_fonts()
    (OUT/'validation.json').write_text(json.dumps({'figures':AUDIT,'source_data_sha256':hashlib.sha256((ROOT/'data.json').read_bytes()).hexdigest()},indent=2)+'\n')
    (OUT/'selected-style.json').write_text(json.dumps(SELECTED,indent=2)+'\n')
    (OUT/'data.json').write_bytes((ROOT/'data.json').read_bytes())
    spacing_review()
    gallery()
    doc='''# Multi-panel figures: 10 pt Arial, R1 and S3

[Gallery](gallery-math-fixed.html) · [Corrected four-page PDF](multipanel-r1-arial-10pt-math-fixed.pdf) · [Native PNG/PDF/SVG files](figures/) · [Urban spacing review](SPACING_REVIEW.md)

The four native multi-panel figures in the retained README examples are remade here. Numeric arrays and uncertainty values are preserved. The concept drawing retains the source generator, seed and coordinates. Native chart dimensions retain the approved 75%-height layout. Outer article blocks fit 8 pt source/notes with equal 13.5 pt top and bottom padding; chart geometry, widths and mark sizes remain fixed.

## Existing style applied

Figure text uses 10 pt Arial; source credits and notes use 8 pt Arial Regular. Figure titles, panel titles and axis titles are bold. Panel letters, tick labels, legends, value labels, annotations, subtitles, sources and notes are regular weight. Equations use a 10 pt base with conventional reduced subscripts/superscripts, Arial letters and STIX fallback symbols. Only source credits and notes use the smaller 8 pt size; plot annotations remain 10 pt. S3 plot panels are #D8E8F4. The full figure/page background is the matching paler blue #EDF4F9, including titles, subtitles, legends, source notes, margins and gutters. Frames are #566C7B at 0.45 pt; grids are dotted #CBD6DF at 0.45 pt. Curves are 1.25 pt and error bars 0.65 pt with 2 pt caps. All agreed R1 method-color mappings are retained. Concepts use 0.08 fill opacity; publication areas retain 0.14 / 0.22 opacity.

## Layout choices for this collection

Panel letters run left-to-right, then top-to-bottom in regular weight. Shared legends sit below their associated panels, 7.5 pt beneath the lowest axis label; separate legend groups have 4.5 pt between them. Title-to-subtitle spacing is 3 pt and subtitle-to-chart-content spacing is 8.25 pt. Outer titles, subtitles, sources and notes are separate page text in the booklet. Shared axes suppress redundant labels; bold titles identify the measured quantity. The spacing review distinguishes defaults taken from Urban's R theme from local layout choices.

| Figure | Layout | Full chart size | Panel gap |
|---|---|---|---|
| IEDB comparison | 1 x 3 | {benchmark_size} | 6 pt horizontal |
| Brute-force composition | 2 x 4 | {composition_size} | 6 pt horizontal; 0.4125 in vertical |
| Concept illustration | 1 x 2 | {concept_size} | 0.56 in horizontal |
| Publication trends | 2 x 1 | {trends_size} | 0.615 in vertical |

The timeline is 6.25 inches wide; the three dense exceptions are 13 inches wide. Styled booklet pages are 14 x 10 inches and embed charts at native scale. The gallery displays all figures with the same scale factor. PNGs are 300 dpi; PDF fonts are embedded. The concept SVG uses outlined glyphs to preserve mathematical rendering on other computers; other SVGs retain editable text. Formula labels use actual mathematical notation, including subscripts, superscripts and calligraphic symbols.

## Data and comparison decisions

- Benchmark bars start at zero, share 0-1.04 limits and retain every supplied mean and standard deviation. Three-decimal labels replace numeric ticks and grids. The original method order and nine-category palette are preserved.
- Composition retains all eight panels and 224 segments. Numbered model keys, shared probability scales and 10 pt value labels keep the complete source data visible. Stack totals of 0.999-1.001 reflect source rounding and are not normalized.
- Concept panel edges align; the schematic receives more width. Its 5,200 source points and original trajectories are preserved. Its annotations and arrows are repositioned or resized only for readability.
- Publication panels use the same 0-125 count scale. All 132 monthly counts and their cumulative sums are unchanged. Source events without an exact match in the original month vector remain omitted; the omissions are listed in validation.json. Event labels are historical source content, not independently verified release dates.

## Reproduce

`MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_multipanel_examples.py`

Dependencies: Matplotlib, NumPy, SciPy, PyMuPDF and Pillow; Arial Regular and Arial Bold must be installed. Original code and data: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), [CC BY-NC 4.0](../upstream/LICENSE).
'''
    for key,entry in zip(['benchmark','composition','concept','trends'],AUDIT):
        w,h=entry['canvas_inches'];doc=doc.replace('{'+key+'_size}',f'{w:.2f} x {h:.2f} in')
    (OUT/'README.md').write_text(doc)
    # Contact sheet: each native figure is available at full size through the gallery.
    thumb_w=1200;thumb_h=850
    overview=Image.new('RGB',(2440,1740),S['canvas'])
    for i,spec in enumerate(EXAMPLES):
        im=Image.open(PREVIEWS/f'{spec["slug"]}.png').convert('RGB');im.thumbnail((thumb_w,thumb_h),Image.Resampling.LANCZOS)
        overview.paste(im,(10+(i%2)*1220,10+(i//2)*870))
    overview.save(OUT/'overview.png')
    with zipfile.ZipFile(OUT/'multipanel-r1-arial-source.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in OUT.rglob('*'):
            if path.is_file() and path.suffix!='.zip' and TEMP not in path.parents:
                z.write(path,'figures4papers-minimal/'+path.relative_to(ROOT).as_posix())
        for path in [Path(__file__),ROOT/'README.md',ROOT/'figure_height.py',ROOT/'text_width.py',ROOT/'figure-height-baseline.json',ROOT/'selected-style.json',ROOT/'data.json',
                     ROOT/'upstream/LICENSE',ROOT/'upstream/figure_VIGIL/plot_concept.py']:
            z.write(path,'figures4papers-minimal/'+path.relative_to(ROOT).as_posix())
        for spec in EXAMPLES:
            path=ROOT/'s3-design-study/cobalt-brick-gold'/f'{spec["old"]}.png'
            z.write(path,'figures4papers-minimal/'+path.relative_to(ROOT).as_posix())
    print('Completed',OUT,flush=True)


if __name__=='__main__':main()
