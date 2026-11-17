"""Five researched cool palettes; all non-palette S3 settings stay fixed.

Run with the same environment as render_examples.py. Writes s3-cool-study/.
"""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/figures4papers-mpl')
from pathlib import Path
from dataclasses import asdict
import json, hashlib, html, re
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.colors import to_rgb
from PIL import Image
import minimal_theme as theme
import render_examples as r
from s3_cool_palettes import S3, COOL, SOURCES, FIXED, COLOR_FIELDS
from render_style_exploration import (
    use_style, finish, fingerprint, assignments, draw_line, write_text,
    style_axes, audit_style, BASE, METHODS,
)
from palette_color_math import simulate, oklab

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'s3-cool-study'
ALL = [S3]+COOL
TAGS = ['Blue + clay + moss (reference)', 'Navy + glacier teal + dusty steel',
        'Indigo + sea glass + dusty iris', 'Lagoon + jade + glazed blue',
        'Indigo + periwinkle + ash violet', 'Clear blue + cyan + mineral violet']

def page(title, subtitle, n, size=(14.5,10.2)):
    fig=plt.figure(figsize=size, facecolor='white')
    write_text(fig,.045,.962,title,22)
    write_text(fig,.045,.912,subtitle,10)
    fig.add_artist(Line2D([.045,.955],[.88,.88],transform=fig.transFigure,color='#566C7B',lw=.45))
    write_text(fig,.045,.034,'S3 COOL PALETTES  /  #EBF1F5 panels  /  Helvetica Regular  /  Original source data',8,color='#666666')
    fig.text(.955,.034,str(n),ha='right',va='top',fontsize=8,color='#666666')
    return fig

def bars(ax,s):
    d=r.raw.data_comparison_IEDB
    ax.bar(range(9),d['mean'][:,0],color=assignments(s)['comparison'],width=s['bar_width'],
           yerr=d['std'][:,0],edgecolor=s['ink'],linewidth=s['bar_edge'],
           error_kw=dict(ecolor=s['ink'],elinewidth=s['error'],capsize=s['cap'],capthick=s['error']))
    ax.set(xticks=range(9),xticklabels=range(1,10),ylim=(.5,.9),yticks=[.5,.6,.7,.8,.9],
           xlabel='Method index (source order)',ylabel='AUROC')
    style_axes(ax,s)

def comparison(kind='lines'):
    f=page('S3, with five cooler palettes' if kind=='lines' else 'The same palettes with nine categories',
           'Only data colors change. The light blue panel, Helvetica, 1.25 pt curves, grids and borders stay identical.'
           if kind=='lines' else 'The original AUROC values and uncertainty, with unchanged bar positions and range (0.5-0.9).',
           1 if kind=='lines' else 2)
    for i,s in enumerate(ALL):
        x=.045+(i%3)*.313;top=.846-(i//3)*.392
        write_text(f,x,top,('S3  Original palette' if i==0 else s['id']+'  '+s['name']),14)
        write_text(f,x,top-.035,TAGS[i],8.6,color='#566C7B')
        cs=s['palette']['colors'][:3]
        for j,c in enumerate(cs):
            sx=x+j*.091
            f.add_artist(Rectangle((sx,top-.084),.075,.019,transform=f.transFigure,facecolor=c,edgecolor='none'))
            write_text(f,sx,top-.089,c,7.3)
        with use_style(s):
            ax=f.add_axes([x+.030,top-.312,.246,.187])
            draw_line(ax,s) if kind=='lines' else bars(ax,s)
    write_text(f,.045,.077,'Core swatches: signature / first companion / second companion. In curves: VIGIL / DPO / DA-DPO.',8.4,color='#666666')
    return f

def research():
    f=page('Where the cool-color relationships come from',
           'Primary sources informed the hue relationships. Every proposed hex palette is newly composed for the S3 background.',3)
    for i,source in enumerate(SOURCES):
        y=.838-i*.157
        t=write_text(f,.045,y,source['id']+'  '+source['title'],13);t.set_url(source['url'])
        write_text(f,.045,y-.034,source['observation'],10,width=145)
        write_text(f,.045,y-.063,source['tones'],9.5,color='#566C7B')
        write_text(f,.045,y-.090,source['adaptation'],10,width=145)
    write_text(f,.045,.185,'HOW I WOULD CHOOSE',11)
    write_text(f,.045,.148,'Start with C2 Glacial iris for balance. C1 is the quietest; C3 is the most marine; C4 leans violet; C5 has the strongest chroma.',10,width=145)
    write_text(f,.045,.099,'Source headings are clickable. Full URLs, exact category mappings and reproduction commands are in the companion README.',8.5,color='#666666')
    return f

def profile(s,n):
    f=page(s['id']+'  '+s['name'],s['caption'],n)
    for i,c in enumerate(s['palette']['colors']):
        x=.045+i*.153
        f.add_artist(Rectangle((x,.795),.129,.040,transform=f.transFigure,facecolor=c,edgecolor='none'))
        write_text(f,x,.787,s['palette']['names'][i],9.1)
        write_text(f,x,.766,c+('  / core' if i<3 else ''),8.6,color='#566C7B')
    ax=f.add_axes([.088,.417,.361,.277]);draw_line(ax,s)
    ax.set_title('Original post-training curves',fontsize=BASE.title)
    ax=f.add_axes([.584,.417,.361,.277]);bars(ax,s)
    ax.set_title('Original AUROC comparison',fontsize=BASE.title)
    write_text(f,.045,.310,'WHY THIS COMBINATION',11)
    write_text(f,.045,.273,s['best'],11)
    write_text(f,.045,.237,'Tradeoff: '+s['tradeoff'],10)
    refs=[v for v in SOURCES if v['id'] in s['palette']['sources']]
    write_text(f,.045,.200,'Related references: '+', '.join(v['id'] for v in refs)+' (page 3). All swatches are original choices.',9.5,color='#566C7B')
    write_text(f,.045,.155,'FIXED S3 SETTINGS',10)
    write_text(f,.045,.123,'Panel #EBF1F5  |  White margins  |  Helvetica Regular  |  Curves 1.25 pt  |  Error bars 0.65 pt  |  Open markers 3.5 pt',9.5)
    write_text(f,.045,.094,'Four-sided frame #566C7B at 0.45 pt  |  Dotted grid #CBD6DF at 0.45 pt  |  All source values and axis ranges retained',9.5)
    return f

def review(audits):
    f=page('Color separation at a glance','The three core colors, shown in the same order under each preview. Background and swatches are transformed together.',9)
    headings=[('normal','Original'),('deutan','Deutan simulation'),('protan','Protan simulation'),('tritan','Tritan simulation'),('gray','Grayscale')]
    for j,(_,head) in enumerate(headings):write_text(f,.25+j*.142,.835,head,9.1)
    for i,s in enumerate(COOL):
        y=.765-i*.105
        write_text(f,.045,y+.02,s['id']+'  '+s['name'],12)
        a=audits[s['id']]
        write_text(f,.045,y-.017,f"Core contrast: {min(a['core_contrast']):.2f}-"+f"{max(a['core_contrast']):.2f}:1",9,color='#566C7B')
        for j,(mode,_) in enumerate(headings):
            x=.25+j*.142
            bg=simulate(np.array(to_rgb(s['panel'])),mode)
            f.add_artist(Rectangle((x-.009,y-.036),.130,.071,transform=f.transFigure,facecolor=bg,edgecolor='none'))
            colors=simulate(np.array([to_rgb(c) for c in s['palette']['colors'][:3]]),mode)
            for k,c in enumerate(colors):f.add_artist(Rectangle((x+k*.037,y-.017),.030,.035,transform=f.transFigure,facecolor=c,edgecolor='none'))
    write_text(f,.045,.212,'READING THE CHECKS',11)
    minimum=min(min(a['extended_contrast']) for a in audits.values())
    write_text(f,.045,.176,f'All nine opaque category colors in every proposal exceed 3:1 against #EBF1F5 (minimum {minimum:.2f}:1). This screen does not measure contrast between categories, thin antialiased edges, or translucent fills.',10,width=143)
    write_text(f,.045,.116,'Marker shapes, dash patterns and labels remain essential. Nine cool categories are harder to separate than three; keep the original category order and legends. Simulations are approximate, not accessibility certification.',10,width=143)
    return f

def expanded_audit(s):
    a=audit_style(s)
    cs=s['palette']['colors']+s['palette']['extra']
    a['expanded_close_pairs']={}
    for mode in ['normal','deutan','protan','tritan','gray']:
        lab=oklab(simulate(np.array([to_rgb(c) for c in cs]),mode))
        a['expanded_close_pairs'][mode]=[
            {'colors':[cs[i],cs[j]],'oklab_distance':round(float(np.linalg.norm(lab[i]-lab[j])),4)}
            for i in range(9) for j in range(i+1,9) if np.linalg.norm(lab[i]-lab[j])<.06]
    a['close_pair_rule']='Distance <0.06 is an editorial review flag, not an accessibility standard.'
    return a

def docs(audits):
    lines=['# S3: five cooler palettes','',
        'S3 is the selected direction for this comparison. These five **palette candidates** keep its entire non-color treatment fixed; no new palette is selected yet. The earlier B exports and S3 reference are preserved.',
        '', '[Compare the figures](gallery.html) · [Nine-page comparison](s3-cool-palettes.pdf) · [Line overview](overview.png) · [Nine-category comparison](bars-overview.png)',
        '', '## What stays fixed','',
        '- Panel **#EBF1F5**, white figure margins **#FFFFFF**.',
        '- **Helvetica Regular**: 10 pt axis labels, 8.57 pt ticks/legends, 11.43 pt panel titles; existing dense annotation sizes and DejaVu Sans math retained.',
        '- Curves **1.25 pt**; errors **0.65 pt** with 2 pt caps; hollow markers **3.5 pt**.',
        '- Four-sided **#566C7B** frame at **0.45 pt**; dotted xy grid **#CBD6DF** at **0.45 pt**; 2 pt ticks.',
        '- Bar width 0.70; bar outline 0.35 pt. Concept fill 0.08; trend fill 0.14 / 0.22; radar fill 0.035. Original shapes, dashes, positions, ranges, values and uncertainty remain fixed.',
        '- Text #282828, secondary text #666666, hatches #707070. Only the data palette, including the diagram prior color, varies.',
        '', '## Research and interpretation','',
        'Sources accessed 2026-11-15. These references establish design precedents for hue relationships, not evidence that any palette is unused in science. The palette recommendations and their adaptation to S3 are design judgments. No full source palette is copied; paint names are not represented as calibrated sRGB conversions.','']
    for q in SOURCES:
        lines += [f"### {q['id']}. [{q['title']}]({q['url']})",'',q['observation']+' '+q['tones'],'',q['adaptation'],'']
    lines += ['## The five proposals','',
        'I would start with **C2 Glacial iris**: indigo, deep sea glass and dusty iris give a coherent cool identity with broader hue separation than related blues alone. C1 is quieter, C3 more marine, C4 more violet, and C5 more vivid.','',
        'The first three swatches are the core: signature / companion 1 / companion 2. In the line and radar examples these map to VIGIL / DPO / DA-DPO.','',
        '| Option | Signature | Companion 1 | Companion 2 | Full six-example gallery |',
        '|---|---|---|---|---|']
    for s in COOL:
        c=s['palette']['colors'];lines.append(f"| {s['id']} {s['name']} | {c[0]} | {c[1]} | {c[2]} | [PDF]({s['slug']}/gallery.pdf) |")
    for s in COOL:
        p=s['palette'];a=audits[s['id']]
        lines += ['',f"### {s['id']} {s['name']}",'',s['caption'],'',s['best']+' '+s['tradeoff'],'',
            '| Role | Name | Hex |','|---|---|---|']
        for i,(name,c) in enumerate(zip(p['names'],p['colors'])):
            lines.append(f"| {['Signature','Companion 1','Companion 2','Extended 4','Extended 5','Extended 6'][i]} | {name} | `{c}` |")
        for i,c in enumerate(p['extra']):lines.append(f'| Extended {i+7} | Supporting category | `{c}` |')
        lines.append(f"| Diagram prior | Cool neutral | `{p['neutral']}` |")
        lines += ['',f"Opaque core contrast against S3: {', '.join(str(x)+':1' for x in a['core_contrast'])}.",'']
        for group,names in [('methods',METHODS),('comparison',list(r.raw.data_comparison_IEDB['methods'])),('composition',list(r.brute.data_brute_force_math['methods']))]:
            lines += [f'**{group} mapping, in original source order**','',
                      '; '.join(f'{n}: `{c}`' for n,c in zip(names,assignments(s)[group]))+'.','']
    lines += ['## Reading and reuse','',
        'The three-color core is the preferred identity. The additional six colors support the existing dense examples; an analogous nine-color palette is not universally distinguishable. Keep labels, spatial positions, marker shapes and dashes. Do not treat these categorical lists as quantitative sequential scales.',
        '', 'All nine opaque category colors exceed 3:1 against the fixed panel. This does not certify small antialiased marks, category-to-category distinction, text, or translucent fills. `validation.json` contains contrast values and normal/protan/deutan/tritan/grayscale distance checks. Close pairs in broad palettes are recorded rather than hidden. Full-figure grayscale and deutan previews are in `simulations/`.',
        '', '## Reproduce','',
        '```sh','MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_s3_cool_study.py','```','',
        'Definitions: [s3_cool_palettes.py](../s3_cool_palettes.py). Renderer: [render_s3_cool_study.py](../render_s3_cool_study.py). Exact fixed tokens, category mappings and expanded palettes: [palettes.json](palettes.json).',
        '', 'Thirty individual figures are exported as 300 dpi PNG, embedded-font PDF and editable-text SVG, plus five six-page galleries. The nine-page comparison uses compact proof charts from the same source data; the individual exports preserve the full original geometry. No sphere or manually assembled composites are included.',
        '', 'Figures and data derive from [Chen Liu, figures4papers](https://github.com/ChenLiu-1996/figures4papers), commit `0ddfbd3fc9892e804a3fa01ae46bd0d32617f2aa`, under [CC BY-NC 4.0](../upstream/LICENSE). Original labels and potentially truncated axes are retained for like-for-like comparison. The conceptual examples are illustrative, not new experimental observations.','']
    (OUT/'README.md').write_text('\n'.join(lines))

def gallery():
    candidates=[dict(id=s['id'],name=s['name'],slug=s['slug'],caption=s['caption'],colors=s['palette']['colors'][:3]) for s in COOL]
    examples=[dict(name=n,title=t) for n,t,_ in r.EXAMPLES]
    opts=''.join(f'<option value="{i}"'+(' selected' if i==1 else '')+f'>{s["id"]} {html.escape(s["name"])}</option>' for i,s in enumerate(COOL))
    plots=''.join(f'<option value="{html.escape(e["name"])}"'+(' selected' if e['name']=='comparison_posttraining' else '')+f'>{html.escape(e["title"])}</option>' for e in examples)
    template='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>S3: five cooler palettes</title><style>
*{box-sizing:border-box}body{margin:0;background:#fff;color:#282828;font:16px Helvetica,Arial,sans-serif}main{max-width:1560px;margin:auto;padding:36px 32px 60px}h1,h2{font-weight:400}h1{font-size:34px;margin:0 0 12px}h2{font-size:22px}p{line-height:1.5;max-width:1000px}a{color:#274E70}nav{display:flex;gap:20px;flex-wrap:wrap;margin:24px 0}.controls{display:flex;gap:24px;flex-wrap:wrap;padding:20px;background:#EBF1F5;border:1px solid #CBD6DF}label{display:grid;gap:8px}select{font:inherit;padding:9px 12px;max-width:100%;background:white;border:1px solid #566C7B}section{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:24px}article{min-width:0}img{width:100%;height:auto;display:block;border:1px solid #D8E1E8}#swatches{display:flex;gap:15px;flex-wrap:wrap;margin:18px 0}#swatches span{display:flex;align-items:center;gap:7px;font-size:14px}i{display:inline-block;width:28px;height:20px}.note{color:#566C7B;font-size:14px}.overview{max-width:1320px;margin-top:36px}footer{border-top:1px solid #CBD6DF;margin-top:40px;padding-top:16px;font-size:13px;color:#566C7B}@media(max-width:900px){section{grid-template-columns:1fr}main{padding:24px 16px}h1{font-size:28px}}
</style><main><h1>S3, with five cooler palettes</h1>
<p>The same light blue <b>#EBF1F5</b> panel, Helvetica Regular, fine dotted grids and thin borders. Only the data colors change. C2 is my suggested starting point.</p>
<nav><a href="s3-cool-palettes.pdf">Comparison PDF</a><a href="README.md">Research and exact colors</a><a href="palettes.json">Palette definitions</a><a href="bars-overview.png">Nine-category overview</a></nav>
<div class="controls"><label>Palette<select id="palette">__OPTIONS__</select></label><label>Example<select id="plot">__PLOTS__</select></label></div>
<p id="caption" aria-live="polite"></p><div id="swatches" aria-label="Three core colors"></div>
<section><article><h2>S3 original palette</h2><img id="old" alt="Original S3 figure"><p class="note">Blue, clay and moss reference.</p></article><article><h2 id="heading"></h2><img id="new" alt="Cool palette figure"><p><a id="png">PNG</a> · <a id="svg">SVG</a> · <a id="pdf">PDF</a> · <a id="all">All six examples (PDF)</a></p><p><a id="gray">Grayscale preview</a> · <a id="deutan">Deutan preview</a></p></article></section>
<h2>All five directions, plus the original reference</h2><a href="overview.png"><img class="overview" src="overview.png" alt="Six-panel palette comparison on the same pale blue background"></a>
<p class="note">Three core colors carry the identity. Additional colors support the dense source figures; retain labels and shapes. Simulations are approximate and are not accessibility certification.</p>
<noscript><p>Enable JavaScript for the selector, or use the PDF and README links above.</p></noscript>
<footer>Source figures: <a href="https://github.com/ChenLiu-1996/figures4papers">Chen Liu / figures4papers</a>, CC BY-NC 4.0. The sphere and assembled composites are excluded. This study preserves the existing B and S3 exports.</footer>
<script>const styles=__STYLES__;const examples=__EXAMPLES__;
const el=id=>document.getElementById(id);
function update(){const s=styles[Number(el('palette').value)],p=el('plot').value,e=examples.find(x=>x.name===p),base=s.slug+'/'+p;
el('old').src='../full-style-study/mineral-grid/'+p+'.png';el('new').src=base+'.png';el('old').alt='Original S3: '+e.title;el('new').alt=s.id+' '+s.name+': '+e.title;
el('heading').textContent=s.id+' '+s.name;el('caption').textContent=s.caption;el('swatches').replaceChildren();s.colors.forEach((c,i)=>{const span=document.createElement('span'),sw=document.createElement('i');sw.style.background=c;span.append(sw,document.createTextNode(['Signature ','Companion 1 ','Companion 2 '][i]+c));el('swatches').append(span)});
['png','pdf','svg'].forEach(ext=>el(ext).href=base+'.'+ext);el('all').href=s.slug+'/gallery.pdf';['gray','deutan'].forEach(mode=>el(mode).href='simulations/'+s.id+'/'+mode+'/'+p+'.png')}
el('palette').addEventListener('change',update);el('plot').addEventListener('change',update);update();</script></main></html>'''
    for key,value in [('__OPTIONS__',opts),('__PLOTS__',plots),('__STYLES__',json.dumps(candidates)),('__EXAMPLES__',json.dumps(examples))]:template=template.replace(key,value)
    (OUT/'gallery.html').write_text(template)

def main():
    OUT.mkdir(exist_ok=True)
    protected=list((ROOT/'figures').glob('*'))+[ROOT/'gallery.pdf',ROOT/'gallery-beige.pdf']+list((ROOT/'full-style-study'/'mineral-grid').glob('*'))
    before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
    geometry={};fonts={}
    with use_style(S3):
        for name,title,render in r.EXAMPLES:
            f=render();finish(f,S3,name);geometry[name]=fingerprint(f)
            fonts[name]=[(t.get_fontfamily(),t.get_fontsize(),t.get_fontweight()) for t in f.findobj(Text)]
            plt.close(f)
    audits={s['id']:expanded_audit(s) for s in COOL}
    definitions=[]
    for s in COOL:
        assert {k:v for k,v in s.items() if k not in COLOR_FIELDS}==FIXED
        assert min(audits[s['id']]['extended_contrast'])>=3
        dest=OUT/s['slug'];dest.mkdir(exist_ok=True)
        with use_style(s):
            with PdfPages(dest/'gallery.pdf',metadata={'Title':s['id']+' '+s['name']+' - six original figures'}) as pdf:
                for name,title,render in r.EXAMPLES:
                    fig=render();finish(fig,s,name)
                    assert fingerprint(fig)==geometry[name],(s['id'],name,'data geometry changed')
                    assert [(t.get_fontfamily(),t.get_fontsize(),t.get_fontweight()) for t in fig.findobj(Text)]==fonts[name]
                    fig.canvas.draw()
                    for ext in ['png','pdf','svg']:fig.savefig(dest/f'{name}.{ext}',dpi=300,facecolor=s['canvas'])
                    pdf.savefig(fig,facecolor=s['canvas']);plt.close(fig)
            definitions.append({**s,'theme':asdict(theme.T),'assignments':assignments(s),
                'category_mappings':{group:list(zip(names,assignments(s)[group])) for group,names in [
                    ('methods',METHODS),('comparison',list(r.raw.data_comparison_IEDB['methods'])),('composition',list(r.brute.data_brute_force_math['methods']))]}})
        print('Rendered '+s['id']+' '+s['name'],flush=True)
    theme.apply_theme()
    with PdfPages(OUT/'s3-cool-palettes.pdf',metadata={'Title':'S3: five cooler palettes','Author':'Plotting style study'}) as pdf:
        for kind,filename in [('lines','overview'),('bars','bars-overview')]:
            f=comparison(kind);pdf.savefig(f,facecolor='white');f.savefig(OUT/f'{filename}.png',dpi=170);plt.close(f)
        f=research();pdf.savefig(f,facecolor='white');plt.close(f)
        for i,s in enumerate(COOL):
            with use_style(s):
                f=profile(s,i+4);pdf.savefig(f,facecolor='white');f.savefig(OUT/s['slug']/'profile.png',dpi=170);plt.close(f)
        f=review(audits);pdf.savefig(f,facecolor='white');f.savefig(OUT/'color-review.png',dpi=170);plt.close(f)
    for s in COOL:
        for name,_,_ in r.EXAMPLES:
            with Image.open(OUT/s['slug']/f'{name}.png') as im:
                im=im.convert('RGB');im.thumbnail((1600,1250));rgb=np.asarray(im,dtype=float)/255
                for mode in ['deutan','gray']:
                    dest=OUT/'simulations'/s['id']/mode;dest.mkdir(parents=True,exist_ok=True)
                    Image.fromarray(np.uint8(np.round(simulate(rgb,mode)*255))).save(dest/f'{name}.png')
    docs(audits);gallery()
    assert before=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in before}
    (OUT/'palettes.json').write_text(json.dumps({'panel_background':'#EBF1F5','fixed_S3':FIXED,
        'fixed_typography':{'font':theme.FONT,'weight':'normal','labels_pt':BASE.base,'ticks_legends_pt':BASE.small,'titles_pt':BASE.title},
        'sources':SOURCES,'candidates':definitions},indent=2)+'\n')
    (OUT/'validation.json').write_text(json.dumps({'source_geometry_equal':True,'typography_fixed':True,
        'all_non_palette_S3_tokens_equal':True,'source_fingerprints':geometry,'protected_exports_sha256':before,
        'candidates':audits,'figure_count':30,'example_count':6,'candidate_count':5},indent=2)+'\n')
    print('Saved 30 figures in PNG/PDF/SVG, 5 six-page galleries and a 9-page comparison.',flush=True)

if __name__=='__main__':main()
