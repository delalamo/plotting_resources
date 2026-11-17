"""Complete style exploration with fixed Helvetica typography and original data.

Run: python figures4papers-minimal/render_style_exploration.py
Writes only full-style-study/. It does not replace the approved default.
"""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/figures4papers-mpl')
from pathlib import Path
from copy import deepcopy
from contextlib import contextmanager
from dataclasses import replace, asdict
import json, hashlib, textwrap, html
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import to_rgb, to_rgba
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.text import Text, Annotation
from matplotlib.collections import PathCollection
import minimal_theme as theme
import render_examples as r
from render_palette_study import palette
from palette_color_math import contrast, simulate, oklab
from palette_schemes import SCHEMES
from style_directions import DIRECTIONS, BACKGROUNDS, LINE_WEIGHTS, direction

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'full-style-study'
BASE=theme.T
BASE_PALETTE=deepcopy(theme.PALETTES)
DEFAULT_AXES=theme.style_axes
METHODS=list(r.post.data_posttraining['methods'])
MARKERS=['s','^','o']
DASHES=[(0,(4,2)),(0,(3,1.5,1,1.5)),'-']
REFERENCE=direction('S0','approved','Approved reference','P1',caption='Existing cream B style, retained as the visual anchor.')
REFERENCE['palette'].update(colors=[BASE.teal,BASE.rust,BASE.ochre,'#A08397','#778958','#54788D'],neutral=BASE.taupe)
REFERENCE['dashes']=False
REFERENCE.update(marker_edge=.4,baseline_width=.8)

def assignments(s):
    if s['id']=='S0':return deepcopy(BASE_PALETTE)
    p=palette(s['palette'])
    if s['emphasis']:p['comparison']=[s['palette']['neutral']]*8+[s['palette']['colors'][0]]
    return p

def style_axes(ax,s,grid='y'):
    policy='' if grid=='' or s['grid']=='none' else s['grid']
    DEFAULT_AXES(ax,grid=policy)
    ax.xaxis.label.set_color(s['ink']);ax.yaxis.label.set_color(s['ink'])
    visible={'box':{'left','right','top','bottom'},'left-bottom':{'left','bottom'},'bottom':{'bottom'},'none':set()}[s['frame']]
    for name,spine in ax.spines.items():
        spine.set_visible(name in visible)
        spine.set_color(s['frame_color']);spine.set_linewidth(s['frame_width'])
    ax.tick_params(axis='both',which='major',length=s['ticks'],width=max(.4,s['frame_width']),
                   direction='out',color=s['frame_color'],labelcolor=s['ink'])
    for line in ax.get_xgridlines()+ax.get_ygridlines():
        line.set_color(s['grid_color']);line.set_linewidth(s['grid_width']);line.set_linestyle(s['grid_style'])

@contextmanager
def use_style(s):
    saved=(theme.T,r.T,theme.PALETTES,r.PALETTES,theme.style_axes,r.style_axes)
    c=s['palette']['colors']
    try:
        theme.T=r.T=replace(BASE,background=s['panel'],ink=s['ink'],muted=s['muted'],
            grid_color=s['grid_color'],frame_color=s['frame_color'],line=s['line'],error=s['error'],
            grid=s['grid_width'],frame=s['frame_width'],marker=s['marker'],
            teal=c[0],rust=c[1],ochre=c[2],taupe=s['palette']['neutral'],scatter=c[0])
        theme.PALETTES=r.PALETTES=assignments(s)
        theme.style_axes=r.style_axes=lambda ax,grid='y':style_axes(ax,s,grid)
        with mpl.rc_context():
            theme.apply_theme()
            mpl.rcParams.update({'figure.facecolor':s['canvas'],'savefig.facecolor':s['canvas'],
                'hatch.color':s['hatch_color'],'hatch.linewidth':s['hatch_width']})
            yield
    finally:
        theme.T,r.T,theme.PALETTES,r.PALETTES,theme.style_axes,r.style_axes=saved

def set_method_line(line,s,index,radar=False):
    color=assignments(s)['methods'][index]
    line.set_color(color);line.set_linewidth(s['line'])
    line.set_marker('o' if s['id']=='S0' else MARKERS[index]);line.set_markersize(s['marker']*(.8 if radar else 1))
    line.set_markeredgewidth(s.get('marker_edge',max(.5,s['line']*.5)));line.set_markeredgecolor(color)
    line.set_markerfacecolor(s['panel'] if s['marker_fill']=='open' else color)
    line.set_linestyle(DASHES[index] if s['dashes'] and not radar else '-')

def fingerprint(fig):
    """Data vertices, bar centers/heights and ranges, excluding permitted visual changes."""
    values=[]
    for ax in fig.axes:
        values.extend([np.round(ax.get_xlim(),9).tolist(),np.round(ax.get_ylim(),9).tolist()])
        for line in ax.lines:values.append(np.round(line.get_xydata(),9).tolist())
        for patch in ax.patches:
            if isinstance(patch,Rectangle):values.append(np.round([patch.get_x()+patch.get_width()/2,patch.get_y(),patch.get_height()],9).tolist())
        for collection in ax.collections:
            values.append(np.asarray(collection.get_offsets()).round(9).tolist())
            values.extend(p.vertices.round(9).tolist() for p in collection.get_paths())
    return hashlib.sha256(json.dumps(values,default=float).encode()).hexdigest()

def finish(fig,s,name):
    fig.set_facecolor(s['canvas'])
    for text in fig.findobj(Text):
        text.set_color(s['muted'] if text.get_color()==theme.T.muted else s['ink'])
        box=text.get_bbox_patch()
        if box:box.set_facecolor(s['panel'])
        if isinstance(text,Annotation) and text.arrow_patch:
            text.arrow_patch.set_color(s['muted']);text.arrow_patch.set_linewidth(s['error'])
    for ax in fig.axes:
        for line in ax.lines:
            label=line.get_label()
            if label in METHODS:set_method_line(line,s,METHODS.index(label),ax.name=='polar')
            elif label=='SFT only':line.set_color(s['muted']);line.set_linewidth(max(.6,s['line']*.55))
            elif line.get_marker()=='_':
                line.set_markersize(2*s['cap']);line.set_markeredgewidth(s['error']);line.set_color(s['ink'])
        if name in ('bars_comparison_IEDB','brute_force'):
            for i,bar in enumerate(ax.patches):
                center=bar.get_x()+bar.get_width()/2
                bar.set_width(s['bar_width']);bar.set_x(center-s['bar_width']/2)
                if name=='bars_comparison_IEDB':
                    bar.set_edgecolor(s['ink'] if s['bar_edge'] else 'none');bar.set_linewidth(s['bar_edge'])
                else:
                    bar.set_edgecolor(s['hatch_color']);bar.set_linewidth(s['hatch_width'])
                    bar.set_alpha(1 if i<7 else s['composition_alpha'])
            if s['emphasis']:
                n=9 if name=='bars_comparison_IEDB' else 7
                ax.set_xticks(range(n),[str(i+1) for i in range(n)])
        if name=='trend_by_month':
            for coll,alpha in zip(ax.collections,s['area_alpha']):coll.set_alpha(alpha)
        if name=='concept':
            if ax is fig.axes[0]:
                for coll in ax.collections[:3]:coll.set_alpha(s['fill_alpha'])
            else:
                factor=s['line']/BASE.line
                for line in ax.lines:
                    line.set_linewidth(line.get_linewidth()*factor)
                    line.set_markersize(line.get_markersize()*s['marker']/BASE.marker)
                    try:
                        if np.mean(to_rgb(line.get_color()))<.18:line.set_color(s['ink'])
                    except (ValueError,TypeError):pass
                for coll in ax.collections:
                    coll.set_linewidths(np.asarray(coll.get_linewidths())*factor)
                    if isinstance(coll,PathCollection):
                        coll.set_sizes(coll.get_sizes()*(s['marker']/BASE.marker)**2)
                        if s['id']=='S8':
                            for getter,setter in [(coll.get_facecolors,coll.set_facecolors),(coll.get_edgecolors,coll.set_edgecolors)]:
                                rgba=getter().copy()
                                if len(rgba):
                                    rgba[np.mean(rgba[:,:3],axis=1)<.18,:3]=to_rgb(s['ink'])
                                    setter(rgba)
                for patch in ax.patches:
                    if isinstance(patch,FancyArrowPatch):
                        patch.set_color(s['ink']);patch.set_linewidth(s['error'])
        if ax.name=='polar':
            for patch in ax.patches:patch.set_alpha(s['radar_alpha'])
            for line in ax.lines:
                if line.get_label() not in METHODS:
                    line.set_linestyle(s['grid_style']);line.set_color(s['grid_color'])
                    line.set_linewidth(s['grid_width'])
    if name=='comparison_radar':
        for artist in fig.artists:
            if isinstance(artist,Rectangle):
                artist.set_edgecolor(s['frame_color'] if s['frame']=='box' else 'none')
                artist.set_linewidth(s['frame_width'])
    legends=list(fig.legends)+[ax.get_legend() for ax in fig.axes if ax.get_legend()]
    for legend in legends:
        for index,(text,handle) in enumerate(zip(legend.get_texts(),legend.legend_handles)):
            label=text.get_text();text.set_color(s['ink'])
            if label in METHODS and isinstance(handle,Line2D):set_method_line(handle,s,METHODS.index(label),name=='comparison_radar')
            elif label=='SFT only' and isinstance(handle,Line2D):handle.set_color(s['muted'])
            if s['emphasis'] and name=='bars_comparison_IEDB':text.set_text(f'{index+1}  {label}')
            if s['emphasis'] and name=='brute_force' and legend is fig.legends[0]:text.set_text(f'{index+1}  {label}')
        if name=='trend_by_month':
            for handle,alpha in zip(legend.legend_handles,s['area_alpha']):handle.set_alpha(alpha)
        if name=='brute_force' and legend is fig.legends[-1]:
            for handle in legend.legend_handles:
                handle.set_facecolor(s['palette']['neutral'] if s['id']=='S8' else s['panel'])
                handle.set_edgecolor(s['hatch_color']);handle.set_linewidth(s['hatch_width'])
    return fig

def draw_line(ax,s,direct=True):
    d=r.post.data_posttraining
    ax.axhline(22,color=s['muted'],lw=s.get('baseline_width',max(.6,s['line']*.55)),ls=(0,(4,3)))
    for i,y in enumerate(d['results']):
        line,=ax.plot(d['steps'],y);set_method_line(line,s,i)
        if direct:ax.text(840,y[-1],['DPO','DA-DPO','VIGIL'][i],fontsize=BASE.small,color=s['ink'],va='center')
    if direct:ax.text(840,22,'SFT',fontsize=BASE.small,color=s['muted'],va='bottom')
    ax.set(xlim=(-25,1070 if direct else 825),ylim=(0,63),xticks=[0,400,800],yticks=[0,20,40,60],xlabel='Post-training steps',ylabel='Performance')
    style_axes(ax,s)

def write_text(fig,x,y,body,size=11,width=None,color='#282828',**kwargs):
    if width:body='\n'.join(textwrap.fill(p,width=width,break_long_words=False,break_on_hyphens=False) for p in body.split('\n'))
    return fig.text(x,y,body,ha='left',va='top',fontsize=size,fontfamily=theme.FONT,fontweight='normal',color=color,linespacing=1.4,**kwargs)

def page(title,subtitle,n,size=(13.5,11.5),canvas='#FFFFFF',ink='#282828'):
    fig=plt.figure(figsize=size,facecolor=canvas)
    write_text(fig,.05,.96,title,22,color=ink)
    write_text(fig,.05,.913,subtitle,10,color=ink)
    fig.add_artist(Line2D([.05,.95],[.878,.878],transform=fig.transFigure,lw=.55,color=ink))
    write_text(fig,.05,.028,'FULL STYLE EXPLORATION  /  Fixed Helvetica Regular  /  Original source data',8,color=ink)
    fig.text(.95,.028,str(n),ha='right',va='top',fontsize=8,color=ink)
    return fig

def matrix(title,subtitle,styles,n,notes,rows=3,cols=3):
    fig=page(title,subtitle,n)
    available=.77;rowheight=available/rows
    for i,s in enumerate(styles):
        col=i%cols;row=i//cols;x=.055+col*.31;y=.865-(row+1)*rowheight
        # Each tile shows the candidate's actual figure margin color too.
        fig.add_artist(Rectangle((x-.008,y+.008),.302,rowheight-.01,facecolor=s['canvas'],edgecolor='#DDDAD3',linewidth=.4,transform=fig.transFigure,zorder=-1))
        write_text(fig,x+.008,y+rowheight-.022,s['name'],12,color=s['ink'])
        write_text(fig,x+.008,y+rowheight-.05,notes[i],8.2,color=s['muted'])
        ax=fig.add_axes([x+.034,y+.055,.248,rowheight-.128])
        with use_style(s):draw_line(ax,s)
    return fig

def overview():
    ss=[REFERENCE]+DIRECTIONS
    return matrix('Eight complete plotting directions','Same typeface, type sizes and data. Background, palette, strokes, axes, grids, markers and fills vary.',ss,1,
        [s['id']+'  |  '+s['panel']+'  |  '+str(s['line'])+' pt curves' for s in ss])

def controls():
    base=direction('control','control','Control','P2')
    bgs=[dict(deepcopy(base),name=name,panel=color) for name,color in BACKGROUNDS]
    yield 'backgrounds',matrix('Background colors in isolation','Only the panel background varies: P2 palette, 1.15 pt curves, 0.55 pt black frame, identical typography.',bgs,2,[s['panel'] for s in bgs])
    weights=[dict(deepcopy(base),name=f'{v:.2f} pt curves',line=v,marker_edge=.575,baseline_width=.8) for v in LINE_WEIGHTS]
    yield 'line-weights',matrix('Line weight in isolation','Only data-curve width varies. Marker size and marker outlines are fixed here; 1.15 pt is the approved reference.',weights,3,
        ['0.55 pt frame  |  3.5 pt markers']*6,rows=2)
    structures=[dict(deepcopy(base),name='Full frame + y grid'),
        dict(deepcopy(base),name='Full frame, no grid',grid='none',ticks=2.5),
        dict(deepcopy(base),name='Open axes + y grid',frame='left-bottom',ticks=2.5),
        dict(deepcopy(base),name='Bottom axis only',frame='bottom'),
        dict(deepcopy(base),name='No frame + y grid',frame='none'),
        dict(deepcopy(base),name='Full frame + dotted xy grid',grid='xy',grid_style=':')]
    yield 'axes-grids',matrix('Axes, frames and grid treatments','Palette, background, typography, curve width and marker sizes stay fixed.',structures,4,
        [s['frame']+'  |  ticks '+str(s['ticks'])+' pt' for s in structures],rows=2)
    samples=[]
    for fill in ['filled','open']:
        for alpha in [0,.12,.30]:
            samples.append(dict(deepcopy(base),name=f'{fill.capitalize()} markers / {int(alpha*100)}% fill',marker_fill=fill,fill_alpha=alpha))
    fig=matrix('Markers and area fills','Two marker treatments crossed with three fill opacities. All other plotting tokens stay fixed.',samples,5,['Fixed 1.15 pt curves  |  3.5 pt markers']*6,rows=2)
    # The same controlled curves plus translucent area to demonstrate layered fills.
    for ax,s in zip(fig.axes,samples):
        for color,y in zip(assignments(s)['methods'],r.post.data_posttraining['results']):
            ax.fill_between(r.post.data_posttraining['steps'],0,y,color=color,alpha=s['fill_alpha'],linewidth=0,zorder=1)
    write_text(fig,.05,.06,'Area fills demonstrate appearance only; they are not uncertainty bands or new source measurements.',9)
    yield 'markers-fills',fig

def profile(s,n):
    fig=page(s['id']+'  '+s['name'],s['caption'],n,size=(12.5,9.5),canvas=s['canvas'],ink=s['ink'])
    colors=s['palette']['colors']
    for i,c in enumerate(colors):
        x=.05+i*.152
        fig.add_artist(Rectangle((x,.793),.132,.044,transform=fig.transFigure,facecolor=c,edgecolor='none'))
        write_text(fig,x,.785,c,9,color=s['ink'])
    ax=fig.add_axes([.10,.43,.37,.28]);draw_line(ax,s)
    ax.set_title('Curves and markers',fontsize=BASE.title,color=s['ink'])
    ax=fig.add_axes([.62,.43,.33,.28]);d=r.raw.data_comparison_IEDB
    ax.bar(range(9),d['mean'][:,0],color=assignments(s)['comparison'],width=s['bar_width'],
        yerr=d['std'][:,0],edgecolor=s['ink'] if s['bar_edge'] else 'none',linewidth=s['bar_edge'],
        error_kw=dict(ecolor=s['ink'],elinewidth=s['error'],capsize=s['cap'],capthick=s['error']))
    ax.set(xticks=range(9),xticklabels=range(1,10),ylim=(.5,.9),yticks=[.5,.6,.7,.8,.9],xlabel='Method index (source order)',ylabel='AUROC')
    style_axes(ax,s);ax.set_title('Bars and uncertainty',fontsize=BASE.title,color=s['ink'])
    write_text(fig,.05,.32,'EXACT SETTINGS',10,color=s['ink'])
    lines=[f'Panel {s["panel"]}    Figure {s["canvas"]}    Text {s["ink"]}',
        f'Curves {s["line"]} pt    Frame {s["frame_width"]} pt ({s["frame"]})    Error bars {s["error"]} pt',
        f'Grid {s["grid_width"]} pt / {s["grid"]} / {s["grid_color"]}    Tick length {s["ticks"]} pt',
        f'Markers {s["marker"]} pt / {s["marker_fill"]}    Bar width {s["bar_width"]}    Area opacity {s["area_alpha"]}',
        f'Best use: {s["best"]}',f'Tradeoff: {s["tradeoff"]}']
    for i,line in enumerate(lines):write_text(fig,.05,.284-i*.034,line,10,color=s['ink'])
    write_text(fig,.05,.061,'Bar y range matches the source (0.5-0.9). Indices retain source order; full method names are in the six-example gallery.',8,color=s['muted'])
    return fig

def selection_page(audits):
    fig=page('How I would narrow the field','Choose the overall surface first, then tune weight and structure using the controlled sheets.',14,size=(12.5,9.5))
    choices=[('S2 Warm editorial','My strongest all-round direction: a visible change from the original, with enough line weight for most uses.'),
             ('S3 Mineral grid','The technical direction: cool panels and explicit reference structure. Particularly useful for comparing numerical values.'),
             ('S5 Rose atlas','The more distinctive light direction: rose surfaces and petrol curves, with open axes and hollow markers.'),
             ('S6 / S8 for presentations','Sandstone and Night studio explore the heavier end of the range. Keep a lighter export for small printed figures.')]
    for i,(head,body) in enumerate(choices):
        y=.82-i*.125;write_text(fig,.05,y,head,15);write_text(fig,.05,y-.04,body,11,width=124)
    write_text(fig,.05,.29,'FIXED THROUGHOUT',11)
    write_text(fig,.05,.25,'Helvetica Regular; 10 pt labels; 8.57 pt ticks/legends; 11.43 pt panel titles. Existing smaller dense annotations and DejaVu Sans math are retained. Source values, uncertainty values, method order and axis ranges are unchanged.',10,width=137)
    write_text(fig,.05,.16,'CHECKED, WITH LIMITS',11)
    minimum=min(min(a['core_contrast']) for a in audits.values())
    write_text(fig,.05,.12,f'Core colors have at least {minimum:.2f}:1 opaque contrast against their own panel backgrounds. Redundant shapes/dashes and grayscale/deutan previews help review distinctions. This is not full accessibility certification; broad palettes and translucent fills still need context-specific review.',10,width=137)
    return fig

def audit_style(s):
    colors=s['palette']['colors'];bg=s['panel']
    rgb=np.array([to_rgb(c) for c in colors[:3]])
    a={'core_contrast':[round(contrast(c,bg),3) for c in colors[:3]],
       'extended_contrast':[round(contrast(c,bg),3) for c in colors+s['palette']['extra']],
       'text_on_panel':round(contrast(s['ink'],bg),3),'text_on_canvas':round(contrast(s['ink'],s['canvas']),3),
       'closest_core_distance':{}}
    for mode in ['normal','deutan','protan','tritan','gray']:
        lab=oklab(simulate(rgb,mode))
        a['closest_core_distance'][mode]=round(min(float(np.linalg.norm(lab[i]-lab[j])) for i in range(3) for j in range(i+1,3)),4)
    return a

def docs(audits):
    lines=['# Full plotting-style exploration','',
        '**Eight complete directions; Helvetica typography fixed.** [Open gallery](gallery.html) · [Visual study PDF](style-exploration.pdf) · [Overview](overview.png)','',
        'This expands the earlier palette study to panel and page backgrounds, frame visibility/color/weight, curve and error-bar weights, grids, ticks, markers, bar width/outlines, hatching and fill opacity. The approved default remains in the parent directory.','',
        '## Fixed typography and data','',
        'Helvetica Regular is used throughout: 10 pt axis labels, 8.57 pt ticks/legends and 11.43 pt panel titles. The original dense-annotation sizes and DejaVu Sans math font are preserved. No font-family, weight or size changes were applied to the six examples. Each example retains its physical canvas size, source values, method order, uncertainty values and axis ranges. Bar widths vary around fixed centers; colors and style do not alter the quantities.','',
        'The sphere and original assembled composites remain excluded. All six source examples are available in each style as 300 dpi PNG, native PDF and editable SVG. The overview/profile pages are comparison sheets, not replacement scientific datasets.','',
        '## Complete directions','',
        '| Style | Panel / figure | Curve | Frame | Grid | Marker |','|---|---|---|---|---|---|']
    for s in DIRECTIONS:
        lines.append(f'| [{s["id"]} {s["name"]}]({s["slug"]}/gallery.pdf) | `{s["panel"]}` / `{s["canvas"]}` | {s["line"]} pt | {s["frame"]}, {s["frame_width"]} pt | {s["grid"]}, {s["grid_width"]} pt | {s["marker"]} pt, {s["marker_fill"]} |')
    lines+=['','## Controlled comparisons','',
        '- [Nine backgrounds](backgrounds.png): only the panel color varies; P2 palette, 1.15 pt curves, black frame and typography stay fixed.',
        '- [Six curve weights](line-weights.png): only curve width changes from 0.65 to 2.3 pt. Markers and their outlines stay fixed.',
        '- [Six axes/grid treatments](axes-grids.png): compare boxed, open, bottom-only and frameless treatments.',
        '- [Markers and fills](markers-fills.png): hollow/filled markers crossed with 0%, 12% and 30% area opacity. These overlapping fills are visual proofs, not new uncertainty bands.','',
        '## Choosing a direction','',
        'S2 is my all-round recommendation; S3 provides a technical look; S5 is a more distinctive light treatment. S6 and S8 explore presentation-oriented extremes. It is reasonable to combine, for example, the S5 background with S2 curve weight and S1 open axes. Recheck contrast after mixing tokens.','']
    for s in DIRECTIONS:
        a=audits[s['id']]
        lines += [f'### {s["id"]} {s["name"]}','',s['caption'],'',f'Best use: {s["best"]} Tradeoff: {s["tradeoff"]}','',
            'Core palette (signature, companion 1, companion 2): '+', '.join('`'+c+'`' for c in s['palette']['colors'][:3])+'.','',
            'Extended colors: '+', '.join('`'+c+'`' for c in s['palette']['colors'][3:]+s['palette']['extra'])+'.','',
            f'Text `{s["ink"]}`; secondary text `{s["muted"]}`; frame `{s["frame_color"]}`; grid `{s["grid_color"]}`; neutral `{s["palette"]["neutral"]}`.', '',
            f'Error bars {s["error"]} pt, caps {s["cap"]} pt; bar width {s["bar_width"]}, bar outline {s["bar_edge"]} pt. Distribution alpha {s["fill_alpha"]}; trend fill alphas {s["area_alpha"]}; radar alpha {s["radar_alpha"]}.', '',
            f'Core contrast on its panel: '+', '.join(f'{v:.2f}:1' for v in a['core_contrast'])+'.', '',
            f'[Six examples]({s["slug"]}/gallery.pdf) · [Profile]({s["slug"]}/profile.png)','']
    lines += ['## Encoding details','',
        'DPO, DA-DPO and VIGIL use square, triangle and circle markers. Styles with dashed curves also use dashed, dash-dot and solid lines respectively. Radar keeps solid paths and the three shapes. Open markers use the panel color inside. The gray SFT baseline remains explicitly labeled.', '',
        'S7 uses a single plum highlight for the target bar and gray comparators. Numbered tick positions and matching legend prefixes identify the otherwise similar gray methods. Its composition figure also uses numbered method positions. Other styles retain the original color-based legends.', '',
        'For open/frameless styles, the radar keeps its radial reference geometry but loses its enclosing rectangle. All original benchmark-specific radial mappings remain unchanged. Cartesian grid removal does not remove the radar scale guides.', '',
        'Source bars preserve their truncated y ranges for comparability. The supplied uncertainty values are preserved without reinterpreting them as one uniform type of confidence interval. Concept plots remain conceptual drawings.','',
        '## Readability and export checks','',
        'The renderer checks source data geometry, fixed font sizes/family/weight, original physical canvas dimensions, and preservation of approved exports. Contrast measurements and approximate Machado color-vision simulations are diagnostic aids, not certification. Extended category sets may converge under color-vision deficiencies; light or transparent fills are not guaranteed to clear a contrast threshold. Native PDFs retain editable text; SVG requires Helvetica on the viewing system.', '',
        'The complete settings and category assignments are in [styles.json](styles.json); validation results are in [validation.json](validation.json). Existing [palette research](../palette-study/README.md) informed this exploration. No new claim about historical rarity or brand exclusivity is made.','',
        '## Reproduce','',
        '```sh','python figures4papers-minimal/render_style_exploration.py','```','',
        'The same requirements as the parent project suffice. Definitions are in `../style_directions.py`. Source data and drawings: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), CC BY-NC 4.0; parent provenance and license apply.','']
    (OUT/'README.md').write_text('\n'.join(lines))

def gallery():
    buttons=''.join(f'<button data-i="{i}" aria-pressed="{str(i==1).lower()}">{s["id"]} · {html.escape(s["name"])}</button>' for i,s in enumerate(DIRECTIONS))
    articles=''.join(f'<article><h3>{title}</h3><a class="full" data-file="{name}"><img data-file="{name}" alt="{title}, same source data in the selected visual style"></a><p><a class="pdf" data-file="{name}">PDF</a> · <a class="svg" data-file="{name}">SVG</a></p></article>' for name,title,_ in r.EXAMPLES)
    markup='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Full plotting style exploration</title><style>
*{box-sizing:border-box}body{margin:0;font:16px Helvetica,Arial,sans-serif;color:#282828;background:#F7F5EF;line-height:1.5}main{max-width:1450px;margin:auto;padding:36px}h1,h2,h3{font-weight:400}h1{font-size:38px;line-height:1.15}h2{font-size:26px}a{color:#68445F}nav{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}button,select{font:inherit;color:inherit;background:white;border:1px solid #b6b0a4;padding:8px 11px;border-radius:4px;cursor:pointer}button[aria-pressed=true]{background:#282828;color:white}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #385A7C;outline-offset:3px}.controls{position:sticky;top:0;background:#F7F5EF;z-index:3;padding:1px 0 12px;border-bottom:1px solid}#profile,#overview{width:100%;display:block}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{background:white;border:1px solid #d3cec3;border-radius:5px;padding:16px}article img{width:100%;display:block}article:nth-child(1),article:nth-child(2),article:nth-child(5),article:nth-child(6){grid-column:1/-1}.meta{font-size:13px}#tokens{font-size:14px}.swatches{display:flex;gap:10px;flex-wrap:wrap}.chip{width:125px;height:32px;margin-bottom:5px}summary{cursor:pointer;margin:16px 0}.tests{display:grid;grid-template-columns:1fr 1fr;gap:20px}.tests img{width:100%}footer{border-top:1px solid;margin-top:26px;padding-top:16px}@media(max-width:800px){main{padding:18px}.grid,.tests{display:block}article{margin-bottom:20px}.controls{position:static}h1{font-size:30px}}
</style><main><h1>Everything except the font</h1><p>Eight complete plotting directions, plus four controlled comparisons. Helvetica Regular and the original data stay fixed.</p><p><a href="style-exploration.pdf">Full visual study</a> · <a href="README.md">Exact specifications</a> · <a href="styles.json">Reusable settings</a> · <a href="../gallery.html">Approved baseline</a></p><details><summary>See all eight directions together</summary><img id="overview" src="overview.png" alt="Eight visual directions alongside the approved baseline"></details><div class="controls"><nav>BUTTONS</nav><label for="vision">Viewing mode </label><select id="vision"><option value="normal">Original colors</option><option value="deutan">Deutan simulation</option><option value="gray">Grayscale</option></select> <span id="status" class="meta" aria-live="polite"></span></div><h2 id="name"></h2><p id="caption"></p><div class="swatches" id="swatches"></div><p id="tokens"></p><p id="best"></p><p class="meta" id="tradeoff"></p><p><a id="pdf-gallery">Six-example PDF</a></p><details><summary>Style profile and exact settings</summary><img id="profile" alt="Style profile with curves, bars and specifications"></details><div class="grid">ARTICLES</div><h2>Mix and match: controlled comparisons</h2><p>These sheets separate background, curve weight, axes/grids, and marker/fill decisions. Each can be enlarged.</p><div class="tests">TESTS</div><footer><p>Shortlist: <strong>S2 Warm editorial</strong> for balance, <strong>S3 Mineral grid</strong> for a technical look, and <strong>S5 Rose atlas</strong> for a more distinctive light direction. S6 and S8 explore heavier presentation styles.</p><p class="meta">The six examples preserve source values, uncertainty values, method order and axis ranges. Comparison bars retain truncated axes. Sphere and original assembled composites are excluded. Viewing simulations affect the six plots; profile, swatches and downloadable vectors remain in original colors.</p><p class="meta">Source figures: <a href="https://github.com/ChenLiu-1996/figures4papers">Chen Liu / figures4papers</a>, CC BY-NC 4.0. These are original style proposals informed by the previous research study.</p></footer></main><script>
const styles=DATA;let selected=1;const vision=document.getElementById('vision');function update(){const s=styles[selected],mode=vision.value,base=s.slug+'/',imbase=mode==='normal'?base:'simulations/'+s.id+'/'+mode+'/';document.getElementById('name').textContent=s.id+' · '+s.name;document.getElementById('caption').textContent=s.caption;document.getElementById('tokens').textContent='Panel '+s.panel+' · Figure '+s.canvas+' · Curves '+s.line+' pt · Frame '+s.frame+' / '+s.frame_width+' pt · Markers '+s.marker+' pt / '+s.marker_fill;document.getElementById('best').textContent=s.best;document.getElementById('tradeoff').textContent=s.tradeoff;document.getElementById('swatches').innerHTML=s.palette.colors.map(c=>'<div><div class="chip" style="background:'+c+'"></div><code>'+c+'</code></div>').join('');document.querySelectorAll('button[data-i]').forEach((b,i)=>b.setAttribute('aria-pressed',i===selected));document.querySelectorAll('img[data-file]').forEach(im=>im.src=imbase+im.dataset.file+'.png');document.querySelectorAll('.full').forEach(a=>a.href=imbase+a.dataset.file+'.png');for(const ext of ['pdf','svg'])document.querySelectorAll('.'+ext).forEach(a=>a.href=base+a.dataset.file+'.'+ext);document.getElementById('pdf-gallery').href=base+'gallery.pdf';document.getElementById('profile').src=base+'profile.png';document.getElementById('status').textContent=mode==='normal'?'':'Approximate simulation; not accessibility certification.';}document.querySelectorAll('button[data-i]').forEach(b=>b.addEventListener('click',()=>{selected=+b.dataset.i;update()}));vision.addEventListener('change',update);update();
</script></html>'''
    tests=''.join(f'<div><h3>{label}</h3><a href="{name}.png"><img src="{name}.png" alt="{label}"></a></div>' for name,label in [('backgrounds','Background only'),('line-weights','Curve width only'),('axes-grids','Axes and grids'),('markers-fills','Markers and opacity')])
    (OUT/'gallery.html').write_text(markup.replace('BUTTONS',buttons).replace('ARTICLES',articles).replace('TESTS',tests).replace('DATA',json.dumps(DIRECTIONS)))

def main():
    OUT.mkdir(exist_ok=True);theme.apply_theme()
    protected=[ROOT/'gallery.pdf',ROOT/'gallery-beige.pdf',ROOT/'data.json',ROOT/'render-info.json']
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    fingerprints={};fonts={}
    for name,_,render in r.EXAMPLES:
        f=render();fingerprints[name]=fingerprint(f)
        fonts[name]=[(t.get_fontfamily(),t.get_fontsize(),t.get_fontweight()) for t in f.findobj(Text)]
        plt.close(f)
    audits={s['id']:audit_style(s) for s in DIRECTIONS};definitions=[]
    for s in DIRECTIONS:
        dest=OUT/s['slug'];dest.mkdir(exist_ok=True)
        with use_style(s):
            with PdfPages(dest/'gallery.pdf',metadata={'Title':s['id']+' '+s['name']+' - six examples'}) as pdf:
                for name,title,render in r.EXAMPLES:
                    fig=render()
                    assert [(t.get_fontfamily(),t.get_fontsize(),t.get_fontweight()) for t in fig.findobj(Text)]==fonts[name]
                    finish(fig,s,name)
                    assert fingerprint(fig)==fingerprints[name],(s['id'],name,'data drift')
                    for t in fig.findobj(Text):
                        assert t.get_fontfamily()==[theme.FONT] and t.get_fontweight()=='normal'
                    fig.canvas.draw()
                    for ext in ['png','pdf','svg']:fig.savefig(dest/f'{name}.{ext}',dpi=300,facecolor=s['canvas'])
                    pdf.savefig(fig,facecolor=s['canvas']);plt.close(fig)
            definitions.append({**s,'theme':asdict(theme.T),'assignments':assignments(s),
                'category_mappings':{group:list(zip(names,assignments(s)[group])) for group,names in [
                    ('methods',METHODS),('comparison',list(r.raw.data_comparison_IEDB['methods'])),('composition',list(r.brute.data_brute_force_math['methods']))]}})
        print('Rendered '+s['id']+' '+s['name'],flush=True)
    theme.apply_theme()
    with PdfPages(OUT/'style-exploration.pdf',metadata={'Title':'Everything except the font - complete plotting styles'}) as pdf:
        f=overview();pdf.savefig(f,facecolor=f.get_facecolor());f.savefig(OUT/'overview.png',dpi=170);plt.close(f)
        for name,f in controls():
            pdf.savefig(f,facecolor=f.get_facecolor());f.savefig(OUT/f'{name}.png',dpi=170);plt.close(f)
        for i,s in enumerate(DIRECTIONS):
            with use_style(s):
                f=profile(s,i+6);pdf.savefig(f,facecolor=s['canvas']);f.savefig(OUT/s['slug']/'profile.png',dpi=170,facecolor=s['canvas']);plt.close(f)
        f=selection_page(audits);pdf.savefig(f,facecolor='white');plt.close(f)
    from PIL import Image
    for s in DIRECTIONS:
        for name,_,_ in r.EXAMPLES:
            with Image.open(OUT/s['slug']/f'{name}.png') as im:
                im=im.convert('RGB');im.thumbnail((1600,1250));rgb=np.asarray(im,dtype=float)/255
                for mode in ['deutan','gray']:
                    dest=OUT/'simulations'/s['id']/mode;dest.mkdir(parents=True,exist_ok=True)
                    Image.fromarray(np.uint8(np.round(simulate(rgb,mode)*255))).save(dest/f'{name}.png')
    docs(audits);gallery()
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    (OUT/'styles.json').write_text(json.dumps({'fixed_typography':{'font':theme.FONT,'weight':'normal','axis_labels_pt':BASE.base,'ticks_legends_pt':BASE.small,'panel_titles_pt':BASE.title},'directions':definitions},indent=2)+'\n')
    (OUT/'validation.json').write_text(json.dumps({'original_data_geometry_equal':True,'typography_fixed':True,
        'source_fingerprints':fingerprints,'approved_exports_unchanged':before,'styles':audits,'original_examples':6,'candidate_styles':8},indent=2)+'\n')
    print('Saved 48 figures, 8 galleries, 4 controlled comparisons and 14-page study.',flush=True)

if __name__=='__main__':main()
