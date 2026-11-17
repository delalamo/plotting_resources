"""Publish the complete selected-style gallery from verified current exports.

Run render_reference_collection.py after changing data or style; then run this
builder. It refuses stale settings and preserves the native chart display size.
Historical cream exports are retained in legacy-beige-gallery/ and figures/.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import hashlib
import json
import shutil
import zipfile
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont
from matplotlib.font_manager import findfont, FontProperties

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'reference-review-10pt'
BOOK = 'gallery-r1-option-a.pdf'
ARCHIVE = SOURCE / 'reference-figures-source.zip'
SETTINGS = json.loads((ROOT / 'selected-style.json').read_text())
STYLE = SETTINGS['style']
RECORDS = json.loads((SOURCE / 'data-and-sources.json').read_text())
BY_ID = {r['id']: r for r in RECORDS}
AUDIT = json.loads((SOURCE / 'validation.json').read_text())
BY_CHECK = {r['id']: r for r in AUDIT['figures']}
GROUPS = [
    ('repository', 'Repository examples', ['P1', 'P2', 'M1', 'M2', 'M3', 'M4']),
    ('references', 'Urban and template references', ['U1', 'U2', 'U3', 'T1', 'T2', 'T3']),
    ('emphasis', 'Blue-and-gray examples', ['H1', 'H2', 'H3', 'H4']),
]


def verify_inputs():
    assert json.loads((SOURCE / 'selected-style.json').read_text()) == SETTINGS
    assert (STYLE['panel'],STYLE['canvas']) == (('#FFFFFF','#FFFFFF') if SETTINGS['rendering']['minimal'] else ('#D8E8F4','#EDF4F9'))
    assert len(RECORDS) == 16 and sum(r['panels'] for r in AUDIT['figures']) == 27
    assert AUDIT['source_data_sha256'] == hashlib.sha256((ROOT / 'data.json').read_bytes()).hexdigest()
    for record in RECORDS:
        check = BY_CHECK[record['id']]
        assert check['base_font'] == 'Arial' and check['base_size_pt'] == 10
        assert check['canvas_color'] == STYLE['canvas'] and check['panel_color'] == STYLE['panel']
        for ext in ['png', 'pdf', 'svg']:
            assert (SOURCE / 'figures' / f'{record["slug"]}.{ext}').is_file()


def gallery():
    sections = []
    manifest = []
    for group_id, title, ids in GROUPS:
        cards = []
        for key in ids:
            r = BY_ID[key]
            path = SOURCE / 'figures' / f'{r["slug"]}.pdf'
            with fitz.open(path) as pdf:
                w, h = pdf[0].rect.width, pdf[0].rect.height
            base = 'reference-review-10pt/figures/' + r['slug']
            links = ' '.join(f'<a href="{base}.{ext}" download>{ext.upper()}</a>' for ext in ['png', 'pdf', 'svg'])
            cards.append(f'''<section class="entry" id="{key}">
<div class="entry-meta"><span>{key} / {w/72:g} in wide / {BY_CHECK[key]['panels']} panel(s)</span><nav aria-label="Downloads for {key}">{links}</nav></div>
<div class="figure-scroll"><figure style="--chart-width:{w*96/72:.6f}px">
<h3>{escape(r['title'])}</h3><p class="subtitle">{escape(r['subtitle'])}</p>
<img loading="lazy" src="{base}.svg" width="{w*96/72:.6f}" height="{h*96/72:.6f}" alt="{escape(r.get('alt', r['title']))}">
<figcaption><p>{escape(r['source'])}</p><p class="notes">{escape(r['notes'])}</p></figcaption>
</figure></div></section>''')
            manifest.append(dict(id=key, group=group_id, title=r['title'], slug=r['slug'],
                native_size_pt=[w, h], css_size_px=[w*96/72, h*96/72],
                panels=BY_CHECK[key]['panels'], files={ext:base+'.'+ext for ext in ['png','pdf','svg']}))
        sections.append(f'<section class="collection" id="{group_id}"><h2>{escape(title)} <span>{len(ids)} figures</span></h2>'+''.join(cards)+'</section>')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Complete figure gallery - R1 / option A</title><style>
*{box-sizing:border-box}body{margin:0;color:#282828;background:#fff;font:11pt/1.5 Arial,sans-serif}
main{max-width:1344px;margin:0 auto;padding:36px 24px}h1{font-size:22pt;line-height:1.2;margin:8px 0 14px}p{margin:0 0 12px}
.eyebrow,.entry-meta{font-size:9pt;color:#666}header>p{max-width:780px}.tokens{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}.tokens span{background:#EDF4F9;padding:7px 12px;font-size:10pt}
a{color:#285F96;text-underline-offset:3px}nav{display:flex;flex-wrap:wrap;gap:20px}.jump{margin-top:18px;padding-top:18px;border-top:1px solid #ddd}
.collection{margin:44px 0}.collection>h2{font-size:17pt;margin:0 0 22px}.collection>h2>span{font-size:10pt;color:#666;font-weight:400;margin-left:12px}
.entry{margin:0 0 38px}.entry-meta{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin:0 0 10px}
.entry-meta nav{gap:16px}.figure-scroll{overflow-x:auto;max-width:100%}figure{background:#EDF4F9;width:calc(var(--chart-width) + 48px);padding:18px 24px;margin:0 auto;font:10pt/1.3 Arial,sans-serif}
figure h3{font-size:10pt;line-height:1.3;margin:0 0 3pt;font-weight:700}figure .subtitle{margin:0 0 6pt}figure img{display:block;width:var(--chart-width);max-width:none;height:auto}
figcaption{margin-top:7.5pt;font:8pt/1.3 Arial,sans-serif}figcaption p{margin:0}figcaption .notes{margin-top:6pt;color:#666}footer{border-top:1px solid #ddd;padding-top:20px;font-size:9pt;color:#666}
@media(max-width:700px){main{padding:24px 12px}.collection>h2{font-size:15pt}figure{margin:0}h1{font-size:20pt}}
</style></head><body><main><header><div class="eyebrow">FIGURES FOR PAPERS / SELECTED STYLE</div>
<h1>The complete figure gallery</h1><p>All 16 current examples, including the six retained repository figures, six Urban/template references and four blue-and-gray plots. The selected backgrounds, R1 colors, 10 pt Arial with 8 pt source/notes, bold titles and below-plot legends are applied throughout.</p>
<div class="tokens"><span>Plot #D8E8F4</span><span>Figure #EDF4F9</span><span>10 pt Arial / 8 pt source + notes</span><span>1.25 pt data lines</span><span>0.45 pt frames</span></div>
<nav><a href="gallery-r1-option-a.pdf">Complete PDF</a><a href="reference-review-10pt/reference-figures-source.zip">All figures and source code</a><a href="README.md">Style guide</a><a href="article-context/article-context.html">All figures in article context</a></nav>
<nav class="jump"><a href="#repository">Repository (6)</a><a href="#references">Urban and templates (6)</a><a href="#emphasis">Blue and gray (4)</a></nav>
<p style="margin-top:16px;font-size:9pt;color:#666">Charts retain their native width: 6.25 in for single references and 13 in for wide repository figures. View at 100% zoom to assess type size. Wide figures scroll on narrow displays. The PDF also preserves native scale.</p></header>
'''+''.join(sections)+'''<footer><p>Original values, supplied uncertainties and source credits are retained. Synthetic examples are labeled. Mathematical symbols use the documented STIX fallback; math-heavy SVGs outline glyphs for portability.</p>
<p>The sphere and manually assembled composites remain excluded. Earlier palette studies are historical comparisons; the current style is documented in the linked guide.</p></footer></main></body></html>'''
    if SETTINGS['rendering']['minimal']:
        import re
        page=re.sub(r'<h3>.*?</h3><p class="subtitle">.*?</p>', '',page,flags=re.S)
        page=re.sub(r'<figcaption>.*?</figcaption>', '',page,flags=re.S)
        page=page.replace('All figures and source code','All figures and source code (credits in metadata)')
        page=page.replace('Plot #D8E8F4','Plot #FFFFFF').replace('Figure #EDF4F9','Figure #FFFFFF')
        page=page.replace('10 pt Arial / 8 pt source + notes','10 pt Arial / captions omitted')
    (ROOT / 'gallery.html').write_text(page)
    (ROOT / 'gallery-manifest.json').write_text(json.dumps(dict(style_id='R1',background_option='A',
        plot_background=STYLE['panel'],figure_background=STYLE['canvas'],font='Arial',font_pt=10,
        figure_count=16,panel_count=27,figures=manifest),indent=2)+'\n')
    return manifest


def overview():
    # Equal-sized review pages preserve one common scale for all chart typography.
    paths=[SOURCE/'previews'/f'page-{i:02}.png' for i in range(2,13)]
    w,h=600,429
    sheet=Image.new('RGB',(1860,1936),'white')
    draw=ImageDraw.Draw(sheet)
    title_font=ImageFont.truetype(findfont(FontProperties(family='Arial',weight='bold')),32)
    label_font=ImageFont.truetype(findfont(FontProperties(family='Arial')),22)
    draw.text((24,20),'Complete gallery / 16 figures / R1 + option A',font=title_font,fill='#282828')
    draw.text((24,65),'Plot #D8E8F4 / Figure #EDF4F9 / Native-size figures in the gallery and PDF',font=label_font,fill='#666666')
    for i,path in enumerate(paths):
        x=12+(i%3)*620;y=116+(i//3)*455
        with Image.open(path) as im:
            im.thumbnail((w,h),Image.Resampling.LANCZOS);sheet.paste(im,(x,y))
    sheet.save(ROOT/'overview.png')


def archive():
    with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED) as z:
        for p in SOURCE.rglob('*'):
            if p.is_file() and p.suffix!='.zip' and 'tmp' not in p.relative_to(SOURCE).parts:
                z.write(p,'figures4papers-minimal/'+p.relative_to(ROOT).as_posix())
        extra=['README.md','text_width.py','figure_height.py','figure-height-baseline.json','selected-style.json','data.json','build_gallery.py','gallery.html',BOOK,'gallery-manifest.json','overview.png',
            'render_reference_collection.py','render_urban_samples.py','render_multipanel_examples.py','render_article_context.py',
            'emphasis-examples/data.json','urban-style-samples/data-and-sources.json','urban-style-samples/sources/StyleGuideGraphs.xlsx',
            'upstream/figure_VIGIL/plot_concept.py','upstream/LICENSE',
            'article-context/article-context.html','article-context/figures-in-article-context.pdf',
            'article-context/all-16-figures-in-article-context.pdf','article-context/README.md','article-context/validation.json']
        extra.extend(['paper_style.py','pyproject.toml','LICENSE'])
        for rel in extra:z.write(ROOT/rel,'figures4papers-minimal/'+rel)
        for path in [*(ROOT/'templates').rglob('*'),*(ROOT/'src').rglob('*')]:
            if path.is_file() and path.suffix not in ('.zip','.pyc') and '__pycache__' not in path.parts:
                z.write(path,'figures4papers-minimal/'+path.relative_to(ROOT).as_posix())


def verify_outputs(manifest):
    class Parser(HTMLParser):
        def __init__(self):super().__init__();self.links=[];self.images=[];self.ids=[]
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if 'id' in a:self.ids.append(a['id'])
            if tag=='a':self.links.append(a.get('href',''))
            if tag=='img':self.images.append(a)
    p=Parser();p.feed((ROOT/'gallery.html').read_text())
    assert len(p.images)==16 and len(set(p.ids))==len(p.ids)
    for href in p.links:
        if href.startswith('#'):assert href[1:] in p.ids
        elif not href.startswith('http'):assert (ROOT/href).is_file(),href
    for im,r in zip(p.images,manifest):
        assert im['src']==r['files']['svg']
        assert abs(float(im['width'])-r['css_size_px'][0])<1e-5
        assert abs(float(im['height'])-r['css_size_px'][1])<1e-5
        svg=(ROOT/im['src']).read_text().lower()
        assert STYLE['panel'].lower() in svg and STYLE['canvas'].lower() in svg
    assert (ROOT/BOOK).read_bytes()==(SOURCE/'reference-figures-r1-s3-arial-10pt.pdf').read_bytes()
    assert (ROOT/'gallery.pdf').read_bytes()==(ROOT/BOOK).read_bytes()
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        for rel in ['README.md','selected-style.json','gallery.html',BOOK]:
            assert z.read('figures4papers-minimal/'+rel)==(ROOT/rel).read_bytes()
    report=dict(figures=16,panels=27,native_display_scale_preserved=True,
        links_valid=True,all_three_export_formats=True,selected_style_matches=True,
        pdf_matches_verified_reference_collection=True,source_archive_verified=True)
    (ROOT/'gallery-validation.json').write_text(json.dumps(report,indent=2)+'\n')


def main():
    verify_inputs()
    manifest=gallery()
    shutil.copyfile(SOURCE/'reference-figures-r1-s3-arial-10pt.pdf',ROOT/BOOK)
    shutil.copyfile(ROOT/BOOK,ROOT/'gallery.pdf')
    overview()
    archive()
    verify_outputs(manifest)
    print('Published gallery.html,',BOOK,'and complete source archive: 16 figures / 27 panels.')


if __name__=='__main__':main()
