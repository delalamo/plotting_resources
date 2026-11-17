"""Compare source/note type sizes without changing the approved figure geometry."""
from pathlib import Path
import base64
import hashlib
import html
import json
import matplotlib.pyplot as plt
import pymupdf as fitz
import render_article_context as article

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'note-size-study'
CARDS=OUT/'figures'
TEMP=OUT/'tmp'
BOOK='source-notes-size-comparison.pdf'
SIZES=[6,7,8,10]
EXAMPLES=['T1','U1','M2']
CURRENT=json.loads((OUT/'baseline-article-layout.json').read_text())
BASE={r['figure_id']:r for r in CURRENT['figures']}
AUDIT=[]


def draw_text(f,x,top,body,width,size=10,bold=False,color=article.INK):
    w,h=f.get_size_inches()*72
    t=f.text(x/w,1-top/h,article.wrapped(body,width,size,bold),
             va='top',ha='left',fontsize=size,fontfamily='Arial',
             fontweight='bold' if bold else 'normal',color=color,linespacing=1.3)
    f.canvas.draw()
    return t,h-t.get_window_extent(f.canvas.get_renderer()).y0*72/f.dpi


def filename(key,size):
    return f'{key.lower()}-source-notes-{size}pt'


def make_card(key,size):
    spec=article.RECORDS[key];baseline=BASE[key]
    number=baseline['figure_number']
    w=baseline['card_rect'][2]-baseline['card_rect'][0]
    h=baseline['card_rect'][3]-baseline['card_rect'][1]
    cw,ch=baseline['native_chart_size_pt']
    f=plt.figure(figsize=(w/72,h/72),facecolor=article.CANVAS)
    _,y=draw_text(f,18,13.5,f'Figure {number}. {spec["title"]}',cw,bold=True)
    _,y=draw_text(f,18,y+3,spec['subtitle'],cw)
    chart_top=y+6
    source_top=chart_top+ch+7.5
    source,y=draw_text(f,18,source_top,spec['source'],cw,size=size)
    notes_top=y+6
    notes,y=draw_text(f,18,notes_top,spec['notes'],cw,size=size,color=article.MUTED)
    assert y<=h-13.5+.02,(key,size,'footer overflow',y,h)
    # Only the footer text changes. Keep the approved card and artwork bounds.
    x0,y0,_,_=baseline['card_rect']
    expected=[v-o for v,o in zip(baseline['chart_rect'],[x0,y0,x0,y0])]
    chart_rect=fitz.Rect(18,chart_top,18+cw,chart_top+ch)
    assert max(abs(a-b) for a,b in zip(chart_rect,expected))<.01
    f.canvas.draw();renderer=f.canvas.get_renderer()
    boxes=[t.get_window_extent(renderer) for t in f.texts]
    assert not any(a.overlaps(b) for i,a in enumerate(boxes) for b in boxes[i+1:])
    for t,box in zip(f.texts,boxes):
        assert box.x0>=0 and box.y0>=0 and box.x1<=f.bbox.width and box.y1<=f.bbox.height
        assert t.get_fontfamily()==['Arial']
        assert t.get_fontsize()==(size if t in [source,notes] else 10)
        if t in [source,notes]:assert t.get_fontweight()=='normal'
    bg=TEMP/f'{filename(key,size)}-text.pdf'
    f.savefig(bg,facecolor=article.CANVAS);plt.close(f)
    doc=fitz.open(bg)
    chart_path=article.SOURCE/'figures'/f'{spec["slug"]}.pdf'
    with fitz.open(chart_path) as chart:doc[0].show_pdf_page(chart_rect,chart,0)
    pdf=CARDS/f'{filename(key,size)}.pdf'
    doc.save(pdf,garbage=4,deflate=True)
    # Outline text for a portable web comparison using the exact PDF artwork.
    (CARDS/f'{filename(key,size)}.svg').write_text(doc[0].get_svg_image(text_as_path=True))
    record=dict(figure_id=key,source_notes_font_pt=size,card_size_pt=[w,h],
        chart_rect_pt=list(chart_rect),source_top_pt=source_top,notes_top_pt=notes_top,
        notes_bottom_pt=y,bottom_padding_pt=h-y,figure_height_factor=.75,
        chart_sha256=hashlib.sha256(chart_path.read_bytes()).hexdigest(),
        other_figure_text_pt=10,footer_bold=False,text_overlaps=0)
    AUDIT.append(record)
    doc.close()
    return record


def overview():
    f=plt.figure(figsize=(15,12),facecolor='white')
    draw_text(f,36,26,'Source and notes: choose a text size',1008,size=18,bold=True)
    draw_text(f,36,54,'Same figure, at the approved 75% height. Only the source and notes change size.',1008,size=10)
    draw_text(f,36,72,'Arial throughout. Titles, axes, ticks and legends remain 10 pt. Compare at 100% zoom.',1008,size=10,color=article.MUTED)
    placements=[]
    for i,size in enumerate(SIZES):
        x=36+(i%2)*522;top=103+(i//2)*367
        label=f'{chr(65+i)}  /  {size} pt'+('  /  current reference' if size==10 else '')
        draw_text(f,x,top,label,486,size=11,bold=True)
        w,h=BASE['T1']['card_rect'][2]-BASE['T1']['card_rect'][0],BASE['T1']['card_rect'][3]-BASE['T1']['card_rect'][1]
        placements.append((size,fitz.Rect(x,top+22,x+w,top+22+h)))
    draw_text(f,36,838,'Following pages show 6, 7 and 8 pt in lorem ipsum context: line, bar and multi-panel examples.',1008,size=9,color=article.MUTED)
    path=TEMP/'overview-text.pdf';f.savefig(path,facecolor='white');plt.close(f)
    doc=fitz.open(path)
    for size,rect in placements:
        with fitz.open(CARDS/f'{filename("T1",size)}.pdf') as card:doc[0].show_pdf_page(rect,card,0)
    return doc


def article_page(key,size,page_number):
    original_base=article.base_page;original_card=article.card;original_temp=article.TEMP
    def base(number):
        f=original_base(number)
        for t in f.texts:
            if t.get_text()=='COLOR CONTEXT PROOF':t.set_text(f'SOURCE + NOTES: {size} PT')
            if t.get_text()==f'{number:02}':t.set_text(f'{page_number:02}')
        return f
    def card(f,spec,number,top):
        b=BASE[key];w=b['card_rect'][2]-b['card_rect'][0];h=b['card_rect'][3]-b['card_rect'][1]
        x=(article.PAGE_W-w)/2;rect=fitz.Rect(x,top,x+w,top+h)
        return top+h,(CARDS/f'{filename(key,size)}.pdf',rect),dict(figure_id=key,
            source_notes_font_pt=size,card_rect=list(rect),native_scale=1.0)
    try:
        article.base_page=base;article.card=card;article.TEMP=TEMP
        doc,record=article.page(article.RECORDS[key],BASE[key]['figure_number'])
    finally:
        article.base_page=original_base;article.card=original_card;article.TEMP=original_temp
    assert max(abs(x-y) for x,y in zip(record['card_rect'],BASE[key]['card_rect']))<.01
    return doc


def verify_pdf():
    with fitz.open(OUT/BOOK) as doc:
        assert len(doc)==10
        for page in doc:
            for font in page.get_fonts():assert doc.extract_font(font[0])[-1]
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        assert page.rect.contains(fitz.Rect(span['bbox'])),span
                        assert span['font'] in ['ArialMT','Arial-BoldMT','Arial-ItalicMT','STIXGeneral-Regular','STIXNonUnicode-Italic'],span
    for record in AUDIT:
        key=record['figure_id'];size=record['source_notes_font_pt']
        with fitz.open(CARDS/f'{filename(key,size)}.pdf') as doc:
            spans=[s for b in doc[0].get_text('dict')['blocks'] for line in b.get('lines',[]) for s in line['spans']]
            footer=[s for s in spans if s['bbox'][1]>=record['source_top_pt']-2]
            assert footer,(key,size)
            assert all(abs(s['size']-size)<.001 and s['font']=='ArialMT' for s in footer),(key,size,footer)


def write_html():
    data={key:{} for key in EXAMPLES}
    for key in EXAMPLES:
        for size in SIZES:
            data[key][size]='data:image/svg+xml;base64,'+base64.b64encode((CARDS/f'{filename(key,size)}.svg').read_bytes()).decode()
    rows=[]
    for key in EXAMPLES:
        b=BASE[key];w=(b['card_rect'][2]-b['card_rect'][0])*96/72;h=(b['card_rect'][3]-b['card_rect'][1])*96/72
        rows.append(f'''<section><div class="reading"><h2>{html.escape(article.SECTIONS[key])}</h2>
<p>{article.PARAGRAPHS[0]}</p></div><div class="scroll"><img data-figure="{key}" width="{w:.5f}" height="{h:.5f}" alt="{html.escape(article.RECORDS[key]['title'])}"></div>
<div class="reading"><p>{article.PARAGRAPHS[1]}</p></div></section>''')
    footer=[]
    for size in SIZES:
        record=next(r for r in AUDIT if r['figure_id']=='T1' and r['source_notes_font_pt']==size)
        # Crop only the footer in the SVG viewport; no scaling of its glyphs.
        with fitz.open(CARDS/f'{filename("T1",size)}.pdf') as doc:
            page=doc[0];page.set_cropbox(fitz.Rect(0,record['source_top_pt']-7.5,page.rect.width,page.rect.height))
            svg=page.get_svg_image(text_as_path=True)
            url='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
            width=page.rect.width*96/72;height=page.rect.height*96/72
        footer.append(f'<div class="sample"><h3>{size} pt'+(' (current)' if size==10 else '')+f'</h3><img src="{url}" width="{width:.5f}" height="{height:.5f}" alt="Source and notes at {size} points"></div>')
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Source and notes: 6, 7 or 8 pt</title><style>
*{box-sizing:border-box}body{margin:0;background:#fff;color:#282828;font:11pt/1.5 Arial,sans-serif}
header,.reading{width:648px;max-width:calc(100% - 48px);margin:0 auto}header{padding:36px 0 20px}
h1{font-size:22pt;line-height:1.2}h2{font-size:17pt}h3{font-size:11pt}a{color:#285F96}
.controls{position:sticky;top:0;z-index:1;background:#fff;border-block:1px solid #ddd;padding:12px 24px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;align-items:center}
button{font:10pt Arial,sans-serif;padding:8px 16px;background:#fff;color:#285F96;border:1px solid #285F96;border-radius:3px;cursor:pointer}
button[aria-pressed="true"]{background:#285F96;color:white}button:focus-visible{outline:2px solid #282828;outline-offset:3px}
.scroll{overflow-x:auto;margin:24px auto;padding:0 24px}.scroll img{display:block;margin:0 auto;max-width:none}
section{margin:36px 0 60px}p{margin:0 0 14px}.samples{max-width:1368px;padding:0 24px;margin:24px auto;display:flex;gap:24px;flex-wrap:wrap}
.sample{overflow-x:auto;max-width:100%}.sample img{display:block;max-width:none}.caption{font-size:10pt;color:#666}
footer{padding:0 0 36px}.sample h3{margin:0 0 8px}
@media(max-width:700px){.scroll img{margin:0}}
</style></head><body><header><h1>Source and notes: choose a text size</h1>
<p>Compare 6, 7 and 8 pt with the current 10 pt reference. Arial, the approved 75% figure height, plot size, colors and all other type sizes stay fixed.</p>
<p class="caption">Use 100% browser zoom to compare the actual type sizes. The wide multi-panel figure scrolls on smaller screens. Only the source and notes change; extra space stays inside the fixed-height figure block.</p>
<p><a href="source-notes-size-comparison.pdf">Open the side-by-side PDF comparison and article examples</a></p>
<h2>Footer comparison</h2></header><div class="samples">FOOTERS</div>
<div class="controls"><span>Show full figures at:</span><button data-size="6" aria-pressed="false">6 pt</button><button data-size="7" aria-pressed="false">7 pt</button><button data-size="8" aria-pressed="true">8 pt</button><button data-size="10" aria-pressed="false">10 pt (current)</button><span id="status" aria-live="polite">8 pt source and notes</span></div>
<main>EXAMPLES</main><footer class="reading"><p class="caption">Decision: 8 pt was selected on 16 November 2026. This historical comparison retains fixed-height blocks and the previous 10 pt control. The current guide and gallery also trim the footer to equal top/bottom padding.</p></footer>
<script>const variants=VARIANTS;function select(size){document.querySelectorAll('img[data-figure]').forEach(img=>img.src=variants[img.dataset.figure][size]);document.querySelectorAll('button[data-size]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.size===String(size))));document.getElementById('status').textContent=size+' pt source and notes';}document.querySelectorAll('button[data-size]').forEach(button=>button.addEventListener('click',()=>select(button.dataset.size)));select(8);</script></body></html>'''
    (OUT/'comparison.html').write_text(page.replace('FOOTERS',''.join(footer)).replace('EXAMPLES',''.join(rows)).replace('VARIANTS',json.dumps(data)))


def main():
    for p in [OUT,CARDS,TEMP]:p.mkdir(parents=True,exist_ok=True)
    protected=[ROOT/'selected-style.json',ROOT/'README.md',ROOT/'article-context/all-16-figures-in-article-context.pdf']
    protected+=list((article.SOURCE/'figures').glob('*'))
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    assert CURRENT['block_height_factor']==.75
    article.mp.setup()
    for key in EXAMPLES:
        for size in SIZES:make_card(key,size)
        print('Compared',key,flush=True)
    book=fitz.open();doc=overview();book.insert_pdf(doc);doc.close()
    toc=[[1,'Side-by-side comparison: 6, 7, 8 and current 10 pt',1]]
    for key in EXAMPLES:
        for size in [6,7,8]:
            page_number=len(book)+1;doc=article_page(key,size,page_number)
            book.insert_pdf(doc);doc.close()
            toc.append([1,f'{key}: {size} pt source and notes',page_number])
    book.set_toc(toc);book.set_metadata({'title':'Source and notes: 6, 7 or 8 pt','author':'Plotting style comparison'})
    book.save(OUT/BOOK,garbage=4,deflate=True);book.close()
    verify_pdf();write_html()
    assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    (OUT/'validation.json').write_text(json.dumps(dict(candidate_sizes_pt=[6,7,8],control_size_pt=10,
        figure_height_factor=.75,figure_geometry_unchanged=True,approved_style_unchanged=True,
        source_exports_byte_unchanged=True,pdf_fonts_embedded=True,pdf_pages=10,figures=AUDIT),indent=2)+'\n')
    (OUT/'README.md').write_text('''# Source and notes font-size comparison

[Interactive comparison](comparison.html) · [PDF comparison](source-notes-size-comparison.pdf)

Candidates: **6, 7 and 8 pt Arial Regular**, with the current **10 pt** as a control. Only source credits and notes change. Figure titles, subtitles, axes, ticks, legends, annotations and values retain their existing type. Colors and source data are unchanged.

The approved 75%-height figure blocks and native chart dimensions stay fixed. The source starts at the same position; notes retain a 6 pt gap after the source. Smaller text wraps naturally, leaving any saved space at the bottom of the fixed-height block. This isolates type size from figure geometry.

The first PDF page compares all four sizes side by side at native scale. The next nine pages show the three candidates in lorem ipsum context for T1 (line chart), U1 (bar chart with longer notes) and M2 (eight-panel composition). The HTML provides footer comparisons and switches the full examples between sizes. Review at 100% zoom; fitting the entire review sheet to a window reduces the apparent font size.

8 pt was selected on 16 November 2026. This historical comparison retains its original fixed-height blocks; the current guide and gallery use 8 pt with equal top/bottom padding. Reproduce with `python figures4papers-minimal/render_note_size_study.py` using the existing plotting environment.
''')
    print('Completed',OUT/BOOK,flush=True)


if __name__=='__main__':main()
