"""Place all sixteen current figures in a fictional article at native scale."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/figures4papers-mpl')
import base64
import hashlib
import html
import json
import shutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle
import pymupdf as fitz
import render_multipanel_examples as mp

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'reference-review-10pt'
OUT=ROOT/'article-context';TEMP=OUT/'tmp';PREVIEWS=OUT/'previews'
BOOK='all-16-figures-in-article-context.pdf'
BOOK_ALIAS='figures-in-article-context.pdf'
HTML='article-context.html'
PAGE_W=PAGE_H=14*72
BODY_W=486;BODY_X=(PAGE_W-BODY_W)/2
SELECTED=['U1','U2','U3','T1','T2','T3','H1','H2','H3','H4','P1','P2','M1','M2','M3','M4']
RECORDS={s['id']:s for s in json.loads((SOURCE/'data-and-sources.json').read_text())}
CANVAS=mp.S['canvas'];PANEL=mp.BG;INK=mp.INK;MUTED=mp.MUTED
VERTICAL_SCALE=mp.SELECTED.get('height_revision',{}).get('vertical_spacing_factor',1)
BLOCK_FACTOR=mp.SELECTED.get('height_revision',{}).get('block_height_factor',1)
HEIGHT_BASELINE=json.loads((ROOT/'figure-height-baseline.json').read_text())['figures'] if BLOCK_FACTOR!=1 else {}
FOOTER_PT=mp.T['notes_pt']
VERTICAL_PADDING=mp.SELECTED['layout']['article_figure_block_vertical_padding_pt']
TITLE='Reading patterns in a changing landscape'
SECTIONS={
    'U1':'A framework for comparison', 'U2':'Contrasting two scenarios', 'U3':'Patterns over time',
    'T1':'Following a process', 'T2':'Comparing a ranked field', 'T3':'A focus among several curves',
    'H1':'A benchmark in context', 'H2':'A focal series in context', 'H3':'Tracing a trajectory',
    'H4':'Responses across a range', 'P1':'Looking across benchmarks', 'P2':'Comparing several methods',
    'M1':'Comparing several measures', 'M2':'Looking across conditions',
    'M3':'A conceptual view', 'M4':'Change across two domains',
}
PARAGRAPHS=[
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer dignissim, velit at tempor placerat, arcu lorem tincidunt sem, vitae fermentum nulla metus at sapien. Sed cursus lectus quis lacus interdum, non posuere enim facilisis. Donec vitae libero at massa commodo varius. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.',
    'Curabitur finibus neque vitae justo vestibulum, sit amet ultricies risus tincidunt. Mauris at mi sed purus molestie faucibus. Nam facilisis, justo et tincidunt aliquet, ligula massa volutpat urna, sed consequat sapien eros non velit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aenean feugiat nibh vitae lorem dictum, sed tempor arcu porttitor.',
    'Praesent blandit erat non diam porttitor, a luctus turpis posuere. Aliquam tempor ante id mauris dictum, vitae pellentesque nibh cursus. Etiam tincidunt dui in erat pulvinar, vitae gravida lorem fermentum. Phasellus non arcu velit. Duis consequat massa et ligula hendrerit, at luctus nulla consectetur. Nulla facilisi. Sed id elit vitae justo sollicitudin imperdiet.',
    'Suspendisse potenti. Morbi in sem quis justo viverra congue. Nunc pulvinar purus vel mi sollicitudin, non placerat sapien rhoncus. Sed venenatis lectus nec quam pretium, at bibendum libero interdum. Fusce vitae dui eget ipsum aliquam mollis. Proin tincidunt nibh eu lacus cursus, ac pharetra nibh consequat. Quisque commodo magna a neque tempor, sed porttitor odio vestibulum.',
]


def wrapped(text,width,size=10,bold=False):
    renderer=RendererAgg(10,10,72)
    prop=FontProperties(family='Arial',size=size,weight='bold' if bold else 'normal')
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if line and renderer.get_text_width_height_descent(candidate,prop,ismath=False)[0]>width:
            lines.append(line);line=word
        else:line=candidate
    lines.append(line)
    return '\n'.join(lines)


def text(f,x,top,body,width=BODY_W,size=10,bold=False,color=INK,leading=1.3):
    t=f.text(x/PAGE_W,1-top/PAGE_H,wrapped(body,width,size,bold),ha='left',va='top',
             fontsize=size,fontfamily='Arial',fontweight='bold' if bold else 'normal',
             color=color,linespacing=leading)
    f.canvas.draw();box=t.get_window_extent(f.canvas.get_renderer())
    return t,PAGE_H-box.y0*72/f.dpi


def body(f,top,paragraph):
    return text(f,BODY_X,top,paragraph,size=11,leading=1.45)


def base_page(number):
    f=plt.figure(figsize=(14,14),facecolor='white')
    text(f,36,24,'FIELD NOTES  /  FICTIONAL ARTICLE',width=550,size=9,color=MUTED)
    text(f,PAGE_W-205,24,'COLOR CONTEXT PROOF',width=170,size=9,color=MUTED)
    text(f,36,PAGE_H-31,'Fictitious prose; existing figure data and source credits retained.',width=850,size=9,color=MUTED)
    text(f,PAGE_W-48,PAGE_H-31,f'{number:02}',width=20,size=9,color=MUTED)
    return f


def card(f,spec,number,top):
    path=SOURCE/'figures'/f'{spec["slug"]}.pdf'
    with fitz.open(path) as chart:cw,ch=chart[0].rect.width,chart[0].rect.height
    width=cw+36;x=(PAGE_W-width)/2;tx=x+18
    if mp.MINIMAL:
        chart_top=top+VERTICAL_PADDING
        title_top=chart_top;notes_bottom=chart_top+ch
        source_top=notes_bottom+VERTICAL_PADDING+1
    else:
        title,y=text(f,tx,top+VERTICAL_PADDING,f'Figure {number}. {spec["title"]}',cw,bold=True)
        _,y=text(f,tx,y+4*VERTICAL_SCALE,spec['subtitle'],cw)
        chart_top=y+8*VERTICAL_SCALE
        source_top=chart_top+ch+10*VERTICAL_SCALE
        _,y=text(f,tx,source_top,spec['source'],cw,size=FOOTER_PT)
        _,y=text(f,tx,y+8*VERTICAL_SCALE,spec['notes'],cw,size=FOOTER_PT,color=MUTED)
        notes_bottom=y
        title_top=PAGE_H-title.get_window_extent(f.canvas.get_renderer()).y1*72/f.dpi
    bottom=notes_bottom+VERTICAL_PADDING
    f.add_artist(Rectangle((x/PAGE_W,1-bottom/PAGE_H),width/PAGE_W,(bottom-top)/PAGE_H,
                 transform=f.transFigure,facecolor=CANVAS,edgecolor='none',zorder=-.5))
    if spec['slug'] in mp.SELECTED['width_revision']['narrowed_figures']:
        assert abs(width-BODY_W)<.01,(spec['id'],'figure does not match text width',width)
    if HEIGHT_BASELINE and spec['slug'] not in mp.SELECTED['width_revision']['narrowed_figures']:
        from figure_height import block_dimensions
        _,expected_chart=block_dimensions(spec['slug'],BLOCK_FACTOR,VERTICAL_SCALE)
        assert abs(ch-expected_chart)<.05,(spec['id'],'approved chart height changed',ch,expected_chart)
    assert abs((title_top-top)-(bottom-notes_bottom))<.01
    return bottom,(path,fitz.Rect(tx,chart_top,tx+cw,chart_top+ch)),dict(
        figure_id=spec['id'],figure_number=number,card_rect=[x,top,x+width,bottom],
        native_chart_size_pt=[cw,ch],native_scale=1.0,chart_rect=[tx,chart_top,tx+cw,chart_top+ch],
        plot_layout_height_factor=BLOCK_FACTOR,
        block_height_factor=(bottom-top)/HEIGHT_BASELINE[spec['slug']]['old_block_height_pt'],
        source_notes_font_pt=FOOTER_PT,source_top_pt=source_top,notes_bottom_pt=notes_bottom,
        top_padding_pt=title_top-top,bottom_padding_pt=bottom-notes_bottom,
        source_pdf_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def page(spec,index):
    f=base_page(index);section=SECTIONS[spec['id']]
    if index==1:
        _,y=text(f,BODY_X,64,TITLE,size=22,bold=True,leading=1.15)
        _,y=text(f,BODY_X,y+10,'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed cursus lectus quis lacus interdum.',size=12,leading=1.4,color=MUTED)
        _,y=text(f,BODY_X,y+12,'Editorial sample  |  15 November 2026',size=9,color=MUTED)
        _,y=body(f,y+18,PARAGRAPHS[0])
    else:
        _,y=text(f,BODY_X,64,section,size=17,bold=True)
        _,y=body(f,y+13,PARAGRAPHS[(index-1)%4])
    bottom,placement,record=card(f,spec,index,y+20)
    assert bottom<PAGE_H-130,(spec['id'],bottom)
    # Text on white above and below the complete colored figure block.
    after=bottom+20;paragraphs_below=0
    for k in range(2 if spec['id'][0]!='M' else 1):
        t,new_y=body(f,after,PARAGRAPHS[(index+k)%4])
        if new_y>PAGE_H-64:
            t.remove();break
        after=new_y+12;paragraphs_below+=1
    assert after>bottom+25,(spec['id'],'no prose below figure')
    record.update(article_section=section,paragraphs_above=1,paragraphs_below=paragraphs_below,
                  prose_bottom_pt=after-12)
    f.canvas.draw();r=f.canvas.get_renderer();boxes=[]
    for t in f.texts:
        box=t.get_window_extent(r)
        assert box.x0>=0 and box.y0>=0 and box.x1<=f.bbox.width and box.y1<=f.bbox.height
        boxes.append(box)
    assert not any(a.overlaps(b) for i,a in enumerate(boxes) for b in boxes[i+1:]),spec['id']
    p=TEMP/f'page-{index:02}.pdf';f.savefig(p,facecolor='white');plt.close(f)
    doc=fitz.open(p)
    with fitz.open(placement[0]) as chart:doc[0].show_pdf_page(placement[1],chart,0)
    return doc,record


def article_html():
    chunks=[]
    for i,key in enumerate(SELECTED,1):
        s=RECORDS[key];slug=s['slug']
        with fitz.open(SOURCE/'figures'/f'{slug}.pdf') as chart:
            w,h=[v*96/72 for v in (chart[0].rect.width,chart[0].rect.height)]
        svg=base64.b64encode((SOURCE/'figures'/f'{slug}.svg').read_bytes()).decode()
        before=PARAGRAPHS[(i-1)%4]
        after=''.join(f'<p>{PARAGRAPHS[(i+k)%4]}</p>' for k in range(2))
        chunks.append(f'''<section id="figure-{i}">
<div class="reading"><h2>{html.escape(SECTIONS[key])}</h2><p>{before}</p></div>
<div class="figure-scroll"><figure style="--chart-width:{w:.5f}px">
<h3>Figure {i}. {html.escape(s['title'])}</h3><p class="subtitle">{html.escape(s['subtitle'])}</p>
<img src="data:image/svg+xml;base64,{svg}" width="{w:.5f}" height="{h:.5f}" alt="{html.escape(s['title'])}">
<figcaption><p>{html.escape(s['source'])}</p><p class="notes">{html.escape(s['notes'])}</p></figcaption>
</figure></div><div class="reading">{after}</div></section>''')
    doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Figures in article context</title><style>
*{box-sizing:border-box}body{margin:0;color:#282828;background:#fff;font:11pt/1.6 Arial,sans-serif}
.masthead{margin:0 auto;padding:24px;max-width:1344px;display:flex;justify-content:space-between;gap:20px;color:#666;font-size:9pt}
.reading{width:648px;max-width:calc(100% - 48px);margin:0 auto}.article-header{margin-top:42px;margin-bottom:36px}
h1{font-size:22pt;line-height:1.2;margin:0 0 16px}h2{font-size:17pt;line-height:1.3;margin:30px 0 14px}
.deck{font-size:12pt;color:#666;line-height:1.4}.byline{font-size:9pt;color:#666}p{margin:0 0 16px}
.figure-scroll{overflow-x:auto;margin:26px auto;max-width:100%;padding:0 24px}
figure{background:CANVAS_COLOR;width:calc(var(--chart-width) + 48px);padding:18px 24px;margin:0 auto;border:0;box-shadow:none;font:10pt/1.3 Arial,sans-serif}
figure h3{font-size:10pt;line-height:1.3;margin:0 0 3pt;font-weight:700}.subtitle{margin:0 0 6pt}
figure img{display:block;width:var(--chart-width);max-width:none;height:auto}
figcaption{margin-top:7.5pt;font:8pt/1.3 Arial,sans-serif}figcaption p{margin:0}figcaption .notes{margin-top:6pt;color:#666}
footer{margin:44px auto 30px;color:#666;font-size:9pt}a{color:#285F96}
.proof-notes{border-top:1px solid #ddd;padding-top:18px}
.contents{font-size:10pt;margin:22px 0 30px}.contents summary{cursor:pointer;margin-bottom:10px}.contents ol{padding-left:22px}.contents li{margin:5px 0}
@media(max-width:700px){.masthead{font-size:8pt}.article-header{margin-top:22px}h1{font-size:20pt}}
</style></head><body>
<div class="masthead"><span>FIELD NOTES / FICTIONAL ARTICLE</span><span>COLOR CONTEXT PROOF</span></div>
<main><header class="reading article-header"><h1>Reading patterns in a changing landscape</h1>
<p class="deck">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed cursus lectus quis lacus interdum.</p>
<p class="byline">Editorial sample | 15 November 2026</p>
<p class="byline">All 16 gallery figures in context. <a href="all-16-figures-in-article-context.pdf">Download the complete PDF</a>.</p>
<details class="contents"><summary>Jump to a figure</summary><ol>CONTENTS_LIST</ol></details></header>
'''+''.join(chunks)+'''</main><footer class="reading"><p>Fictitious prose; existing figure data and source credits retained.</p>
<div class="proof-notes"><p>Page: #FFFFFF. Figure blocks: CANVAS_COLOR. Plot panels: PANEL_COLOR.</p>
<p>All sixteen charts retain their approved native size and 10 pt Arial type; source credits and notes use 8 pt Arial. Wide figures scroll on smaller screens. Titles, subtitles and source notes are inside the pale blue blocks; article text stays on white.</p>
<p><a href="all-16-figures-in-article-context.pdf">Download the sixteen-page PDF proof</a></p></div></footer></body></html>'''
    contents=''.join(f'<li><a href="#figure-{i}">{key}: {html.escape(RECORDS[key]["title"])}</a></li>'
                     for i,key in enumerate(SELECTED,1))
    (OUT/HTML).write_text(doc.replace('CANVAS_COLOR',CANVAS).replace('PANEL_COLOR',PANEL).replace('CONTENTS_LIST',contents))


def main():
    for p in [OUT,TEMP,PREVIEWS]:p.mkdir(parents=True,exist_ok=True)
    assert len(SELECTED)==16 and len(set(SELECTED))==16 and set(SELECTED)==set(RECORDS)
    assert json.loads((SOURCE/'selected-style.json').read_text())==mp.SELECTED
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (SOURCE/'figures').iterdir() if p.is_file()}
    mp.setup();book=fitz.open();audit=[]
    for i,key in enumerate(SELECTED,1):
        doc,record=page(RECORDS[key],i)
        doc[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(PREVIEWS/f'page-{i:02}.png')
        book.insert_pdf(doc);doc.close();audit.append(record)
        print('Placed',key,flush=True)
    book.set_metadata({'title':'All 16 figures in article context - R1 / option A','author':'Layout proof'})
    book.set_toc([[1,f'{i}. {key}: {RECORDS[key]["title"]}',i] for i,key in enumerate(SELECTED,1)])
    book.save(OUT/BOOK,garbage=4,deflate=True);book.close()
    with fitz.open(OUT/BOOK) as d:
        assert len(d)==len(SELECTED)==len(audit)
        for page_,record in zip(d,audit):
            for font in page_.get_fonts():assert d.extract_font(font[0])[-1]
            chart_rect=fitz.Rect(record['chart_rect'])
            for b in page_.get_text('dict')['blocks']:
                for line in b.get('lines',[]):
                    for span in line['spans']:
                        rect=fitz.Rect(span['bbox']);size=round(span['size'],3)
                        assert page_.rect.contains(rect),(record['figure_id'],span)
                        assert span['font'] in ['ArialMT','Arial-BoldMT','Arial-ItalicMT','STIXGeneral-Regular','STIXNonUnicode-Italic']
                        if chart_rect.contains(rect):assert size in [7,10],span
                        if record['source_top_pt']-2<=rect.y0 and rect.y1<=record['card_rect'][3]:
                            assert size==FOOTER_PT and span['font']=='ArialMT',span
            assert page_.get_pixmap(clip=fitz.Rect(2,2,4,4)).pixel(0,0)==(255,255,255)
            x,y,_,_=record['card_rect']
            rgb=page_.get_pixmap(clip=fitz.Rect(x+2,y+2,x+4,y+4)).pixel(0,0)
            assert max(abs(a-b) for a,b in zip(rgb,tuple(round(v*255) for v in mp.mpl.colors.to_rgb(CANVAS))))<=1,rgb
            assert record['paragraphs_above']>=1 and record['paragraphs_below']>=1
    assert source_hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (SOURCE/'figures').iterdir() if p.is_file()}
    shutil.copyfile(OUT/BOOK,OUT/BOOK_ALIAS)
    article_html()
    if mp.MINIMAL:
        import re
        p=OUT/HTML;contents=p.read_text()
        contents=re.sub(r'<h3>.*?</h3><p class="subtitle">.*?</p>', '',contents,flags=re.S)
        contents=re.sub(r'<figcaption>.*?</figcaption>', '',contents,flags=re.S)
        p.write_text(contents)
    (OUT/'validation.json').write_text(json.dumps(dict(page_background='#FFFFFF',figure_background=CANVAS,
        plot_background=PANEL,minimal_mode=mp.MINIMAL,figure_count=len(SELECTED),page_count=len(SELECTED),
        plot_layout_height_factor=BLOCK_FACTOR,
        block_height_mode='Fit 8 pt source/notes with equal top and bottom padding',
        source_notes_font_pt=FOOTER_PT,vertical_padding_pt=VERTICAL_PADDING,
        figure_font_pt=10,charts_rescaled=False,pdf_fonts_embedded=True,
        figure_data_unchanged=True,source_exports_byte_unchanged=True,
        lorem_ipsum_above_and_below_every_figure=True,figures=audit),indent=2)+'\n')
    (OUT/'README.md').write_text('''# Figures in a fictitious article

[Scrolling article](article-context.html) · [Complete sixteen-page PDF proof](all-16-figures-in-article-context.pdf)

All sixteen gallery figures (U1-U3, T1-T3, H1-H4, P1-P2 and M1-M4) are embedded in lorem ipsum prose, one figure per PDF page. Every figure has prose above and below it. The article page is white (#FFFFFF), complete figure blocks are pale blue (#EDF4F9), and plot panels retain #D8E8F4. Figure blocks have 18 pt horizontal padding and matching 13.5 pt top/bottom padding, measured from the title and final note text boxes and no added border or shadow. Titles, subtitles, legends, sources and notes stay inside each block. PDF bookmarks and the HTML figure index identify every example.

The charts are regenerated at shorter heights and embedded without rescaling: the default chart width is 6.25 inches, including figures 11, 12 and 16; three dense multi-panel charts have documented 13-inch exceptions, preserving 10 pt Arial. The PDF uses common 14 x 14-inch review pages to fit both widths with surrounding prose. The HTML uses the same physical sizes in CSS pixels and scrolls wide figures on smaller screens. Article prose is 11 pt Arial; article headings are larger than figure titles. This typography belongs to the fictitious article, not the plotting style.

The approved chart dimensions from the 75%-height review are unchanged. Source credits and notes are 8 pt Arial Regular; all other figure text remains 10 pt with the documented math-script exception. The outer blue block fits the smaller footer, ending 13.5 pt below the last note to match the top padding. Saved footer space is removed without stretching the plot. Original data, axis limits, colors and line weights are retained. Figure titles and source notes are copied from the current collection; surrounding prose is intentionally fictitious and should not be read as an interpretation of the data. The HTML is self-contained, with SVG figures embedded as data URLs. Review at 100% browser zoom to inspect native text size.

Reproduce: `MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_article_context.py`.
''')
    print('Completed',OUT/BOOK,flush=True)


if __name__=='__main__':main()
