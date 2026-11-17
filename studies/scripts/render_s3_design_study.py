"""Research-led mixed-hue alternatives on S3. Does not overwrite prior studies."""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/figures4papers-mpl')
from pathlib import Path
from dataclasses import asdict
import json, hashlib, html
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
from s3_design_palettes import S3, PROPOSALS, SOURCES, FIXED, COLOR_FIELDS
from render_style_exploration import (
    use_style,finish,fingerprint,assignments,draw_line,write_text,BASE,METHODS,
)
from render_s3_cool_study import bars, expanded_audit
from palette_color_math import simulate, contrast

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'s3-design-study'
ALL=[S3]+PROPOSALS
REFS={s['id']:s for s in SOURCES}
SHORT_REFS=['Original S3 reference','Garden Home / Gisbert Poppler','Pinterest Palette 2026',
            'Gunia showroom / Temp Project','Benjamin Moore + Little Greene','Benjamin Moore archive / c. 1930']

def page(title,subtitle,n):
    f=plt.figure(figsize=(14.5,10.2),facecolor='white')
    write_text(f,.045,.962,title,22)
    write_text(f,.045,.912,subtitle,10)
    f.add_artist(Line2D([.045,.955],[.88,.88],transform=f.transFigure,color='#566C7B',lw=.45))
    write_text(f,.045,.032,'S3 DESIGN PALETTES  /  #EBF1F5 panels  /  Helvetica Regular  /  Original source data',8,color='#666666')
    f.text(.955,.032,str(n),ha='right',va='top',fontsize=8,color='#666666')
    return f

def comparison(kind='lines'):
    f=page('Warm and cool accents on S3' if kind=='lines' else 'More variety across nine categories',
           'Five adaptations of design precedents, beside the original. Background, font, line weights, grids and borders stay fixed.',
           1 if kind=='lines' else 2)
    for i,s in enumerate(ALL):
        x=.045+(i%3)*.313;top=.846-(i//3)*.392
        write_text(f,x,top,'S3  Original palette' if i==0 else s['id']+'  '+s['name'],12.7)
        write_text(f,x,top-.034,SHORT_REFS[i],8.5,color='#566C7B')
        for j,c in enumerate(s['palette']['colors'][:3]):
            sx=x+j*.091
            f.add_artist(Rectangle((sx,top-.084),.075,.019,transform=f.transFigure,facecolor=c,edgecolor='none'))
            write_text(f,sx,top-.089,c,7.3)
        with use_style(s):
            ax=f.add_axes([x+.030,top-.312,.246,.187])
            draw_line(ax,s) if kind=='lines' else bars(ax,s)
    write_text(f,.045,.078,'Swatch order: signature / companion 1 / companion 2. Curves: VIGIL / DPO / DA-DPO. These are original sRGB adaptations.',8.4,color='#666666')
    return f

def precedents():
    f=page('Actual design precedents for the pale blue surface',
           'The sources use pale/cool blues or blue-gray surroundings. None is claimed to use the exact S3 hex.',3)
    summaries=[
        ('Garden Home: light blue, crimson and mustard',
         'Gisbert Poppler combines the three hues across a villa, with green and orange elsewhere. R1 makes the blue/red/gold accents into a plotting core.'),
        ('Pinterest: icy blue with plum, orange-red and yellow-green',
         'The published palette includes Cool Blue #D7EFFF, Plum Noir, Persimmon, Wasabi and Jade. R2 adapts three accent families and increases mark contrast.'),
        ('Gunia showroom: pale blue, dark wood, rose and green',
         'Temp Project retains dark wood alongside pale blue, pink and green. Hospitality Design explicitly notes the chocolate/pale-blue pairing. R3 uses darker cocoa, rose and jade.'),
        ('Paint guidance: blue/orange and blue/yellow',
         'Benjamin Moore demonstrates blue with orange-red; Little Greene pairs blue walls with yellow woodwork. R4 combines those relationships as petrol, coral and saffron.'),
        ('Benjamin Moore archive: pale blue, red, gray-green and blue',
         'The circa-1930 scheme has a light blue ceiling, a gray-green rug, red upholstery and blue bookcases. R5 adapts the accents to wine, olive and denim.'),
    ]
    for i,(s,(head,body)) in enumerate(zip(PROPOSALS,summaries)):
        y=.835-i*.143
        write_text(f,.045,y,s['id']+'  '+head,12)
        write_text(f,.045,y-.034,body,10,width=147)
        for j,key in enumerate(s['palette']['sources']):
            source=REFS[key]
            t=write_text(f,.045+j*.45,y-.090,'Open source '+key+': '+source['title'],8.3,color='#285F96')
            t.set_url(source['url'])
    write_text(f,.045,.094,'Interpretation: use pale blue as the quiet surface, then let warm and cool accents supply the variety. Paint names are not hex matches.',9,color='#566C7B')
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
    write_text(f,.045,.309,'DESIGN RELATIONSHIP',11)
    write_text(f,.045,.274,s['palette']['precedent'],11)
    write_text(f,.045,.237,s['best'],10)
    write_text(f,.045,.203,'Reading tradeoff: '+s['tradeoff'],9.5)
    write_text(f,.045,.161,'References '+', '.join(s['palette']['sources'])+' on page 3. All proposed hex values are authored for S3.',9.5,color='#566C7B')
    write_text(f,.045,.123,'Panel #EBF1F5  |  White margins  |  Helvetica Regular  |  Curves 1.25 pt  |  Error bars 0.65 pt  |  Open markers 3.5 pt',9.5)
    write_text(f,.045,.094,'Four-sided frame #566C7B at 0.45 pt  |  Dotted grid #CBD6DF at 0.45 pt  |  All source data and axis ranges retained',9.5)
    return f

def review(audits):
    f=page('Hue variety and the limits of color alone',
           'Core colors in the same order under each preview. Swatches and the fixed S3 background are transformed together.',9)
    modes=[('normal','Original'),('deutan','Deutan simulation'),('protan','Protan simulation'),('tritan','Tritan simulation'),('gray','Grayscale')]
    for j,(_,head) in enumerate(modes):write_text(f,.27+j*.138,.835,head,9)
    for i,s in enumerate(PROPOSALS):
        y=.765-i*.105
        write_text(f,.045,y+.02,s['id']+'  '+s['name'],10.5)
        a=audits[s['id']]
        write_text(f,.045,y-.017,f"Core contrast: {min(a['core_contrast']):.2f}-{max(a['core_contrast']):.2f}:1",9,color='#566C7B')
        for j,(mode,_) in enumerate(modes):
            x=.27+j*.138
            f.add_artist(Rectangle((x-.009,y-.036),.128,.071,transform=f.transFigure,
                                  facecolor=simulate(np.array(to_rgb(s['panel'])),mode),edgecolor='none'))
            cs=simulate(np.array([to_rgb(c) for c in s['palette']['colors'][:3]]),mode)
            for k,c in enumerate(cs):f.add_artist(Rectangle((x+k*.037,y-.017),.030,.035,transform=f.transFigure,facecolor=c,edgecolor='none'))
    minimum=min(min(a['extended_contrast']) for a in audits.values())
    write_text(f,.045,.212,'CHECKED AT THE INTENDED PANEL COLOR',11)
    write_text(f,.045,.175,f'All nine opaque category colors in each proposal exceed 3:1 against #EBF1F5 (minimum {minimum:.2f}:1). This measures mark/background contrast only; it does not certify category separation, antialiasing or transparent fills.',10,width=146)
    write_text(f,.045,.115,'Warm/cool contrast gives more hue variety, but red-green differences can still collapse in simulation. The original marker shapes, dash patterns, labels and category positions are retained. These previews are approximate, not accessibility certification.',10,width=146)
    return f

def docs(audits):
    lines=['# S3: mixed warm/cool design palettes','',
        'This revision responds to the rejected C1-C5 study: the background is a quiet pale blue-gray surface, while plotted colors span warm and cool families. **R1 is selected**: cobalt / brick / gold on S3. See the [current style guide](../README.md). R2-R5 remain comparison alternatives.','',
        '[Compare all examples](gallery.html) · [Nine-page comparison PDF](s3-design-palettes.pdf) · [Overview](overview.png) · [Nine-category comparison](bars-overview.png)','',
        '## Actual design precedents','',
        'Research accessed 2026-11-15. Sources contain pale-blue or blue-gray surroundings and mixed accent colors; none is claimed to use the exact S3 hex. Findings below are sourced; the translation into plotting colors is our design interpretation. No complete brand palette is reproduced, and no paint-to-sRGB match is claimed.','']
    for q in SOURCES:
        lines += [f"### {q['id']}. [{q['title']}]({q['url']})",'',q['kind']+'. '+q['finding'],'',q['application'],'']
    lines += ['## Fixed background and typography','',
        '- Panel **#EBF1F5**, margins **#FFFFFF**. All original non-palette S3 tokens are fixed.',
        '- **Helvetica Regular**, 10 pt axis labels, 8.57 pt ticks/legends, 11.43 pt panel titles. Existing smaller annotations and math settings are retained.',
        '- Data curves **1.25 pt**, errors **0.65 pt**, caps 2 pt, hollow markers **3.5 pt**.',
        '- Four-sided frame **#566C7B**, **0.45 pt**; dotted xy grid **#CBD6DF**, **0.45 pt**; ticks 2 pt.',
        '- Bar width 0.70; bar outlines 0.35 pt. Fill opacities: concepts 0.08, trends 0.14 / 0.22, radar 0.035.',
        '- Text #282828, secondary text #666666, hatches #707070. Source values, uncertainty, labels, axis ranges, geometry and method order remain fixed. Only the data palette, including the diagram prior color, changes.','',
        '## Five proposals','',
        '| Option | Signature | Companion 1 | Companion 2 | Source references | Six examples |',
        '|---|---|---|---|---|---|']
    for s in PROPOSALS:
        p=s['palette'];c=p['colors']
        lines.append(f"| {s['id']} {s['name']} | {c[0]} | {c[1]} | {c[2]} | {', '.join(p['sources'])} | [PDF]({s['slug']}/gallery.pdf) |")
    lines += ['', 'The core swatches map to VIGIL / DPO / DA-DPO respectively in the line and radar examples. The expanded nine-color lists are categorical, not sequential measurement scales.','']
    for s in PROPOSALS:
        p=s['palette'];a=audits[s['id']]
        lines += [f"### {s['id']} {s['name']}",'',s['caption'],'',p['precedent']+'. '+s['best'],'',
                  'Reading tradeoff: '+s['tradeoff'],'','| Role | Name | Hex |','|---|---|---|']
        for i,(name,c) in enumerate(zip(p['names'],p['colors'])):
            lines.append(f"| {['Signature','Companion 1','Companion 2','Extended 4','Extended 5','Extended 6'][i]} | {name} | `{c}` |")
        for i,c in enumerate(p['extra']):lines.append(f'| Extended {i+7} | Supporting category | `{c}` |')
        lines += [f"| Diagram prior | Neutral | `{p['neutral']}` |",'',
                  f"Opaque core contrast on S3: {', '.join(str(c)+':1' for c in a['core_contrast'])}.",'']
        for group,names in [('methods',METHODS),('comparison',list(r.raw.data_comparison_IEDB['methods'])),('composition',list(r.brute.data_brute_force_math['methods']))]:
            lines += [f'**{group}, original source order**','',
                      '; '.join(f'{n}: `{c}`' for n,c in zip(names,assignments(s)[group]))+'.','']
    lines += ['## What the checks mean','',
        'All nine opaque category colors exceed 3:1 against the panel. This is not a guarantee of category-to-category separation, small antialiased mark contrast or transparent-fill contrast. Warm/cool contrasts also have red-green color-vision limits. Retain marker shapes, dash patterns, labels and category order. Full-figure deutan/grayscale previews are provided. Numerical screens for normal, protan, deutan, tritan and grayscale appear in `validation.json`; the 0.06 Oklab close-pair flag is an editorial heuristic, not an accessibility standard.','',
        '## Files and reproduction','',
        'Thirty figures: six original examples for each of five proposals, in 300 dpi PNG, embedded-font PDF and editable-text SVG. Five six-page galleries and the nine-page report supplement those exports. The sphere and manually assembled composites remain excluded.','',
        '```sh','MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_s3_design_study.py','```','',
        'Source definitions: [s3_design_palettes.py](../s3_design_palettes.py). Renderer: [render_s3_design_study.py](../render_s3_design_study.py). Exact tokens and category mappings: [palettes.json](palettes.json).','',
        'Source figures/data: [Chen Liu, figures4papers](https://github.com/ChenLiu-1996/figures4papers), commit `0ddfbd3fc9892e804a3fa01ae46bd0d32617f2aa`, [CC BY-NC 4.0](../upstream/LICENSE). Original data and potentially truncated axes are retained for comparison. Concept examples are illustrative, not new observations.','']
    (OUT/'README.md').write_text('\n'.join(lines))

def gallery():
    candidates=[dict(id=s['id'],name=s['name'],slug=s['slug'],caption=s['caption'],
        colors=s['palette']['colors'][:3],sources=[REFS[k] for k in s['palette']['sources']]) for s in PROPOSALS]
    examples=[dict(name=n,title=t) for n,t,_ in r.EXAMPLES]
    opts=''.join(f'<option value="{i}">{s["id"]} {html.escape(s["name"])}</option>' for i,s in enumerate(PROPOSALS))
    plots=''.join(f'<option value="{e["name"]}"'+(' selected' if e['name']=='comparison_posttraining' else '')+f'>{html.escape(e["title"])}</option>' for e in examples)
    text='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Warm and cool accents on S3</title>
<style>*{box-sizing:border-box}body{margin:0;background:white;color:#282828;font:16px Helvetica,Arial,sans-serif}main{max-width:1600px;margin:auto;padding:36px 32px 60px}h1,h2{font-weight:400}h1{font-size:34px;margin:0 0 12px}h2{font-size:22px}p{line-height:1.5;max-width:1100px}a{color:#285F96}nav,.controls{display:flex;gap:22px;flex-wrap:wrap;margin:24px 0}.controls{padding:20px;background:#EBF1F5;border:1px solid #CBD6DF}label{display:grid;gap:8px}select{font:inherit;padding:9px 12px;background:#fff;border:1px solid #566C7B;max-width:100%}.pair{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:24px}article{min-width:0}img{display:block;width:100%;height:auto;border:1px solid #D8E1E8}.note{font-size:14px;color:#566C7B}#swatches{display:flex;gap:15px;flex-wrap:wrap;margin:18px 0}#swatches span{display:flex;align-items:center;gap:7px;font-size:14px}i{display:inline-block;width:28px;height:20px}footer{border-top:1px solid #CBD6DF;margin-top:40px;padding-top:16px;font-size:13px;color:#566C7B}@media(max-width:900px){.pair{grid-template-columns:1fr}main{padding:24px 16px}h1{font-size:28px}}</style>
<main><h1>Warm and cool accents on S3</h1><p>Five new proposals grounded in actual design projects and palettes. The pale blue-gray <b>#EBF1F5</b> surface stays fixed, with mixed warm and cool plotted colors.</p>
<nav><a href="s3-design-palettes.pdf">Comparison PDF</a><a href="README.md">Research and exact colors</a><a href="palettes.json">Palette definitions</a><a href="bars-overview.png">Nine-category comparison</a></nav>
<div class="controls"><label>Palette<select id="palette">__OPTIONS__</select></label><label>Example<select id="plot">__PLOTS__</select></label></div>
<p id="caption" aria-live="polite"></p><div id="swatches"></div><p id="sources" class="note"></p>
<div class="pair"><article><h2>S3 original palette</h2><img id="old" alt="Original S3"><p class="note">Original blue, clay and moss reference.</p></article><article><h2 id="heading"></h2><img id="new" alt="Revised palette"><p><a id="png">PNG</a> · <a id="svg">SVG</a> · <a id="pdf">PDF</a> · <a id="all">All six examples</a></p><p><a id="gray">Grayscale preview</a> · <a id="deutan">Deutan preview</a></p></article></div>
<h2>All five directions beside the original</h2><a href="overview.png"><img src="overview.png" alt="Original S3 and five mixed warm and cool palettes"></a>
<p class="note">All five retain Helvetica Regular and every non-palette S3 setting. The colors are authored sRGB adaptations; source interiors are not claimed to match the exact background hex. Shape, dash and label encodings remain essential.</p>
<noscript><p>The comparison PDF and README work without JavaScript.</p></noscript>
<footer>Original examples: <a href="https://github.com/ChenLiu-1996/figures4papers">Chen Liu / figures4papers</a>, CC BY-NC 4.0. Prior studies and approved exports remain intact.</footer>
<script>const styles=__STYLES__,examples=__EXAMPLES__;const el=id=>document.getElementById(id);
function update(){const s=styles[Number(el('palette').value)],p=el('plot').value,e=examples.find(x=>x.name===p),base=s.slug+'/'+p;
el('old').src='../full-style-study/mineral-grid/'+p+'.png';el('new').src=base+'.png';el('old').alt='Original S3: '+e.title;el('new').alt=s.id+' '+s.name+': '+e.title;
el('heading').textContent=s.id+' '+s.name;el('caption').textContent=s.caption;el('swatches').replaceChildren();s.colors.forEach((c,i)=>{const span=document.createElement('span'),sw=document.createElement('i');sw.style.background=c;span.append(sw,document.createTextNode(['Signature ','Companion 1 ','Companion 2 '][i]+c));el('swatches').append(span)});
el('sources').replaceChildren(document.createTextNode('Design precedents: '));s.sources.forEach((q,i)=>{if(i)el('sources').append(document.createTextNode(' · '));const a=document.createElement('a');a.href=q.url;a.textContent=q.title;el('sources').append(a)});
['png','pdf','svg'].forEach(ext=>el(ext).href=base+'.'+ext);el('all').href=s.slug+'/gallery.pdf';['gray','deutan'].forEach(mode=>el(mode).href='simulations/'+s.id+'/'+mode+'/'+p+'.png')}
el('palette').addEventListener('change',update);el('plot').addEventListener('change',update);update();</script></main></html>'''
    for key,value in [('__OPTIONS__',opts),('__PLOTS__',plots),('__STYLES__',json.dumps(candidates)),('__EXAMPLES__',json.dumps(examples))]:text=text.replace(key,value)
    (OUT/'gallery.html').write_text(text)

def main():
    OUT.mkdir(exist_ok=True)
    protected=list((ROOT/'figures').glob('*'))+[ROOT/'gallery.pdf',ROOT/'gallery-beige.pdf']
    protected+=list((ROOT/'full-style-study'/'mineral-grid').glob('*'))+list((ROOT/'s3-cool-study').rglob('*'))
    before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
    geometry={};fonts={}
    with use_style(S3):
        for name,title,render in r.EXAMPLES:
            f=render();finish(f,S3,name);geometry[name]=fingerprint(f)
            fonts[name]=[(t.get_fontfamily(),t.get_fontsize(),t.get_fontweight()) for t in f.findobj(Text)];plt.close(f)
    audits={s['id']:expanded_audit(s) for s in PROPOSALS};definitions=[]
    for s in PROPOSALS:
        assert {k:v for k,v in s.items() if k not in COLOR_FIELDS}==FIXED
        assert min(contrast(c,s['panel']) for c in s['palette']['colors']+s['palette']['extra'])>3
        dest=OUT/s['slug'];dest.mkdir(exist_ok=True)
        with use_style(s):
            with PdfPages(dest/'gallery.pdf',metadata={'Title':s['id']+' '+s['name']+' - six source examples'}) as pdf:
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
    with PdfPages(OUT/'s3-design-palettes.pdf',metadata={'Title':'Mixed warm and cool accents on S3'}) as pdf:
        for kind,filename in [('lines','overview'),('bars','bars-overview')]:
            f=comparison(kind);pdf.savefig(f,facecolor='white');f.savefig(OUT/f'{filename}.png',dpi=170);plt.close(f)
        f=precedents();pdf.savefig(f,facecolor='white');f.savefig(OUT/'design-precedents.png',dpi=170);plt.close(f)
        for i,s in enumerate(PROPOSALS):
            with use_style(s):
                f=profile(s,i+4);pdf.savefig(f,facecolor='white');f.savefig(OUT/s['slug']/'profile.png',dpi=170);plt.close(f)
        f=review(audits);pdf.savefig(f,facecolor='white');f.savefig(OUT/'color-review.png',dpi=170);plt.close(f)
    for s in PROPOSALS:
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
    print('Saved 30 figures, five six-page galleries and a nine-page research/comparison PDF.',flush=True)

if __name__=='__main__':main()
