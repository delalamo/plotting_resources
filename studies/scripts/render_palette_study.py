"""Render five original color proposals without replacing the approved palette.

Run with the same Python environment as render_examples.py.
Outputs go to palette-study/. All original examples keep their source data.
Only the study's additional heatmaps use synthetic, explicitly labeled data.
"""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/figures4papers-mpl')
from pathlib import Path
from contextlib import contextmanager
from dataclasses import replace, asdict
import json, hashlib, textwrap, html
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap, to_rgb, to_hex
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.text import Text
import minimal_theme as theme
import render_examples as r
from palette_schemes import SCHEMES, SOURCES
from palette_color_math import audit, ramp, simulate, contrast

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'palette-study'
BASE=theme.T
BASE_PALETTES=theme.PALETTES
SOURCE_BY_ID={s['id']:s for s in SOURCES}
PATTERNS=[('s',(0,(4,2))),('^',(0,(3,1.5,1,1.5))),('o','-')]

def palette(s):
    c=s['colors'];e=s['extra']
    return {'methods':[c[1],c[2],c[0]],
            'comparison':[e[0],c[5],e[1],c[3],c[1],c[4],e[2],c[2],c[0]],
            'composition':[c[0],c[1],c[2],c[3],c[4],c[5],e[0]]}

@contextmanager
def use_scheme(s):
    saved=(theme.T,r.T,theme.PALETTES,r.PALETTES)
    try:
        c=s['colors']
        theme.T=r.T=replace(BASE,teal=c[0],rust=c[1],ochre=c[2],taupe=s['neutral'],scatter=c[0])
        theme.PALETTES=r.PALETTES=palette(s)
        with mpl.rc_context():
            theme.apply_theme()
            yield
    finally:
        theme.T,r.T,theme.PALETTES,r.PALETTES=saved

def mark_redundantly(fig):
    """Add shape/line redundancy without moving any data or changing weights."""
    methods=list(r.post.data_posttraining['methods'])
    lookup={name:i for i,name in enumerate(methods)}
    for ax in fig.axes:
        for line in ax.lines:
            if line.get_label() in lookup:
                marker,ls=PATTERNS[lookup[line.get_label()]]
                line.set_marker(marker)
                if ax.name!='polar': line.set_linestyle(ls)
    for leg in fig.legends:
        for label,handle in zip(leg.get_texts(),leg.legend_handles):
            if label.get_text() in lookup and isinstance(handle,Line2D):
                marker,ls=PATTERNS[lookup[label.get_text()]]
                handle.set_marker(marker)
                if not any(ax.name=='polar' for ax in fig.axes):handle.set_linestyle(ls)

def geometry(fig):
    """Digest plotted coordinates, axes ranges and bar geometry, ignoring style."""
    values=[]
    for ax in fig.axes:
        values += [ax.get_xlim(),ax.get_ylim()]
        for line in ax.lines:values.append(np.asarray(line.get_xydata()).round(10).tolist())
        for patch in ax.patches:
            if isinstance(patch,Rectangle):values.append([patch.get_x(),patch.get_y(),patch.get_width(),patch.get_height()])
        for coll in ax.collections:
            values.append(np.asarray(coll.get_offsets()).round(10).tolist())
            values += [p.vertices.round(10).tolist() for p in coll.get_paths()]
    return hashlib.sha256(json.dumps(values,default=float).encode()).hexdigest()

def figure_checks(fig,expected):
    assert geometry(fig)==expected,'Data/geometry drift'
    for ax in fig.axes:
        if ax.name=='polar':continue
        assert np.allclose(ax.get_facecolor()[:3],to_rgb(BASE.background))
        for sp in ax.spines.values():
            assert sp.get_visible() and sp.get_linewidth()==BASE.frame
            assert np.allclose(sp.get_edgecolor()[:3],to_rgb('#000000'))
    for txt in fig.findobj(Text):
        if txt.get_text():assert txt.get_fontfamily()==[theme.FONT]

def text(fig,x,y,string,size=11,width=None,**kwargs):
    if width:string='\n'.join(textwrap.fill(p,width=width,break_long_words=False,break_on_hyphens=False) for p in string.split('\n'))
    return fig.text(x,y,string,va='top',ha='left',fontsize=size,color=BASE.ink,linespacing=1.45,**kwargs)

def page(title,subtitle,number,size=(11.7,8.3)):
    fig=plt.figure(figsize=size,facecolor='white')
    text(fig,.05,.955,title,22)
    text(fig,.05,.902,subtitle,10)
    fig.add_artist(Line2D([.05,.95],[.866,.866],transform=fig.transFigure,lw=.55,color='#000000'))
    text(fig,.05,.037,'PALETTE STUDY  /  Helvetica Regular  /  Cream B #FAF6EE  /  15 November 2026',8)
    fig.text(.95,.037,str(number),ha='right',va='top',fontsize=8)
    return fig

def draw_line(ax,colors,title='',direct=True):
    d=r.post.data_posttraining
    ax.axhline(d['results'][0,0],color='#888888',lw=.8,ls=(0,(4,3)))
    if direct:ax.text(840,d['results'][0,0],'SFT only',fontsize=7,va='bottom',color=BASE.muted)
    for i,(name,y,c) in enumerate(zip(d['methods'],d['results'],colors)):
        marker,ls=PATTERNS[i]
        ax.plot(d['steps'],y,color=c,lw=BASE.line,marker=marker,ms=BASE.marker,ls=ls)
        if direct:ax.text(840,y[-1],['DPO','DA-DPO','VIGIL'][i],fontsize=8,va='center',color=BASE.ink)
    ax.set(xlim=(-25,1050 if direct else 825),ylim=(0,63),xticks=[0,400,800],yticks=[0,20,40,60],xlabel='Post-training steps',ylabel='Performance')
    theme.style_axes(ax)
    if title:ax.set_title(title,fontsize=12)

def comparison():
    fig=page('Five color directions, one plotting style','Same source curves, same axes, same font and strokes. The approved palette is shown first for reference.',1,size=(13.5,10.3))
    schemes=[dict(id='Current',name='Approved teal & earth',colors=[BASE.teal,BASE.rust,BASE.ochre])]+SCHEMES
    for i,s in enumerate(schemes):
        col=i%3;row=i//3;x=.07+col*.315;y=.545-row*.39
        ax=fig.add_axes([x,y,.265,.235])
        draw_line(ax,[s['colors'][1],s['colors'][2],s['colors'][0]],direct=True)
        text(fig,x,y+.315,s['id']+'  '+s['name'],13)
        for j,c in enumerate(s['colors'][:3]):
            fig.add_artist(Rectangle((x+j*.085,y+.28),.075,.012,transform=fig.transFigure,facecolor=c,edgecolor='none'))
        text(fig,x,y+.263,' / '.join(s['colors'][:3]),8)
    text(fig,.05,.079,'Start with P2 for a distinctive identity, P3 for a warmer material feel, or P5 for a more energetic print aesthetic.',10)
    return fig

def research_pages():
    fig=page('What the established systems teach us','Research synthesis: borrow repeatable rules and color relationships, then author a new palette.',2)
    items=[('One signature, a small working set','The Economist uses a deliberately limited palette; ONS also favors restrained category counts and highlighting. For us: one signature hue, two companions and a neutral. [1, 3]'),
           ('Keep identity separate from magnitude','Datawrapper separates categorical, highlight, neutral and scale colors. Our category swatches identify methods; dedicated ramps encode measured values. [4]'),
           ('Scientific publishing has distinct systems','Nature separates accent and context colors in commissioned illustrations; its research-figure guide has different constraints. ACS and Okabe-Ito emphasize accessible palettes and redundant labels/symbols. [5, 6, 15, 16]'),
           ('An opportunity, not a measured gap','I found useful cross-domain directions, not evidence that any exact palette is rare across scientific publishing. “Distinctive” here is a design judgment, not a prevalence or exclusivity claim.')]
    for i,(head,body) in enumerate(items):
        y=.82-i*.176
        text(fig,.055,y,head,14)
        text(fig,.055,y-.043,body,11,width=117)
    return fig

def domain_page():
    fig=page('Translate the design language','The proposals use newly selected sRGB colors. They do not reproduce a publication or designer palette.',3)
    cards=[('Architecture and interiors','Le Corbusier color keyboards organize solids, graded shades and contrasts. The transferable idea is a family of mineral colors with a quiet ground, rather than one official swatch set. [8]','P1 mineral blue / clay; P2 aubergine / brass; P4 petrol / rose'),
           ('Textiles and surface materials','The Albers Foundation documents links between woven works, printmaking and functional design. Cloth, dye and material associations are a creative prompt here, not a sampled historical color standard. [10]','P2 aubergine / brass; P3 oxblood / denim / lichen'),
           ('Printmaking and graphic design','Martian Press describes a finite Riso ink library and the effect of transparent inks and paper. We borrow palette discipline, while using opaque marks and restrained saturation for quantitative plots. [11]','P5 violet ink / persimmon / lake blue'),
           ('Color in context','Albers teaches observation of interacting colors; the BBC cookbook separates chart structure from data-color choices. Test each proposal at actual line widths and fill areas on cream B. [2, 9]','All five: fixed Helvetica, black frame, warm grid and cream panels')]
    for i,(head,body,transfer) in enumerate(cards):
        y=.82-i*.177
        text(fig,.055,y,head,14)
        text(fig,.055,y-.043,body,10.5,width=121)
        text(fig,.055,y-.115,transfer,10)
    return fig

def profile(s,number):
    fig=page(s['id']+'  '+s['name'],s['origin']+'  |  '+s['subtitle'],number)
    text(fig,.05,.828,s['idea'],10.5,width=129)
    # Six named colors; first three form the everyday core.
    for i,(name,c) in enumerate(zip(s['names'],s['colors'])):
        x=.05+i*.153
        fig.add_artist(Rectangle((x,.696),.135,.055,transform=fig.transFigure,facecolor=c,edgecolor='none'))
        text(fig,x,.686,name,9)
        text(fig,x,.665,c+('  / core' if i<3 else ''),8)
    ax=fig.add_axes([.09,.35,.37,.255]);draw_line(ax,palette(s)['methods'])
    ax.set_title('Three-series identity',fontsize=11)
    # Source AUROC point-and-interval view: direct labels avoid nine-color decoding.
    ax=fig.add_axes([.64,.35,.30,.255]);d=r.raw.data_comparison_IEDB
    names=['Prime-2.1','NetMHCpan','MHCnuggets','MHCflurry','DeepNeo','BigMHC-EL','BigMHC-IM','BigMHC retrained','ImmunoStruct']
    for i,(v,e) in enumerate(zip(d['mean'][:,0],d['std'][:,0])):
        ax.errorbar(v,i,xerr=e,fmt='o',color=s['colors'][0] if i==8 else s['neutral'],ms=4.3 if i==8 else 3.5,elinewidth=.65,capsize=2)
    ax.set(yticks=range(9),yticklabels=names,xlim=(.48,.92),ylim=(-.6,8.6),xlabel='AUROC',xticks=[.5,.6,.7,.8,.9])
    ax.invert_yaxis();theme.style_axes(ax,grid='x');ax.tick_params(axis='y',labelsize=7.8)
    ax.set_title('Signature + quiet comparators',fontsize=11)
    # Deterministic illustrative heatmaps; these are not repository observations.
    yy,xx=np.mgrid[0:5,0:6]
    magnitude=(np.sin(xx*.7+yy*.45)+1)/2
    difference=np.sin(xx*.85-yy*.55)
    for k,(data,div,title) in enumerate([(magnitude,False,'Sequential: magnitude'),(difference,True,'Diverging: signed difference')]):
        ax=fig.add_axes([.09+k*.46,.135,.32,.12])
        cmap=ListedColormap(ramp(s,div));im=ax.imshow(data,cmap=cmap,vmin=-1 if div else 0,vmax=1,aspect='auto',interpolation='nearest')
        ax.set(xticks=[],yticks=[]);theme.style_axes(ax,grid='');ax.set_title(title,fontsize=10,pad=6)
        cax=fig.add_axes([.42+k*.46,.135,.011,.12]);fig.colorbar(im,cax=cax,ticks=[-1,0,1] if div else [0,.5,1]);cax.tick_params(labelsize=7,length=0)
    text(fig,.05,.087,'Heatmaps: identical synthetic demonstration data. Ramps are prototypes; all six original example plots are in this palette’s gallery.',8.5)
    return fig

def quality_page(audits):
    fig=page('Readability checks and practical limits','All five proposals pass the opaque-color contrast screen; dense category sets still need redundant labels.',9)
    text(fig,.05,.823,'Three-color cores under simulated viewing conditions',13)
    modes=['normal','protan','deutan','tritan','gray']
    for j,label in enumerate(['Original','Protan simulation','Deutan simulation','Tritan simulation','Grayscale']):text(fig,.255+j*.14,.77,label,8.5)
    for i,s in enumerate(SCHEMES):
        y=.708-i*.079;text(fig,.05,y+.016,s['id']+'  '+s['name'],10)
        for j,mode in enumerate(modes):
            rgb=simulate(np.array([to_rgb(h) for h in s['colors'][:3]]),mode)
            for k,c in enumerate(rgb):fig.add_artist(Rectangle((.255+j*.14+k*.038,y-.012),.032,.035,transform=fig.transFigure,facecolor=c,edgecolor='none'))
    minimum=min(v for a in audits.values() for v in a['opaque_contrast_on_cream'].values())
    paragraphs=[f'Contrast: all 45 proposed opaque category colors are at least {minimum:.2f}:1 against #FAF6EE. This 3:1 screen applies to opaque marks; translucent fills are supported by outlines, curves and labels. It does not establish full WCAG compliance. [12]',
        'Simulation: Machado severity-100 transforms on linear RGB, plus luminance grayscale. Marker shapes and line patterns preserve a second cue when hues converge. Expanded seven/nine-color examples are stress tests, not certified colorblind-safe sets. [6, 14]',
        'Ramps: Oklab interpolation with chroma reduction to stay in sRGB. Sequential luminance decreases monotonically; diverging halves lighten toward a centered zero. These are checked prototypes, not comprehensively validated scientific colormaps. [7, 13]',
        'Selection: P2 is my recommendation for identity; P3 is a strong warm alternative; P5 is the most lively. Choose a direction before assigning permanent semantic category names.']
    for i,p in enumerate(paragraphs):text(fig,.05,.31-i*.061,p,9.3,width=139)
    return fig

def reference_pages():
    for page_index in range(2):
        fig=page('Sources and reproducibility', 'Primary guides, practitioners and technical methods. Links are clickable in the PDF.',10+page_index)
        for i,s in enumerate(SOURCES[page_index*8:(page_index+1)*8]):
            y=.82-i*.089;number=page_index*8+i+1
            text(fig,.05,y,f'[{number}] {s["title"]}',11,url=s['url'])
            text(fig,.05,y-.031,s['finding'],9,width=143)
        yield fig

def write_docs(audits):
    lines=['# Color identity study','',
      'Five original proposals on the approved **B / #FAF6EE** plot background, with **Helvetica Regular**, 0.55 pt black frames and 1.15 pt curves. The approved theme remains the default.', '',
      '[Browse and switch all six plots](gallery.html) · [Research and visual comparison](palette-study.pdf) · [Quick comparison](comparison.png)', '',
      '## Recommendation','',
      '**Start with P2 Aubergine & Brass.** It provides a more distinctive signature while staying quiet enough for scientific figures. P3 Oxide & Denim is the warmest alternative; P5 Ink & Persimmon has more graphic energy. P1 is the conservative all-purpose choice. P4 is the closest evolution of the current style.', '',
      '“Distinctive” is a design judgment. This research did not measure palette prevalence across scientific publications or establish that these colors are unique. The combinations are newly selected; no complete brand palette was copied.', '',
      '## What the research changes','',
      'Use a signature hue consistently, two companion hues for everyday comparisons, and a neutral for context. Keep category identity separate from sequential or diverging magnitude scales. Expanded palettes are useful in dense bar examples, but permanent scientific figures should favor direct labels, a smaller active set, or a signature-plus-neutral view.', '',
      'The six source figures retain their arrays, uncertainty values, axes, geometry and ordering. The line and radar samples add distinct marker shapes; line samples also distinguish dash patterns. The source bar examples still have their original truncated y axes. The profile pages add a directly labeled AUROC point-and-interval view using those same supplied uncertainty values. Only the explicitly labeled heatmaps use synthetic data.', '',
      '## Exact palette definitions','',
      'First color = signature; next two = companions. Colors 4–6 extend the set. Hex values are sRGB. Keep text #282828, secondary text #666666, grid #E3DCCF, border #000000, margins #FFFFFF. Font and size rules remain in the [approved style guide](../README.md).','']
    for s in SCHEMES:
        a=audits[s['id']];lines += [f'### {s["id"]}: {s["name"]}','',s['idea'],'',s['use'],'',
            '| Role / color | Hex | Opaque contrast on cream |','|---|---|---|']
        for i,(n,c) in enumerate(zip(s['names'],s['colors'])):
            role='Signature' if i==0 else 'Companion' if i<3 else 'Extended'
            lines.append(f'| {role}: {n} | `{c}` | {a["opaque_contrast_on_cream"][c]:.2f}:1 |')
        lines += ['',f'Context neutral: `{s["neutral"]}`. Extra dense-bar colors: '+', '.join(f'`{c}`' for c in s['extra'])+'.','',
            f'[Six-figure PDF]({s["slug"]}/gallery.pdf) · [Profile]({s["slug"]}/profile.png)','',
            '**Use with care:** '+s['caution'],'',
            'Sequential nine-stop preview: '+', '.join('`'+h+'`' for h in a['sequential_9_stops'])+'.','',
            'Diverging nine-stop preview, negative to positive: '+', '.join('`'+h+'`' for h in a['diverging_9_stops'])+'.','',
            'Inspiration: '+', '.join('['+SOURCE_BY_ID[k]['title']+']('+SOURCE_BY_ID[k]['url']+')' for k in s['sources'])+'.','']
    lines += ['## Assignment rules','',
        '- Three methods: DPO = companion 1 / square / dashed; DA-DPO = companion 2 / triangle / dash-dot; VIGIL = signature / circle / solid. Radar retains solid lines with distinct shapes.',
        '- Two trend categories: evaluation/application = companion 1; methodological contribution = signature. Original fill opacity is retained.',
        '- Nine-method bars: extra 1, color 6, extra 2, color 4, color 2, color 5, extra 3, color 3, signature. Seven-method composition: colors 1–6, then extra 1. Complete category-to-hex assignments are in palettes.json.',
        '- Prefer the first three colors for thin lines. The extended set is a candidate vocabulary, not nine equally distinguishable series under every viewing condition.',
        '- A category keeps its color across figures; add explicit labels and shapes. Do not assign a color purely by its position in a changing sort order.',
        '- Sequential ramps represent magnitude. Diverging ramps require a meaningful midpoint; use symmetric limits for signed comparisons. The missing-data color should be separately explained, never silently conflated with zero.', '',
        '## Checks and limits','',
        'All 45 proposed opaque category colors exceed 3:1 against the cream background. This is a design screen, not full WCAG certification; contrast to adjacent data colors and opacity also matter. Detailed numbers, close-pair flags and monotonic ramp checks are in [validation.json](validation.json).', '',
        'The gallery shows Machado severity-100 protan/deutan/tritan simulations and grayscale on the actual plots. These are approximations, not user testing or a guarantee of accessibility. Oklab distances below 0.06 are flagged for review as an editorial heuristic, not an accepted accessibility threshold. Grayscale collapses some categories in every palette; labels, positions, marker shapes and line styles carry the remaining distinctions.', '',
        'Sequential and diverging ramps are interpolated in Oklab, with chroma reduced to stay within sRGB. Monotonic luminance is checked at 257 samples. This alone does not establish perceptual uniformity or equal discriminability under all color-vision conditions. For sensitive quantitative imaging, prefer a validated scientific colormap and retain the house identity in labels and categorical marks.', '',
        'Submission settings remain journal-specific. Nature currently asks for ticks, discourages grids and patterns, and specifies different final text sizes. The cream/grid/hatch house style is therefore not a claim of automatic Nature submission compliance. RGB-to-CMYK print proofs may also change color appearance. [Nature specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)', '',
        '## Research notes','',
        '| Source | Published practice | Adaptation |','|---|---|---|']
    for s in SOURCES:lines.append(f'| [{s["title"]}]({s["url"]}) | {s["finding"]} | {s["transfer"]} |')
    lines += ['', 'Sources accessed 15 November 2026. Original example data and drawings: [Chen Liu / figures4papers](https://github.com/ChenLiu-1996/figures4papers), commit `0ddfbd3fc9892e804a3fa01ae46bd0d32617f2aa`, CC BY-NC 4.0. Existing provenance and untouched source snapshot remain in the parent directory.', '',
        '## Reproduce','',
        'From the repository root, using the existing requirements:', '',
        '```sh','python figures4papers-minimal/render_palette_study.py','```','',
        'Definitions: `../palette_schemes.py`. Rendering and temporary palette context: `../render_palette_study.py`. Color math: `../palette_color_math.py`. The approved default is not switched by running the study. No new runtime dependencies are required.','']
    (OUT/'README.md').write_text('\n'.join(lines))

def write_html():
    data=[dict(id='Current',slug='',name='Approved teal & earth',subtitle='Approved reference',colors=[BASE.teal,BASE.rust,BASE.ochre],idea='Current approved color system.',use='Reference only.',caution='Original palette; no new readability certification.')]+SCHEMES
    buttons=''.join(f'<button type="button" data-index="{i}" aria-pressed="{str(i==2).lower()}">{s["id"]} · {html.escape(s["name"])}</button>' for i,s in enumerate(data))
    figures=''.join(f'<article><h3>{html.escape(title)}</h3><a class="full" data-name="{name}"><img data-name="{name}" alt="{html.escape(title)}; original data, palette preview"></a><p><a class="svg" data-name="{name}">Editable SVG</a> · <a class="pdf" data-name="{name}">Individual PDF</a></p></article>' for name,title,_ in r.EXAMPLES)
    doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Color identity study</title><style>
*{box-sizing:border-box}body{margin:0;background:#FAF6EE;color:#282828;font:16px Helvetica,Arial,sans-serif;line-height:1.55}main{max-width:1420px;margin:auto;padding:38px}h1,h2,h3{font-weight:400;line-height:1.15}h1{font-size:39px;margin:0 0 12px}h2{font-size:28px}h3{font-size:19px}a{color:#68445F;text-underline-offset:3px}nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}button,select{font:inherit;padding:9px 13px;border:1px solid #aaa;background:white;color:#282828;border-radius:4px;cursor:pointer}button[aria-pressed="true"]{background:#282828;color:white;border-color:#282828}button:focus-visible,a:focus-visible,select:focus-visible{outline:3px solid #385A7C;outline-offset:3px}.note{max-width:1080px}.controls{position:sticky;top:0;background:#FAF6EE;z-index:5;padding:4px 0 12px;border-bottom:1px solid #000}#swatches{display:flex;flex-wrap:wrap;gap:15px}.swatch{min-width:125px}.chip{height:44px;border-radius:2px;margin-bottom:5px}.chip+span{font-size:13px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{background:white;border:1px solid #d6d0c6;border-radius:7px;padding:17px}article img{width:100%;display:block}article:nth-child(1),article:nth-child(2),article:nth-child(5),article:nth-child(6){grid-column:1/-1}#profile{width:100%;background:white}.meta{font-size:13px;color:#555}#status{font-size:13px}summary{cursor:pointer}footer{border-top:1px solid;margin-top:30px;padding-top:16px}@media(max-width:800px){main{padding:20px}.grid{display:block}article{margin-bottom:20px}.controls{position:static}h1{font-size:31px}}
</style><main><h1>Five color directions for a research identity</h1><p class="note">Original palette proposals informed by editorial graphics, scientific publishing, architecture, textiles and printmaking. Same Helvetica Regular, cream B <code>#FAF6EE</code>, black frames and thin strokes throughout.</p><p><a href="palette-study.pdf">Research + visual comparison PDF</a> · <a href="README.md">Research notes and exact hex values</a> · <a href="palettes.json">Reusable palette definitions</a></p><div class="controls"><nav>BUTTONS</nav><label for="vision">Preview: </label><select id="vision"><option value="normal">Original color</option><option value="protan">Protan simulation</option><option value="deutan">Deutan simulation</option><option value="tritan">Tritan simulation</option><option value="gray">Grayscale</option></select> <span id="status" aria-live="polite"></span></div><h2 id="name"></h2><p id="idea" class="note"></p><div id="swatches"></div><p id="recommendation" class="note"></p><p class="meta" id="caution"></p><p><a id="gallery-pdf">All six figures in this palette (PDF)</a></p><details open id="profile-block"><summary>Palette profile: lines, labeled comparison and prototype heatmaps</summary><img id="profile" alt="Palette profile with exact swatches and four plotting examples"></details><h2>Six original examples</h2><p class="meta">Original arrays, uncertainty values and axes. New proposals add marker and dash distinctions. The source comparison bars retain truncated axes; the profile uses a labeled point-and-interval alternative. The sphere and original assembled composites are excluded.</p><div class="grid">FIGURES</div><footer><p>My recommendation: <strong>P2 Aubergine &amp; Brass</strong>. P3 is a warmer alternative; P5 brings more graphic energy. The approved default has not been replaced.</p><p class="meta">“Distinctive” is a design judgment, not measured rarity across science. Simulations are approximate screening aids; seven/nine-color sets are not certified colorblind-safe. PDF/SVG links always contain original colors. Only profile heatmaps use synthetic data.</p><p class="meta">Data and original drawings: <a href="https://github.com/ChenLiu-1996/figures4papers">Chen Liu / figures4papers</a>, CC BY-NC 4.0. Research sources and reproduction details are in the notes.</p></footer></main><script>
const schemes=DATA;let selected=2;const vision=document.getElementById('vision');function update(){const s=schemes[selected],mode=vision.value,base=selected===0?'../figures/':s.slug+'/',imgbase=mode==='normal'?base:'simulations/'+s.id+'/'+mode+'/';document.getElementById('name').textContent=s.id+' · '+s.name;document.getElementById('idea').textContent=s.idea;document.getElementById('recommendation').textContent=s.use;document.getElementById('caution').textContent=s.caution;document.getElementById('swatches').innerHTML=s.colors.map((c,i)=>'<div class="swatch"><div class="chip" style="background:'+c+'"></div><span>'+((s.names||['Signature','Companion 1','Companion 2'])[i]||'')+'<br>'+c+'</span></div>').join('');document.querySelectorAll('button[data-index]').forEach((b,i)=>b.setAttribute('aria-pressed',i===selected));document.querySelectorAll('img[data-name]').forEach(im=>im.src=imgbase+im.dataset.name+'.png');document.querySelectorAll('.full').forEach(a=>a.href=imgbase+a.dataset.name+'.png');document.querySelectorAll('.svg').forEach(a=>a.href=base+a.dataset.name+'.svg');document.querySelectorAll('.pdf').forEach(a=>a.href=base+a.dataset.name+'.pdf');document.getElementById('gallery-pdf').href=selected===0?'../gallery-beige.pdf':s.slug+'/gallery.pdf';document.getElementById('profile-block').hidden=selected===0;document.getElementById('profile').src=selected===0?'comparison.png':s.slug+'/profile.png';document.getElementById('status').textContent=(mode==='normal'?'Original colors.':'Simulation applies to the six plots below; swatches/profile stay in original color.');}document.querySelectorAll('button[data-index]').forEach(b=>b.addEventListener('click',()=>{selected=+b.dataset.index;update()}));vision.addEventListener('change',update);update();
</script></html>'''
    (OUT/'gallery.html').write_text(doc.replace('BUTTONS',buttons).replace('FIGURES',figures).replace('DATA',json.dumps(data)))

def simulations():
    from PIL import Image
    for s in [dict(id='Current',slug=None)]+SCHEMES:
        source=ROOT/'figures' if s['slug'] is None else OUT/s['slug']
        for name,_,_ in r.EXAMPLES:
            with Image.open(source/f'{name}.png') as image:
                image=image.convert('RGB');image.thumbnail((1650,1250))
                rgb=np.asarray(image,dtype=float)/255
                for mode in ('protan','deutan','tritan','gray'):
                    dest=OUT/'simulations'/s['id']/mode;dest.mkdir(parents=True,exist_ok=True)
                    Image.fromarray(np.uint8(np.round(simulate(rgb,mode)*255))).save(dest/f'{name}.png')

def main():
    OUT.mkdir(exist_ok=True);theme.apply_theme()
    protected=[ROOT/'gallery.pdf',ROOT/'gallery-beige.pdf',ROOT/'data.json']
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    originals={}
    for name,_,render in r.EXAMPLES:
        f=render();originals[name]=geometry(f);plt.close(f)
    audits={s['id']:audit(s,BASE.background) for s in SCHEMES}
    definitions=[];rendered=[]
    for s in SCHEMES:
        dest=OUT/s['slug'];dest.mkdir(exist_ok=True)
        with use_scheme(s):
            with PdfPages(dest/'gallery.pdf',metadata={'Title':s['id']+' '+s['name']+' - six original examples','Author':'Palette study; original figures by Chen Liu'}) as pdf:
                for name,title,render in r.EXAMPLES:
                    fig=render();mark_redundantly(fig);figure_checks(fig,originals[name]);fig.canvas.draw()
                    for ext in ('png','pdf','svg'):fig.savefig(dest/f'{name}.{ext}',dpi=300)
                    pdf.savefig(fig);plt.close(fig);rendered.append(s['id']+'/'+name)
            definitions.append({**s,'theme':asdict(theme.T),'assignments':palette(s),
                'category_mappings':{group:list(zip(names,palette(s)[group])) for group,names in [
                    ('methods',list(r.post.data_posttraining['methods'])),
                    ('comparison',list(r.raw.data_comparison_IEDB['methods'])),
                    ('composition',list(r.brute.data_brute_force_math['methods']))]},
                'sequential_rgb':ramp(s).tolist(),'diverging_rgb':ramp(s,True).tolist()})
        print('Rendered '+s['id']+' '+s['name'],flush=True)
    theme.apply_theme()
    with PdfPages(OUT/'palette-study.pdf',metadata={'Title':'Five original color identities for scientific plots','Author':'Plotting resources research study'}) as report:
        fig=comparison();report.savefig(fig);fig.savefig(OUT/'comparison.pdf');fig.savefig(OUT/'comparison.png',dpi=160);plt.close(fig)
        for make in (research_pages,domain_page):
            fig=make();report.savefig(fig);plt.close(fig)
        for i,s in enumerate(SCHEMES):
            with use_scheme(s):
                fig=profile(s,i+4);report.savefig(fig);fig.savefig(OUT/s['slug']/'profile.png',dpi=160);plt.close(fig)
        fig=quality_page(audits);report.savefig(fig);fig.savefig(OUT/'readability.png',dpi=160);plt.close(fig)
        for fig in reference_pages():report.savefig(fig);plt.close(fig)
    simulations();write_docs(audits);write_html()
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    assert theme.T==BASE and theme.PALETTES==BASE_PALETTES
    (OUT/'palettes.json').write_text(json.dumps({'font':theme.FONT,'background':BASE.background,'proposals':definitions},indent=2)+'\n')
    (OUT/'sources.json').write_text(json.dumps({'accessed':'2026-11-15','sources':SOURCES},indent=2)+'\n')
    (OUT/'validation.json').write_text(json.dumps({'font':theme.FONT,'background':BASE.background,'rendered':rendered,
        'source_geometry_equal':True,'approved_exports_unchanged':before,'opaque_contrast_target':3,
        'cvd_model':'Machado et al. 2009, severity 100, linear sRGB','close_pair_flag_oklab':.06,
        'close_pair_flag_is_editorial_heuristic':True,'schemes':audits},indent=2)+'\n')
    print('Saved report, comparison, 30 native figures and simulation previews.',flush=True)

if __name__=='__main__':main()
