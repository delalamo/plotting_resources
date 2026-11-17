"""Blue focus / neutral-gray context examples using the selected R1/S3 style.

One dataset is the original post-training benchmark. Three are explicitly
synthetic illustrations. Outputs are separate from the selected R1 exports.
"""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/figures4papers-mpl')
from pathlib import Path
import json, hashlib, html
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.colors import to_rgb
from render_style_exploration import use_style, style_axes, write_text
import render_examples as source
import minimal_theme as theme
from palette_color_math import contrast

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'emphasis-examples'
SELECTED=json.loads((ROOT/'selected-style.json').read_text())
STYLE=SELECTED['style']
BLUE=STYLE['palette']['colors'][0]
BG=STYLE['panel']
FONT=SELECTED['typography']['font']
SMALL=SELECTED['typography']['ticks_legends_pt']
DASHES=[(0,(4,2)),(0,(3,1.5,1,1.5)),(0,(1,2)),(0,(6,2)),(0,(3,2,1,2))]

def gray_colors(n):
    """Opaque neutral grays, darkest to lightest; no blue tint or alpha wash."""
    return ['#'+f'{int(v):02X}'*3 for v in np.rint(np.linspace(119,183,n))]

def line(name,y,**kwargs):
    return dict(name=name,y=np.asarray(y,dtype=float).tolist(),**kwargs)

def datasets():
    d=source.post.data_posttraining
    original=dict(id='H1',slug='original-benchmark',title='Original benchmark',
        subtitle='One cobalt method against three gray baselines',
        origin='Original figures4papers post-training data; values unchanged.',synthetic=False,
        x=np.asarray(d['steps']).tolist(),xlabel='Post-training steps',ylabel='Performance',
        xlim=[-25,825],ylim=[0,63],xticks=np.asarray(d['steps']).tolist(),yticks=[0,20,40,60],
        focus=line('VIGIL (Ours)',d['results'][2],short='VIGIL'),
        references=[line('DPO',d['results'][0],marker='s'),line('DA-DPO',d['results'][1],marker='^'),
                    line('SFT only',np.full(len(d['steps']),d['results'][0,0]),marker=None)],
        markers=True,markevery=1,xscale='linear')

    x=np.arange(0,101,5)
    refs=[]
    for i,(start,limit,tau) in enumerate(zip([48,52,50,54,47],[74,79,83,87,90],[15,24,30,32,38])):
        y=start+(limit-start)*(1-np.exp(-x/tau))+.35*np.sin(x/12+i)
        refs.append(line(f'Baseline {i+1}',y))
    learning=dict(id='H2',slug='learning-curves',title='Learning curves',
        subtitle='One focus among five baselines; it need not be the best',
        origin='Synthetic illustration, generated deterministically; not experimental results.',synthetic=True,
        x=x.tolist(),xlabel='Training epoch',ylabel='Illustrative score',xlim=[-2,103],ylim=[45,92],
        xticks=[0,25,50,75,100],yticks=[50,60,70,80,90],
        focus=line('Selected method',50+31*(1-np.exp(-x/19))+.25*np.sin(x/11),short='Focus'),
        references=refs,markers=False,markevery=4,xscale='linear')

    rng=np.random.default_rng(418)
    x=np.arange(24)
    refs=[]
    for i in range(8):
        y=80+3*i+.65*x+4*np.sin(x/3+i*.55)+rng.normal(0,.8,len(x))
        refs.append(line(f'Reference {chr(65+i)}',y))
    trajectories=dict(id='H3',slug='reference-trajectories',title='A trajectory in context',
        subtitle='One cobalt trajectory against eight gray references',
        origin='Synthetic illustration, random seed 418; not observed time-series data.',synthetic=True,
        x=x.tolist(),xlabel='Month',ylabel='Illustrative index',xlim=[-.4,23.6],ylim=[74,124],
        xticks=[0,6,12,18,23],yticks=[80,90,100,110,120],
        focus=line('Selected trajectory',91+.6*x+6*np.sin(x/3.2+.6)+rng.normal(0,.8,len(x)),short='Focus'),
        references=refs,markers=False,markevery=4,xscale='linear')

    x=np.logspace(-3,1,9);lx=np.log10(x)
    refs=[]
    for i,(floor,amp,center,width) in enumerate([(64,14,-1.9,.7),(65,16,-.4,.9),(63,18,-1.4,1.4),(67,11,.05,.7)]):
        refs.append(line(f'Comparison {i+1}',floor+amp*np.exp(-((lx-center)**2)/width),marker=['s','^','D','v'][i]))
    response=dict(id='H4',slug='parameter-response',title='Crossing response curves',
        subtitle='One cobalt method across four gray comparisons',
        origin='Synthetic illustration; curves show a style example, not measured sensitivity.',synthetic=True,
        x=x.tolist(),xlabel='Parameter value (log scale)',ylabel='Illustrative score',xlim=[.0008,13],ylim=[60,87],
        xticks=[.001,.01,.1,1,10],yticks=[60,65,70,75,80,85],
        focus=line('Selected method',66+17*np.exp(-((lx+1.1)**2)/.95),short='Focus'),
        references=refs,markers=True,markevery=1,xscale='log')
    return [original,learning,trajectories,response]

def draw(ax,d,overview=False):
    refs=d['references'];colors=gray_colors(len(refs))
    lines=[]
    # Background first; the selected series is drawn last and above intersections.
    for i,(item,c) in enumerate(zip(refs,colors)):
        marker=item.get('marker','o') if d['markers'] else None
        ln,=ax.plot(d['x'],item['y'],label=item['name'],color=c,lw=STYLE['line'],
            ls=DASHES[i%len(DASHES)],marker=marker,markevery=d['markevery'],
            ms=STYLE['marker'],mfc=BG,mec=c,mew=.625,alpha=1,zorder=2)
        lines.append(ln)
    focus,=ax.plot(d['x'],d['focus']['y'],label=d['focus']['name'],color=BLUE,lw=STYLE['line'],
        ls='-',marker='o' if d['markers'] else None,markevery=d['markevery'],
        ms=STYLE['marker'],mfc=BG,mec=BLUE,mew=.625,alpha=1,zorder=4)
    ax.set(xscale=d['xscale'],xlim=d['xlim'],ylim=d['ylim'],xticks=d['xticks'],yticks=d['yticks'],
           xlabel=d['xlabel'],ylabel=d['ylabel'])
    if d['xscale']=='log':
        ax.set_xticklabels(['0.001','0.01','0.1','1','10'])
        ax.minorticks_off()
    style_axes(ax,STYLE)
    if overview:
        ax.annotate(d['focus']['short'],xy=(1.02,d['focus']['y'][-1]),xycoords=('axes fraction','data'),
                    ha='left',va='center',fontsize=SMALL,color=BLUE,annotation_clip=False)
    else:
        handles=[focus]+lines
        ncols=2 if len(handles)<=4 else 3 if len(handles)<=6 else 5
        legend=ax.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,-.17),ncols=ncols,
                         fontsize=SMALL,handlelength=2.2,columnspacing=1.4,labelspacing=.6)
        legend.get_texts()[0].set_color(BLUE)
        for text in legend.get_texts()[1:]:text.set_color('#666666')
    # Focus is a choice of attention, never an encoded claim of superiority.
    for ln,item in zip(lines,refs):assert np.array_equal(ln.get_ydata(),item['y'])
    assert np.array_equal(focus.get_ydata(),d['focus']['y'])
    assert all(ln.get_linewidth()==1.25 for ln in lines+[focus])
    assert all(len(set(to_rgb(ln.get_color())))==1 for ln in lines)
    return focus,lines

def standalone(d):
    f=plt.figure(figsize=(7.4,5.2),facecolor='white')
    write_text(f,.11,.965,d['id']+'  '+d['title'],STYLE['theme']['title'])
    write_text(f,.11,.919,d['subtitle'],SMALL,color=STYLE['muted'])
    ax=f.add_axes([.11,.255,.835,.59]);draw(ax,d)
    label='Original benchmark data' if not d['synthetic'] else 'Synthetic illustration'
    write_text(f,.11,.04,label+'  |  R1 cobalt + neutral grays  |  S3 background',7.7,color=STYLE['muted'])
    return f

def overview(data):
    f=plt.figure(figsize=(15,11.3),facecolor='white')
    write_text(f,.045,.965,'One blue series, gray comparison lines',22)
    write_text(f,.045,.921,'Selected R1 cobalt #285F96 on S3 #EBF1F5. Helvetica, 1.25 pt curves, dotted grids and thin frames are retained.',10)
    f.add_artist(Line2D([.045,.955],[.886,.886],transform=f.transFigure,lw=.45,color=STYLE['frame_color']))
    for i,d in enumerate(data):
        x=.07+(i%2)*.49;top=.85-(i//2)*.39
        write_text(f,x,top,d['id']+'  '+d['title'],STYLE['theme']['title'])
        note=('Original benchmark' if not d['synthetic'] else 'Synthetic example')+f"  /  {len(d['references'])} gray comparison lines"
        write_text(f,x,top-.035,note,SMALL,color=STYLE['muted'])
        ax=f.add_axes([x,top-.30,.35,.225]);draw(ax,d,overview=True)
    write_text(f,.045,.108,'All curves use 1.25 pt. Emphasis comes from cobalt, a solid line and drawing the selected series above the gray context.',9)
    for i,c in enumerate(gray_colors(5)):
        x=.045+i*.10
        f.add_artist(Line2D([x,x+.075],[.071,.071],transform=f.transFigure,color=c,lw=2))
        write_text(f,x,.061,c,8)
    f.add_artist(Line2D([.595,.675],[.071,.071],transform=f.transFigure,color=BLUE,lw=2))
    write_text(f,.695,.077,'Emphasized series  '+BLUE,9,color=BLUE)
    write_text(f,.045,.024,'H1 uses the original repository data. H2-H4 are illustrative datasets. Full-size examples include individual baseline legends.',8,color=STYLE['muted'])
    return f

def spec_page(data):
    f=plt.figure(figsize=(11.7,8.3),facecolor='white')
    write_text(f,.06,.93,'An optional emphasis treatment for R1 / S3',20)
    rows=[
        ('Emphasized series',BLUE+' cobalt; solid, 1.25 pt; draw last at z-order 4.'),
        ('Background entries','Opaque neutral grays from #777777 to #B7B7B7; 1.25 pt; dashed, z-order 2.'),
        ('Three background entries',', '.join(gray_colors(3))),
        ('Five background entries',', '.join(gray_colors(5))),
        ('Eight background entries',', '.join(gray_colors(8))),
        ('Surface and frame',BG+' panel; white margin; #566C7B frame at 0.45 pt on all four sides.'),
        ('Grid','#CBD6DF, 0.45 pt, dotted major x/y grid.'),
        ('Typography','Helvetica Regular: 10 pt axes; 8.57 pt ticks/legends; 11.43 pt plot titles.'),
        ('Markers','Where used: 3.5 pt, open, panel-colored centers; baseline shapes remain distinct.'),
    ]
    for i,(label,value) in enumerate(rows):
        y=.83-i*.065;write_text(f,.06,y,label,10);write_text(f,.31,y,value,9.5)
    write_text(f,.06,.20,'Use the lighter grays when individual background entries are secondary. Use fewer, darker gray shades and explicit labels when each baseline needs close comparison. Color and dash patterns do not uniquely identify arbitrarily many series.',10,width=127)
    write_text(f,.06,.10,'Data provenance: H1 is the source post-training benchmark. H2-H4 are deterministic synthetic illustrations; the highlighted line is not consistently the top performer.',9,width=137,color=STYLE['muted'])
    return f

def gallery(data):
    cards=[]
    for d in data:
        slug=d['slug'];title=html.escape(d['id']+' '+d['title'])
        cards.append(f'<section><h2>{title}</h2><p>{html.escape(d["origin"])}</p><a href="{slug}.png"><img src="{slug}.png" alt="{title}: one cobalt series and gray comparisons"></a><p><a href="{slug}.png">PNG</a> · <a href="{slug}.svg">SVG</a> · <a href="{slug}.pdf">PDF</a></p></section>')
    (OUT/'gallery.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blue focus, gray context</title><style>
body{margin:0;color:#282828;background:#fff;font:16px/1.5 Helvetica,Arial,sans-serif}main{max-width:1250px;margin:auto;padding:36px 28px}h1,h2{font-weight:400}h1{font-size:34px}h2{font-size:22px}a{color:#285F96}img{display:block;width:100%;height:auto}section{margin:32px 0;border-top:1px solid #CBD6DF;padding-top:12px}p{max-width:1000px}nav{display:flex;flex-wrap:wrap;gap:20px}.examples{display:grid;grid-template-columns:1fr 1fr;gap:30px}section p{font-size:14px;color:#666}@media(max-width:900px){.examples{grid-template-columns:1fr}main{padding:20px 14px}}</style><main>
<h1>One blue series, gray comparison lines</h1><p>Four samples in the selected R1/S3 style: cobalt <b>#285F96</b>, neutral gray comparisons, pale blue-gray <b>#EBF1F5</b> panels and Helvetica Regular. All curves keep the selected 1.25 pt line width.</p><nav><a href="blue-focus-gray-context.pdf">Full PDF</a><a href="README.md">Settings and source</a><a href="data.json">Example data</a></nav><a href="overview.png"><img src="overview.png" alt="Four examples of a cobalt focus line against muted gray references"></a><div class="examples">'''+''.join(cards)+'''</div><p>H1 derives from <a href="https://github.com/ChenLiu-1996/figures4papers">Chen Liu / figures4papers</a>, CC BY-NC 4.0. H2-H4 are synthetic demonstrations. This emphasis treatment supplements the selected R1 palette.</p></main></html>''')

def main():
    OUT.mkdir(exist_ok=True)
    protected=[ROOT/'selected-style.json']+list((ROOT/'s3-design-study'/'cobalt-brick-gold').glob('*'))
    before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
    data=datasets();checks=[]
    with use_style(STYLE):
        with PdfPages(OUT/'blue-focus-gray-context.pdf',metadata={'Title':'R1/S3: one blue series, gray comparison lines'}) as pdf:
            f=overview(data);pdf.savefig(f);f.savefig(OUT/'overview.png',dpi=180);plt.close(f)
            for d in data:
                f=standalone(d);f.canvas.draw()
                renderer=f.canvas.get_renderer()
                assert f.axes[0].get_legend().get_window_extent(renderer).y0 > f.texts[-1].get_window_extent(renderer).y1+6
                for t in f.findobj(Text):assert t.get_fontfamily()==[FONT] and t.get_fontweight()=='normal'
                for ext in ['png','pdf','svg']:f.savefig(OUT/f'{d["slug"]}.{ext}',dpi=300)
                pdf.savefig(f);plt.close(f)
                checks.append(dict(id=d['id'],synthetic=d['synthetic'],references=len(d['references']),
                    gray_colors=gray_colors(len(d['references'])),all_line_widths_pt=1.25,
                    plotted_values_equal_input=True))
            f=spec_page(data);pdf.savefig(f);plt.close(f)
    gallery(data)
    (OUT/'data.json').write_text(json.dumps(data,indent=2)+'\n')
    (OUT/'settings.json').write_text(json.dumps(dict(base_style='R1 / S3',focus_color=BLUE,background=BG,
        font=FONT,line_width_pt=1.25,gray_range=['#777777','#B7B7B7'],
        gray_palettes={str(n):gray_colors(n) for n in [3,4,5,8]},focus_zorder=4,context_zorder=2,
        alpha=1,source='selected-style.json',samples=checks),indent=2)+'\n')
    (OUT/'README.md').write_text('''# Cobalt focus with gray context

An optional emphasis treatment for the selected R1/S3 style. [View all samples](gallery.html) · [Six-page PDF](blue-focus-gray-context.pdf) · [Overview](overview.png).

The emphasized entry is **#285F96**, the selected R1 cobalt. Background entries use opaque, neutral gray shades from **#777777** to **#B7B7B7**. Both retain **1.25 pt** strokes: the visual hierarchy comes from hue, a solid focus line, dashed comparison lines, and drawing the focus last. No extra line-weight change is needed.

The panel remains **#EBF1F5** with white margins, **Helvetica Regular**, a **0.45 pt #566C7B** four-sided frame and a **0.45 pt dotted #CBD6DF** grid. Used markers remain 3.5 pt and hollow. All type sizes stay as specified in the [selected guide](../README.md).

| Sample | Data | Purpose |
|---|---|---|
| H1 Original benchmark | Original post-training source values | A cobalt method against three gray baselines |
| H2 Learning curves | Synthetic, deterministic | One focus among five baselines; the focus is not the best performer |
| H3 A trajectory in context | Synthetic, seed 418 | One highlighted trajectory among eight references |
| H4 Crossing response curves | Synthetic, deterministic | Four gray comparisons on a log-scaled x axis |

Three-reference gray set: `#777777`, `#979797`, `#B7B7B7`.

Five-reference gray set: `#777777`, `#878787`, `#979797`, `#A7A7A7`, `#B7B7B7`.

The lightest shades deliberately recede. For close reading of every reference, use fewer, darker grays and explicit labels. Gray shades and dash styles do not uniquely identify arbitrarily many entries. The full-size examples include individual legends; the overview directly labels the blue line.

Exact sample arrays are in [data.json](data.json), and settings are in [settings.json](settings.json). Exports include 300 dpi PNG, embedded-font PDF and editable-text SVG.

```sh
MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_emphasis_examples.py
```

H1 data: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), [CC BY-NC 4.0](../upstream/LICENSE). H2-H4 are illustrative data, not new scientific measurements. The selected R1 exports are unchanged.
''')
    assert before=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in before}
    (OUT/'validation.json').write_text(json.dumps(dict(selected_exports_unchanged=before,
        typeface=FONT,focus_contrast=contrast(BLUE,BG),gray_contrasts={c:contrast(c,BG) for c in gray_colors(8)},
        samples=checks),indent=2)+'\n')
    print('Saved four line-plot samples, a four-panel overview, and a six-page PDF.',flush=True)

if __name__=='__main__':main()
