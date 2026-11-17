"""Urban Institute chart conventions with the selected R1/S3 overrides.

Source workbook is preserved under urban-style-samples/sources. No spreadsheet
software or network is needed to regenerate. PDF chart files contain chart text;
booklet titles, subtitles, sources and notes are separate vector page elements.
"""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/figures4papers-mpl')
import json
import hashlib
import html
import shutil
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import FuncFormatter
import pymupdf as fitz
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'urban-style-samples'
SOURCES = OUT / 'sources'
CHARTS = OUT / 'charts'
PREVIEWS = OUT / 'previews'
TEMP = OUT / 'tmp'
SETTINGS = json.loads((ROOT / 'selected-style.json').read_text())
STYLE = SETTINGS['style']
BLUE, BRICK, GOLD, GREEN = STYLE['palette']['colors'][:4]
BG, INK, MUTED = STYLE['panel'], STYLE['ink'], STYLE['muted']
FONT = SETTINGS['typography']['font']
AXIS_TITLE_WEIGHT = SETTINGS['typography']['axis_title_weight']
SMALL = SETTINGS['typography']['ticks_legends_pt']
TITLE = SETTINGS['typography']['titles_pt']
GUIDE = 'https://urbaninstitute.github.io/graphics-styleguide/'
WORKBOOK_URL = GUIDE + 'StyleGuideGraphs.xlsx'
UPSTREAM = 'https://github.com/ChenLiu-1996/figures4papers'
CHART_W, CHART_H = 6.25, 4.35
PAGE_W, PAGE_H = 7.25, 7.5
DASHES = [(0, (4, 2)), (0, (2, 2)), (0, (6, 2, 1, 2)), (0, (1, 2)), (0, (5, 2, 2, 2))]
CHECKS = []


def setup():
    for folder in [OUT, SOURCES, CHARTS, PREVIEWS, TEMP]:
        folder.mkdir(parents=True, exist_ok=True)
    for src, dst in [('/private/tmp/urban-style-examples.xlsx', 'StyleGuideGraphs.xlsx'),
                     ('/private/tmp/urban-bar.png', 'urban-original-bar.png'),
                     ('/private/tmp/urban-paired-bar.png', 'urban-original-paired-bar.png'),
                     ('/private/tmp/urban-line.png', 'urban-original-line.png')]:
        if not (SOURCES / dst).exists():
            shutil.copyfile(src, SOURCES / dst)
    for weight in ('normal', AXIS_TITLE_WEIGHT):
        path=font_manager.findfont(FontProperties(family=FONT,weight=weight),fallback_to_default=False)
        assert font_manager.get_font(path).family_name == FONT
    plt.rcParams.update({
        'font.family': FONT, 'font.weight': 'normal', 'font.size': 10,
        'text.color': INK, 'text.usetex': False, 'text.hinting': 'none', 'axes.labelcolor': INK,
        'axes.labelsize': 10, 'axes.labelweight': AXIS_TITLE_WEIGHT, 'axes.labelpad': 7,
        'axes.titlesize': TITLE, 'axes.titleweight': 'normal',
        'xtick.labelsize': SMALL, 'ytick.labelsize': SMALL,
        'xtick.color': INK, 'ytick.color': INK,
        'xtick.major.pad': 4, 'ytick.major.pad': 4,
        'legend.fontsize': SMALL, 'legend.frameon': False,
        'figure.facecolor': 'white', 'savefig.facecolor': 'white',
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'savefig.dpi': 300, 'mathtext.fontset': 'dejavusans',
        'axes.unicode_minus': True,
    })


def workbook_sheets():
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    result = {}
    with zipfile.ZipFile(SOURCES / 'StyleGuideGraphs.xlsx') as z:
        strings = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rel = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        paths = {e.get('Id'): e.get('Target') for e in rel}
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        for sheet in wb.find('s:sheets', ns):
            rid = sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            cells = {}
            for c in ET.fromstring(z.read('xl/' + paths[rid])).findall('.//s:c', ns):
                val = c.find('s:v', ns)
                if val is not None:
                    cells[c.get('r')] = strings[int(val.text)] if c.get('t') == 's' else float(val.text)
            result[sheet.get('name')] = cells
    return result


def axes(left=.65, right=.12, top=.30, bottom=.56, grid='xy'):
    f = plt.figure(figsize=(CHART_W, CHART_H))
    ax = f.add_axes([left/CHART_W, bottom/CHART_H,
                     (CHART_W-left-right)/CHART_W, (CHART_H-top-bottom)/CHART_H])
    ax.set_facecolor(BG)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_color(STYLE['frame_color']); sp.set_linewidth(STYLE['frame_width'])
    ax.tick_params(length=STYLE['ticks'], width=STYLE['frame_width'])
    ax.grid(False)
    for dim in grid:
        ax.grid(True, axis=dim, color=STYLE['grid_color'], linewidth=STYLE['grid_width'], linestyle=STYLE['grid_style'])
    return f, ax


def bare_bars(ax, labels):
    ax.set_yticks(np.arange(len(labels)), labels)
    ax.set_xticks([])
    ax.tick_params(axis='y', length=0)
    ax.set_ylim(len(labels)-.5, -.5)
    for t in ax.get_yticklabels():
        t.set_ha('right'); t.set_va('center')


def bar_labels(ax, vals, yy, fmt, pad=.35):
    return [ax.text(float(v)+pad, float(y), fmt(v), va='center', ha='left', fontsize=8.5)
            for v, y in zip(vals, yy)]


def plot_line(ax, x, y, color, label, marker=None, dash='-', zorder=3):
    ln, = ax.plot(x, y, color=color, label=label, lw=STYLE['line'], ls=dash,
                  marker=marker, ms=STYLE['marker'], mfc=BG, mec=color,
                  mew=.625, zorder=zorder, alpha=1)
    assert np.array_equal(ln.get_ydata(), y)
    return ln


def make_urban_bars(wb):
    d = wb['BarChart']
    labels = [d[f'A{i}'] for i in range(3, 12)]
    values = np.array([d[f'B{i}'] for i in range(3, 12)]) * 100
    display = [s.replace('Elementary and second education', 'Elementary and secondary\neducation')
               .replace('Housing and community development', 'Housing and community\ndevelopment') for s in labels]
    f, ax = axes(left=2.04, right=.10, top=.10, bottom=.16, grid='')
    colors = ['#979797'] * len(labels); colors[1] = BLUE
    ax.barh(np.arange(9), values, height=STYLE['bar_width'], color=colors, edgecolor=colors, linewidth=STYLE['bar_edge'])
    bare_bars(ax, display); ax.set_xlim(0, 27)
    bar_labels(ax, values, range(9), lambda v: f'{v:.1f}%')
    return f, dict(labels=labels, values=values.tolist(), unit='percent')


def make_urban_paired(wb):
    d = wb['PairedBarChart']; labels = [d[f'A{i}'] for i in range(4, 8)]
    a = np.array([d[f'B{i}'] for i in range(4, 8)])*100
    b = np.array([d[f'C{i}'] for i in range(4, 8)])*100
    # Each individual bar retains .70 width in category units; groups are 2.2 units apart.
    f, ax = axes(left=1.08, right=.10, top=.58, bottom=.15, grid='')
    y = np.arange(4)*2.2
    ax.barh(y-.35, a, height=.70, color=BRICK, edgecolor=BRICK, linewidth=.35)
    ax.barh(y+.35, b, height=.70, color=BLUE, edgecolor=BLUE, linewidth=.35)
    ax.set_yticks(y, [s.replace('Identity not listed','Identity\nnot listed') for s in labels])
    ax.set_ylim(y[-1]+1.05, -1.05); ax.set_xlim(0, 28); ax.set_xticks([])
    ax.tick_params(axis='y', length=0)
    bar_labels(ax, a, y-.35, lambda v:f'{v:.1f}%')
    bar_labels(ax, b, y+.35, lambda v:f'{v:.1f}%')
    ax.legend(handles=[Patch(color=BRICK, label='Trust fund depleted'), Patch(color=BLUE, label='Scheduled benefits paid')],
              loc='lower left', bbox_to_anchor=(0,1.04), ncols=2, borderaxespad=0,
              handlelength=1.1, columnspacing=1.8)
    return f, dict(groups=labels, depleted=a.tolist(), benefits_paid=b.tolist(), unit='percent')


def make_urban_debt(wb):
    d = wb['LineChart']; x = [int(d[f'A{i}']) for i in range(2,27)]
    series = [('C', 'Total home-equity debt', BLUE), ('D','Depository home-equity debt',BRICK),
              ('F','Funded HELOCs',GOLD), ('E','Closed-end second mortgages',GREEN)]
    f, ax = axes(top=.73, left=.67, right=.13)
    lines=[]; data={}
    for col,label,color in series:
        y=[d[f'{col}{i}'] for i in range(2,27)]; data[label]=y
        lines.append(plot_line(ax, x, y, color, label, marker='o'))
    ax.set_xlim(1998.5,2023.5); ax.set_ylim(0,1400)
    ax.set_xticks([2000,2005,2010,2015,2020,2023]); ax.set_yticks(np.arange(0,1401,200))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y,p:f'{y:,.0f}'))
    ax.legend(handles=[lines[i] for i in [0,2,1,3]], loc='lower left', bbox_to_anchor=(0,1.025),
              ncols=2, borderaxespad=0, handlelength=1.65, columnspacing=1.4, labelspacing=.6)
    return f, dict(years=x, series=data, unit='USD billions',
                  correction='Dates use workbook column A. The source image repeats 2022 at its last tick; column A identifies that observation as 2023.')


def make_ours_training(data):
    d = data['posttraining']; x=d['steps']
    f, ax = axes(left=.58, right=1.00, top=.16)
    ax.set_xlim(-20,820); ax.set_ylim(0,65); ax.set_xticks(x); ax.set_yticks([0,20,40,60])
    ax.set_xlabel('Post-training steps')
    labels=['DPO','DA-DPO','VIGIL (ours)']
    for label,y,c in zip(labels,d['results'],[BRICK,GOLD,BLUE]):
        plot_line(ax,x,y,c,label,marker='o')
        ax.text(1.025,y[-1],label,transform=ax.get_yaxis_transform(),ha='left',va='center',
                color=BLUE if c==BLUE else INK,fontsize=SMALL,clip_on=False)
    plot_line(ax,x,[22.]*5,'#979797','SFT only',dash=(0,(4,2)),zorder=2)
    ax.text(1.025,22,'SFT only',transform=ax.get_yaxis_transform(),ha='left',va='center',fontsize=SMALL,color=MUTED)
    return f, d


def make_ours_benchmark(data):
    d=data['comparison_IEDB']; vals=np.array(d['mean'])[:,0]; err=np.array(d['std'])[:,0]
    order=np.argsort(-vals,kind='stable')
    names=[d['methods'][i].replace('BigMHC$_\\text{retrained}$','BigMHC retrained') for i in order]
    colors=[BLUE if i==8 else '#979797' for i in order]
    f,ax=axes(left=1.47,right=.10,top=.10,bottom=.16,grid='')
    ax.barh(np.arange(9),vals[order],height=.70,color=colors,edgecolor=colors,linewidth=.35,
            xerr=err[order],error_kw=dict(ecolor=INK,elinewidth=.65,capsize=2,capthick=.65))
    bare_bars(ax,names);ax.set_xlim(0,1.02)
    for j,i in enumerate(order):
        ax.text(vals[i]+err[i]+.014,j,f'{vals[i]:.3f}',ha='left',va='center',fontsize=8.5)
    return f, dict(methods=names,mean=vals[order].tolist(),std=err[order].tolist(),
                  metric='AUROC', original_order_indices=order.tolist(),values_unchanged=True)


def make_ours_emphasis(emphasis):
    d=next(x for x in emphasis if x['id']=='H2')
    f,ax=axes(left=.58,right=1.21,top=.16)
    x=d['x'];grays=[f'#{v:02x}{v:02x}{v:02x}' for v in np.rint(np.linspace(119,183,5)).astype(int)]
    endlabels=[]
    for i,(ref,c) in enumerate(zip(d['references'],grays)):
        plot_line(ax,x,ref['y'],c,ref['name'],dash=DASHES[i],zorder=2)
        endlabels.append((ref['y'][-1],ref['name'],MUTED))
    plot_line(ax,x,d['focus']['y'],BLUE,d['focus']['name'],zorder=4)
    endlabels.append((d['focus']['y'][-1],'Selected method',BLUE))
    ax.set_xlim(-1,101);ax.set_ylim(45,94);ax.set_xticks(d['xticks']);ax.set_yticks(d['yticks'])
    ax.set_xlabel('Training epoch')
    # Preserve endpoint order, then separate labels by a documented 3.2 data units.
    endlabels.sort()
    label_y=[]
    for y,_,_ in endlabels:label_y.append(max(y,label_y[-1]+3.2 if label_y else y))
    if label_y[-1]>92:
        shift=label_y[-1]-92;label_y=[v-shift for v in label_y]
    for (y,name,c),yy in zip(endlabels,label_y):
        ax.annotate(name,xy=(100,y),xycoords='data',xytext=(1.045,yy),textcoords=ax.get_yaxis_transform(),
                    ha='left',va='center',color=c,fontsize=SMALL,annotation_clip=False,
                    arrowprops=dict(arrowstyle='-',color=c,lw=.45,shrinkA=3,shrinkB=2))
    return f,d


def wrap(text, width_pt, size):
    # Font-aware wrapping in physical units, independent of raster resolution.
    from matplotlib.backends.backend_agg import RendererAgg
    renderer=RendererAgg(10,10,72)
    props=FontProperties(family=FONT,size=size)
    result=[]
    for para in text.split('\n'):
        line=''
        for word in para.split():
            candidate=(line+' '+word).strip()
            if line and renderer.get_text_width_height_descent(candidate,props,ismath=False)[0]>width_pt:
                result.append(line);line=word
            else:line=candidate
        result.append(line)
    return '\n'.join(result)


def page_text(f, x, top, text, size, color=INK, width=450, linespacing=1.35, url=None):
    t=f.text(x/(PAGE_W*72),1-top/(PAGE_H*72),wrap(text,width,size),fontsize=size,
             ha='left',va='top',color=color,linespacing=linespacing)
    if url:t.set_url(url)
    return t


def validate_chart(f, spec):
    f.canvas.draw();renderer=f.canvas.get_renderer()
    problems=[]
    for txt in f.findobj(matplotlib.text.Text):
        if not txt.get_visible() or not txt.get_text():continue
        box=txt.get_window_extent(renderer)
        if box.x0 < -1 or box.y0 < -1 or box.x1>f.bbox.width+1 or box.y1>f.bbox.height+1:
            problems.append(txt.get_text())
    assert not problems,(spec['slug'],problems)
    ax=f.axes[0]
    assert all(sp.get_visible() and sp.get_linewidth()==.45 for sp in ax.spines.values())
    assert np.allclose(ax.get_facecolor()[:3],matplotlib.colors.to_rgb(BG))
    for label in (ax.xaxis.label,ax.yaxis.label):
        if label.get_text():
            assert label.get_fontweight()==AXIS_TITLE_WEIGHT
            assert label.get_fontfamily()==[FONT]
    if 'bar' in spec['slug']:assert ax.get_xlim()[0]==0
    CHECKS.append(dict(id=spec['id'],slug=spec['slug'],physical_width_inches=CHART_W,
                       text_within_canvas=True,font=FONT,axis_title_weight=AXIS_TITLE_WEIGHT,
                       frame_width_pt=.45,background=BG,
                       axis_starts_at_zero=bool(ax.get_xlim()[0]==0) if 'bar' in spec['slug'] else None))


def make_page(spec, chart_path, number):
    f=plt.figure(figsize=(PAGE_W,PAGE_H))
    page_text(f,36,20,f'FIGURE {number}  /  '+spec['group'].upper(),8,BLUE)
    page_text(f,36,40,spec['title'],TITLE)
    page_text(f,36,63,spec['subtitle'],10)
    source=page_text(f,36,425,spec['source'],8,width=450,url=spec['url'])
    source_lines=source.get_text().count('\n')+1
    notes_top=425+source_lines*10.8+6
    notes=page_text(f,36,notes_top,spec['notes'],8,MUTED,width=450)
    rule_top=notes_top+(notes.get_text().count('\n')+1)*10.8+9
    page_text(f,36,rule_top,spec['rule'],8,MUTED,width=450)
    assert rule_top+(wrap(spec['rule'],450,8).count('\n')+1)*10.8<516
    page_text(f,36,526,'URBAN CONVENTIONS  /  R1 COLORS  /  S3 BACKGROUND  /  ARIAL',7,MUTED)
    page_text(f,477,526,f'{number:02}',7,MUTED,width=15)
    path=TEMP/f'{spec["slug"]}-page.pdf';f.savefig(path);plt.close(f)
    page=fitz.open(path)
    with fitz.open(chart_path) as chart:
        page[0].show_pdf_page(fitz.Rect(36,100,486,100+CHART_H*72),chart,0)
    return page


def make_intro():
    f=plt.figure(figsize=(PAGE_W,PAGE_H))
    page_text(f,36,27,'SAMPLE COLLECTION  /  15 NOVEMBER 2026',8,BLUE)
    page_text(f,36,60,'Urban Layout, Our Visual Identity',18)
    page_text(f,36,96,'Three examples from Urban Institute, followed by three from our templates.',11)
    page_text(f,36,144,'Retained decisions',11)
    page_text(f,36,168,'Arial Regular with bold axis titles; R1 cobalt, brick and gold; S3 panels; thin four-sided frames; existing line, marker and font sizes. The blue-and-gray emphasis mode is included.',10)
    swatches=[(BLUE,'Cobalt'),(BRICK,'Brick'),(GOLD,'Gold'),(BG,'Panel'),('#979797','Context')]
    for i,(c,label) in enumerate(swatches):
        x=36+i*91
        f.add_artist(Rectangle((x/(PAGE_W*72),1-244/(PAGE_H*72)),70/(PAGE_W*72),24/(PAGE_H*72),
                               transform=f.transFigure,facecolor=c,edgecolor=STYLE['frame_color'],lw=.45))
        page_text(f,x,253,label,8)
        page_text(f,x,267,c,8,MUTED)
    page_text(f,36,308,'Urban conventions applied',11)
    page_text(f,36,332,'Charts are 6.25 inches wide. Titles, subtitles, sources and notes sit outside the chart artwork. Bars start at zero. Directly labeled bars omit numeric axes and gridlines. Line labels replace legends where they fit; other legends sit above the plot.',10)
    page_text(f,36,420,'Exact values, disclosed adaptations',11)
    page_text(f,36,443,'Urban data come from its downloadable example workbook. Existing benchmark data are unchanged. The final learning-curve example remains synthetic. This is a sample treatment, not a replacement of the selected guide.',9)
    page_text(f,36,509,'Reference: urbaninstitute.github.io/graphics-styleguide/',8,BLUE,url=GUIDE)
    path=TEMP/'intro.pdf';f.savefig(path);plt.close(f);return fitz.open(path)


RULE_ROWS=[
    ('Typography','Arial Regular; axis titles use Arial Bold. Sizes remain 11.43 / 10 / 8.57 pt for plot titles / axis titles / ticks and legends. Figure numbers and notes are 8 pt; direct bar values are 8.5 pt.'),
    ('Palette and emphasis','Keep R1 category colors and S3 #EBF1F5. The emphasis example retains cobalt, five neutral grays, equal 1.25 pt strokes, dashed references and blue drawn last.'),
    ('Frame, grid and marks','Keep the .45 pt frame, .45 pt dotted grid, 3.5 pt open markers, .70 bar width, .35 pt bar edges and .65 pt error bars with 2 pt caps. Omit grids on directly labeled bars.'),
    ('Labels and arrangement','Apply Urban\'s title/sentence capitalization, zero-based bars, right-aligned horizontal categories, above-chart legends and direct series labels where feasible.'),
    ('Output and spacing','Chart width is Urban\'s 6.25 in print width. The 4.35 in chart height, .5 in page margins, label clearances and annotation routing are local layout choices where the guide gives no exact measurement.'),
    ('Data and identity','U1 expands a shortened education label. U3 uses the actual 2023 year from column A, correcting the repeated 2022 tick in the source image. No Urban logo is used on these adapted figures.'),
]


def make_rules():
    f=plt.figure(figsize=(PAGE_W,PAGE_H))
    page_text(f,36,25,'SPECIFICATION NOTES',8,BLUE)
    page_text(f,36,50,'What Was Retained and What Was Applied',16)
    y=89
    for title,body in RULE_ROWS:
        page_text(f,36,y,title,10,BLUE)
        t=page_text(f,36,y+18,body,9)
        y+=18+(t.get_text().count('\n')+1)*12.15+17
    assert y<521,y
    page_text(f,36,526,'Urban rules plus the explicit R1/S3 exceptions above; no claim of Urban authorship.',7,MUTED)
    path=TEMP/'rules.pdf';f.savefig(path);plt.close(f);return fitz.open(path)


def write_gallery(specs):
    cards=[]
    for s in specs:
        original=f'<a href="sources/{s["original"]}">Urban original</a>' if s.get('original') else f'<a href="{s["previous"]}">Previous template</a>'
        cards.append(f'''<article id="{s['id']}"><p class="eyebrow">{s['id']} / {html.escape(s['group'])}</p>
<h2>{html.escape(s['short'])}</h2><a href="previews/{s['slug']}.png"><img src="previews/{s['slug']}.png" alt="{html.escape(s['alt'])}"></a>
<p>{html.escape(s['rule'])}</p><nav>{original}<a href="charts/{s['slug']}.svg">SVG</a><a href="charts/{s['slug']}.pdf">Chart PDF</a><a href="{s['url']}">Data source</a></nav></article>''')
    content='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Urban layout, R1 / S3 identity</title>
<style>*{box-sizing:border-box}body{margin:0;background:#fff;color:#282828;font:16px/1.5 Arial,Helvetica,sans-serif}main{max-width:1440px;margin:auto;padding:38px 30px}h1,h2{font-weight:400}h1{font-size:34px;margin:0 0 12px}h2{font-size:22px;margin:6px 0 10px}a{color:#285F96}p{max-width:980px}header{padding-bottom:26px;border-bottom:1px solid #CBD6DF}nav{display:flex;gap:18px;flex-wrap:wrap;font-size:14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:30px}.eyebrow{font-size:12px;letter-spacing:.08em;color:#566C7B;margin:0}article{margin-top:28px;min-width:0}img{display:block;width:100%;border:1px solid #CBD6DF}article>p:not(.eyebrow){font-size:14px;color:#666}.notice{padding:16px 20px;background:#EBF1F5;max-width:1100px}footer{border-top:1px solid #CBD6DF;margin-top:40px;padding-top:20px;font-size:14px}@media(max-width:850px){.grid{grid-template-columns:1fr}main{padding:24px 18px}h1{font-size:27px}}</style>
<main><header><h1>Urban layout, our visual identity</h1><p>Three Urban Institute examples and three existing templates, with Arial, bold axis titles, R1 colors and the S3 background.</p>
<p class="notice">These samples apply Urban's documented conventions with the explicit exceptions listed in the specification notes. Chart dimensions and text remain measurable at export size. Arial and bold axis titles are the current typography settings.</p>
<nav><a href="urban-r1-samples.pdf">Eight-page PDF booklet</a><a href="urban-r1-samples.zip">Native charts and source code</a><a href="README.md">Specification notes</a></nav></header><div class="grid">'''
    content+='\n'.join(cards)+'''</div><footer><p>Urban examples use its published workbook. Template examples retain the source arrays; U3 corrects a year-label error in the original workbook chart. T3 is synthetic. Titles, sources and notes are separate from the downloadable chart artwork.</p><a href="https://urbaninstitute.github.io/graphics-styleguide/">Urban Institute guide</a></footer></main></html>'''
    (OUT/'gallery.html').write_text(content)


def main():
    setup();wb=workbook_sheets();data=json.loads((ROOT/'data.json').read_text())
    emphasis=json.loads((ROOT/'emphasis-examples/data.json').read_text())
    specs=[
        dict(id='U1',slug='urban-spending-bars',group='Urban example',short='Spending priorities',
             title='Education Accounts for One-Fifth of State and Local Spending',
             subtitle='Share of total spending by function, fiscal year 2021',
             source='Source: US Census Bureau state and local finance survey, via Urban Institute; fiscal year 2021.',
             notes='Notes: Selected functions are shown. Government liquor stores, utilities and insurance trusts are excluded. Medicaid spans welfare and health spending.',
             rule='Urban layout: horizontal categories, zero baseline, direct values and no redundant numeric axis or grid.',
             url=WORKBOOK_URL,original='urban-original-bar.png',
             alt='Education is highlighted in cobalt at 20.5 percent; public welfare is highest at 23.4 percent. Seven further spending categories are gray.',builder=lambda:make_urban_bars(wb)),
        dict(id='U2',slug='urban-poverty-paired-bars',group='Urban example',short='Two policy scenarios',
             title='Trust Fund Depletion Raises Projected Poverty Across Groups',
             subtitle='Projected poverty rates under two Social Security scenarios, 2045',
             source='Source: Urban Institute DYNASIM4, run 1004, via its example workbook.',
             notes='Notes: Adults aged 62+ or receiving disability benefits. Black, White and identity-not-listed groups are non-Hispanic; the last includes Asian, Indigenous and multiracial people.',
             rule='Urban layout: paired bars from zero, category order preserved, direct values and an above-chart legend.',
             url='https://www.urban.org/urban-wire/if-social-security-runs-out-money-poverty-among-older-adults-and-people-disabilities',original='urban-original-paired-bar.png',
             alt='Projected poverty rates are higher under trust fund depletion for all four groups. Paired bars compare 16.2 versus 9.9, 24.0 versus 17.8, 6.4 versus 3.5, and 9.3 versus 6.4 percent.',builder=lambda:make_urban_paired(wb)),
        dict(id='U3',slug='urban-home-equity-lines',group='Urban example',short='Home-equity lending',
             title='Home-Equity Debt Rebounds but Remains Below Its Earlier Peak',
             subtitle='Outstanding balances, billions of US dollars, 1999-2023',
             source='Source: Inside Mortgage Finance, via Urban Institute\'s LineChart workbook sheet.',
             notes='Notes: HELOCs are home-equity lines of credit. Years use column A; the final observation is 2023, correcting a repeated 2022 tick in the original chart.',
             rule='Urban layout: four series, an above-chart legend for long names and open circles for near-parallel trajectories.',
             url='https://www.urban.org/urban-wire/freddie-macs-new-second-lien-pilot-first-step-toward-helping-borrowers-cap-too',original='urban-original-line.png',
             alt='Four home-equity debt series rise to peaks around 2007-2009, fall through 2021 and rise again by 2023. Total debt ends at 512.34 billion dollars.',builder=lambda:make_urban_debt(wb)),
        dict(id='T1',slug='template-posttraining-lines',group='Our template',short='Post-training performance',
             title='VIGIL Maintains the Highest Score After Post-Training',
             subtitle='Performance on highly vision-dependent tasks, original benchmark scale',
             source='Source: Chen Liu, figures4papers, figure_VIGIL/plot_posttraining.py (CC BY-NC 4.0).',
             notes='Notes: All five steps and all three method series are unchanged. The SFT reference stays at the shared initial value of 22.',
             rule='Urban layout: series named at their right endpoints; the redundant legend is removed.',url=UPSTREAM,
             previous='../s3-design-study/cobalt-brick-gold/comparison_posttraining.png',
             alt='VIGIL rises from 22 to 58.5, DA-DPO to 40.5 and DPO to 30.2 after 800 steps, above the SFT-only reference at 22.',builder=lambda:make_ours_training(data)),
        dict(id='T2',slug='template-iedb-bars',group='Our template',short='Benchmark comparison',
             title='ImmunoStruct Leads the IEDB AUROC Comparison',
             subtitle='Area under the receiver operating characteristic curve; higher is better',
             source='Source: Chen Liu, figures4papers, figure_ImmunoStruct/raw_data.py (CC BY-NC 4.0).',
             notes='Notes: This sample shows the AUROC metric from the original three-metric template. Means and supplied standard deviations are unchanged; bars show mean +/- SD.',
             rule='Urban layout: bars begin at zero, methods are ranked, long names run horizontally and values are directly labeled.',url=UPSTREAM,
             previous='../s3-design-study/cobalt-brick-gold/bars_comparison_IEDB.png',
             alt='All nine methods are ranked by AUROC on a zero-based scale, with ImmunoStruct highlighted at 0.882 and eight gray comparison bars. Error bars show supplied standard deviations.',builder=lambda:make_ours_benchmark(data)),
        dict(id='T3',slug='template-emphasis-lines',group='Our template',short='A selected curve in context',
             title='A Highlighted Method Can Sit Within the Comparison Group',
             subtitle='Illustrative learning curves; synthetic scores across 100 training epochs',
             source='Source: Our existing H2 learning-curves sample; deterministic illustrative data.',
             notes='Notes: All six series are unchanged. Cobalt identifies the selected method; selection does not indicate the best performance.',
             rule='Urban layout: direct endpoint labels with short leaders; gray comparisons retain distinct dash patterns.',
             url='../emphasis-examples/data.json',previous='../emphasis-examples/learning-curves.png',
             alt='One cobalt selected-method curve and five dashed gray references rise and level off. The selected curve finishes below the best reference, demonstrating emphasis without implying superiority.',builder=lambda:make_ours_emphasis(emphasis)),
    ]
    book=fitz.open();intro=make_intro();book.insert_pdf(intro);intro.close();records=[]
    for i,s in enumerate(specs,1):
        f,values=s['builder']();validate_chart(f,s)
        for ext in ['png','pdf','svg']:f.savefig(CHARTS/f'{s["slug"]}.{ext}',dpi=300)
        plt.close(f)
        page=make_page(s,CHARTS/f'{s["slug"]}.pdf',i)
        page[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(PREVIEWS/f'{s["slug"]}.png')
        book.insert_pdf(page);page.close()
        records.append({k:v for k,v in s.items() if k!='builder'}|{'data':values})
        print('Rendered',s['id'],s['slug'],flush=True)
    rules=make_rules();book.insert_pdf(rules);rules.close()
    book.set_metadata({'title':'Urban layout, R1/S3 identity - six samples','author':'Adapted examples; sources credited per figure'})
    book.save(OUT/'urban-r1-samples.pdf',garbage=4,deflate=True);book.close()
    (OUT/'data-and-sources.json').write_text(json.dumps(records,indent=2)+'\n')
    manifest=dict(reference=GUIDE,workbook=WORKBOOK_URL,workbook_sha256=hashlib.sha256((SOURCES/'StyleGuideGraphs.xlsx').read_bytes()).hexdigest(),
                  chart_width_inches=CHART_W,chart_height_inches=CHART_H,font=FONT,
                  axis_title_weight=AXIS_TITLE_WEIGHT,selected_style='R1 / S3',
                  specs=RULE_ROWS,validation=CHECKS)
    (OUT/'settings-and-validation.json').write_text(json.dumps(manifest,indent=2)+'\n')
    write_gallery(specs)
    readme='# Urban layout samples with R1 / S3\n\n[Gallery](gallery.html) · [PDF booklet](urban-r1-samples.pdf) · [Native charts](charts/)\n\n'
    readme+='These six samples use the selected Arial typography with bold axis titles. U1-U3 reproduce data behind examples in the [Urban Institute guide]('+GUIDE+'). T1-T3 adapt existing templates.\n\n'
    readme+='## Explicit settings and exceptions\n\n'+ '\n\n'.join('**'+a+'.** '+b for a,b in RULE_ROWS)+'\n\n'
    readme+='## Data and provenance\n\nThe original public workbook and reference PNGs are preserved in `sources/`. Every array, source link and adaptation is recorded in `data-and-sources.json`. No data are estimated from pixels. The IEDB sample selects AUROC from the original three metrics and preserves every method and standard deviation. The last example is synthetic.\n\n'
    readme+='Urban typography and color are replaced by the selected settings. The Urban logo is omitted because these are adaptations. Numeric axes and grids are removed on directly labeled bars under Urban\'s bar-chart rule; the selected frame remains. Source and notes are separate from the chart artwork in the booklet.\n\n'
    readme+='## Regenerate\n\n`MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_urban_samples.py`\n\nPython dependencies: Matplotlib, NumPy, PyMuPDF and Pillow. Source arrays from Chen Liu\'s repository remain subject to [CC BY-NC 4.0](../upstream/LICENSE).\n'
    (OUT/'README.md').write_text(readme)
    # A contact sheet of the finished scientific figures, not a new composite data figure.
    thumb_w,thumb_h=870,900
    sheet=Image.new('RGB',(thumb_w*2+60,thumb_h*3+80),'white')
    for i,s in enumerate(specs):
        img=Image.open(PREVIEWS/f'{s["slug"]}.png').convert('RGB')
        img.thumbnail((thumb_w,thumb_h),Image.Resampling.LANCZOS)
        x=20+(i%2)*(thumb_w+20);y=20+(i//2)*(thumb_h+20)
        sheet.paste(img,(x,y))
    sheet.save(OUT/'overview.png')
    with zipfile.ZipFile(OUT/'urban-r1-samples.zip','w',zipfile.ZIP_DEFLATED) as z:
        prefix='figures4papers-minimal/'
        for path in sorted(CHARTS.iterdir()):z.write(path,prefix+'urban-style-samples/charts/'+path.name)
        for name in ['README.md','settings-and-validation.json','data-and-sources.json']:
            z.write(OUT/name,prefix+'urban-style-samples/'+name)
        for name in ['gallery.html','urban-r1-samples.pdf','overview.png']:
            z.write(OUT/name,prefix+'urban-style-samples/'+name)
        for path in sorted(PREVIEWS.iterdir()):z.write(path,prefix+'urban-style-samples/previews/'+path.name)
        z.write(Path(__file__),prefix+'render_urban_samples.py')
        z.write(ROOT/'selected-style.json',prefix+'selected-style.json')
        z.write(ROOT/'data.json',prefix+'data.json')
        z.write(ROOT/'emphasis-examples/data.json',prefix+'emphasis-examples/data.json')
        z.write(ROOT/'upstream/LICENSE',prefix+'upstream/LICENSE')
        for path in sorted(SOURCES.iterdir()):z.write(path,prefix+'urban-style-samples/sources/'+path.name)
        for spec in specs:
            if spec.get('previous'):
                path=(OUT/spec['previous']).resolve()
                z.write(path,prefix+path.relative_to(ROOT).as_posix())
    print('Completed',OUT,flush=True)


if __name__=='__main__':main()
