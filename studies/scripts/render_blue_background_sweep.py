"""Eight controlled plot-blue candidates in identical lorem ipsum article pages.

The agreed outer figure color stays #EDF4F9. This study does not select a new
default. Existing chart data, physical dimensions, Arial type and R1 marks stay
fixed. Run with the same environment as render_reference_collection.py.
"""
from pathlib import Path
import base64
import hashlib
import html
import json
import shutil
import subprocess

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont

import render_article_context as article
import render_reference_collection as reference
import render_multipanel_examples as mp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'blue-background-sweep'
CHARTS = OUT / 'figures'
PREVIEWS = OUT / 'previews'
TEMP = OUT / 'tmp'
BOOK = 'blue-backgrounds-in-article.pdf'
CANVAS = '#EDF4F9'
PAGE_COLOR = '#FFFFFF'
CANDIDATES = [
    ('A', '#D8E8F4'),
    ('B', '#D3E5F2'),
    ('C', '#CEE1F0'),
    ('D', '#C9DEED'),
    ('E', '#C4DBEA'),
    ('F', '#BFD8E7'),
    ('G', '#BAD4E4'),
    ('H', '#B5D1E1'),
]
PAGE_W, PAGE_H = 612, 792
BODY_W, BODY_X = 450, 81
CARD_X, CARD_W = 63, 486
TITLE = 'Lorem ipsum dolor sit amet'
SPEC = next(s for s in json.loads((ROOT / 'reference-review-10pt/data-and-sources.json').read_text())
            if s['id'] == 'T1')
DATA_SHA = hashlib.sha256((ROOT / 'data.json').read_bytes()).hexdigest()
BASE_SETTINGS = (ROOT / 'selected-style.json').read_bytes()
SELECTED_OPTION = json.loads(BASE_SETTINGS).get('background_revision', {}).get('selected_option')
SELECTED_COLOR = dict(CANDIDATES).get(SELECTED_OPTION)
SELECTION_NOTE = (f'Option {SELECTED_OPTION} ({SELECTED_COLOR}) is selected in the style guide; '
                  'the other options remain as comparison artifacts.' if SELECTED_COLOR
                  else 'These candidates have not replaced the selected plotting style.')


def luminance(color):
    rgb = np.array(mpl.colors.to_rgb(color))
    rgb = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    return float(rgb @ [0.2126, 0.7152, 0.0722])


def contrast(a, b):
    x, y = sorted([luminance(a), luminance(b)])
    return (y + .05) / (x + .05)


def render_chart(letter, color):
    # In-memory overrides only; the saved selected style is not edited.
    mp.BG = reference.BG = reference.urban.BG = color
    mp.S['panel'] = color
    mp.S['theme']['background'] = color
    reference.urban.axes = reference.axes
    f, values = reference.prepare_urban(3, None)
    mp.compact_layout(f)
    reference.check_figure(f, SPEC)
    assert values == SPEC['data']
    baseline = next(v for v in json.loads((ROOT / 'reference-review-10pt/validation.json').read_text())['figures']
                    if v['id'] == 'T1')
    assert np.allclose(f.get_size_inches(), baseline['size_inches'])
    assert f._layout_audit == baseline['spacing']
    axes = f.axes[0]
    panel = axes.get_position()
    panel_rect = [panel.x0 * f.get_figwidth() * 72,
                  (1 - panel.y1) * f.get_figheight() * 72,
                  panel.x1 * f.get_figwidth() * 72,
                  (1 - panel.y0) * f.get_figheight() * 72]
    for ext in ['pdf', 'svg', 'png']:
        f.savefig(CHARTS / f'option-{letter}.{ext}', dpi=240)
    record = dict(option=letter, plot_background=color, figure_background=CANVAS,
                  chart_size_pt=(f.get_size_inches() * 72).tolist(),
                  panel_rect_pt=panel_rect, chart_scale=1.0,
                  source_chart_id='T1', source_data_sha256=DATA_SHA,
                  spacing=f._layout_audit, font='Arial', font_pt=10,
                  ink_contrast=round(contrast(mp.INK, color), 3),
                  panel_to_figure_contrast=round(contrast(CANVAS, color), 3))
    plt.close(f)
    return record


def tx(f, x, top, content, width=BODY_W, size=10, bold=False, color=mp.INK, leading=1.3):
    return article.text(f, x, top, content, width=width, size=size,
                        bold=bold, color=color, leading=leading)


def render_page(record, index):
    letter, color = record['option'], record['plot_background']
    f = plt.figure(figsize=(PAGE_W / 72, PAGE_H / 72), facecolor='white')
    tx(f, CARD_X, 22, 'FIELD NOTES / BACKGROUND STUDY', width=300, size=9, color=mp.MUTED)
    tx(f, 402, 22, f'{letter}  /  {color}', width=147, size=9, color=mp.MUTED)
    _, y = tx(f, BODY_X, 55, TITLE, size=19, bold=True)
    _, y = tx(f, BODY_X, y + 13, article.PARAGRAPHS[0], size=11, leading=1.45)
    top = y + 20

    _, y = tx(f, BODY_X, top + 18, 'Figure 1. ' + SPEC['title'], bold=True)
    _, y = tx(f, BODY_X, y + 4, SPEC['subtitle'])
    chart_top = y + 8
    cw, ch = record['chart_size_pt']
    assert abs(cw - BODY_W) < .01
    _, y = tx(f, BODY_X, chart_top + ch + 10, SPEC['source'])
    _, y = tx(f, BODY_X, y + 8, SPEC['notes'], color=mp.MUTED)
    bottom = y + 18
    f.add_artist(Rectangle((CARD_X / PAGE_W, 1 - bottom / PAGE_H),
                          CARD_W / PAGE_W, (bottom - top) / PAGE_H,
                          transform=f.transFigure, facecolor=CANVAS,
                          edgecolor='none', zorder=-.5))
    _, prose_bottom = tx(f, BODY_X, bottom + 20, article.PARAGRAPHS[1], size=11, leading=1.45)
    assert prose_bottom < PAGE_H - 48, (letter, prose_bottom)
    tx(f, CARD_X, PAGE_H - 28, 'Fictitious article. Figure background: #EDF4F9. Plot background: ' + color,
       width=460, size=8, color=mp.MUTED)
    tx(f, 532, PAGE_H - 28, f'{index:02}', width=17, size=8, color=mp.MUTED)
    f.canvas.draw()
    boxes = [t.get_window_extent(f.canvas.get_renderer()) for t in f.texts]
    assert all(f.bbox.contains(b.x0, b.y0) and f.bbox.contains(b.x1, b.y1) for b in boxes)
    assert not any(a.overlaps(b) for i, a in enumerate(boxes) for b in boxes[i + 1:])
    intermediate = TEMP / f'article-{letter}.pdf'
    f.savefig(intermediate, facecolor='white')
    plt.close(f)
    d = fitz.open(intermediate)
    chart_rect = fitz.Rect(BODY_X, chart_top, BODY_X + cw, chart_top + ch)
    with fitz.open(CHARTS / f'option-{letter}.pdf') as chart:
        d[0].show_pdf_page(chart_rect, chart, 0)
    record.update(card_rect=[CARD_X, top, CARD_X + CARD_W, bottom],
                  chart_rect=list(chart_rect), prose_bottom=prose_bottom)
    return d


def verify(book, records):
    with fitz.open(book) as d:
        assert len(d) == 8
        common_chart_text = None
        common_article_text = None
        for page, r in zip(d, records):
            chart_rect = fitz.Rect(r['chart_rect'])
            chart_text = []
            article_text = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        rect = fitz.Rect(span['bbox'])
                        assert page.rect.contains(rect), (r['option'], span)
                        assert span['font'] in ['ArialMT', 'Arial-BoldMT'], span
                        if chart_rect.contains(rect):
                            assert abs(span['size'] - 10) < .001
                            chart_text.append((span['text'], span['size'], span['font'], span['bbox']))
                        elif 40 < rect.y0 < PAGE_H - 48:
                            article_text.append((span['text'], span['size'], span['font'], span['bbox']))
            if common_chart_text is None:
                common_chart_text = chart_text
                common_article_text = article_text
            assert chart_text == common_chart_text
            assert article_text == common_article_text
            for font in page.get_fonts():
                assert d.extract_font(font[0])[-1]
            pix = page.get_pixmap()
            assert pix.pixel(2, 2) == (255, 255, 255)
            x, y, _, _ = r['card_rect']
            samples = [(int(x + 3), int(y + 3), CANVAS)]
            x0, y0, x1, y1 = r['panel_rect_pt']
            samples.append((int(BODY_X + x0 + 5), int(chart_rect.y0 + y0 + 5), r['plot_background']))
            for x, y, expected in samples:
                rgb = pix.pixel(x, y)
                want = tuple(round(c * 255) for c in mpl.colors.to_rgb(expected))
                assert max(abs(a - b) for a, b in zip(rgb, want)) <= 1, (r['option'], rgb, want)
    for r in records:
        svg = (CHARTS / f'option-{r["option"]}.svg').read_text().lower()
        assert CANVAS.lower() in svg and r['plot_background'].lower() in svg
        assert '#dceaf4' not in svg
    assert (ROOT / 'selected-style.json').read_bytes() == BASE_SETTINGS
    assert hashlib.sha256((ROOT / 'data.json').read_bytes()).hexdigest() == DATA_SHA


def write_html(records):
    nav = ''.join(f'<a href="#option-{r["option"]}"><span style="background:{r["plot_background"]}"></span>'
                  f'{r["option"]} <small>{r["plot_background"]}</small></a>' for r in records)
    sections = []
    for r in records:
        letter, color = r['option'], r['plot_background']
        svg = base64.b64encode((CHARTS / f'option-{letter}.svg').read_bytes()).decode()
        w, h = [v * 96 / 72 for v in r['chart_size_pt']]
        sections.append(f'''<section id="option-{letter}" class="proof">
<div class="proof-heading"><span>OPTION {letter}</span><span>Plot: {color} / Figure: {CANVAS}</span></div>
<article><div class="reading"><h2>{TITLE}</h2><p>{article.PARAGRAPHS[0]}</p></div>
<div class="figure-scroll"><figure>
<h3>Figure 1. {html.escape(SPEC['title'])}</h3><p class="subtitle">{html.escape(SPEC['subtitle'])}</p>
<img src="data:image/svg+xml;base64,{svg}" width="{w}" height="{h}" alt="{html.escape(SPEC['alt'])}">
<figcaption><p>{html.escape(SPEC['source'])}</p><p class="notes">{html.escape(SPEC['notes'])}</p></figcaption>
</figure></div><div class="reading"><p>{article.PARAGRAPHS[1]}</p></div></article>
</section>''')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eight blue plot backgrounds in article context</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:white;color:#282828;font:11pt/1.45 Arial,sans-serif}
header{max-width:800px;margin:36px auto 28px;padding:0 24px}header h1{font-size:22pt;line-height:1.15;margin:0 0 12px}header p{margin:0 0 12px}
a{color:#285F96}nav{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:22px 0}nav a{display:flex;align-items:center;gap:8px;text-decoration:none;color:#282828;font-size:11pt}
nav span{width:26px;height:26px;border:1px solid #566C7B}nav small{font-size:9pt}.proof{max-width:816px;margin:0 auto 42px;padding:24px 0;scroll-margin-top:12px;border-top:1px solid #ddd}
.proof-heading{max-width:648px;margin:0 auto 30px;display:flex;justify-content:space-between;gap:16px;font-size:9pt;color:#666}
.reading{width:600px;max-width:calc(100% - 48px);margin:0 auto}.reading h2{font-size:19pt;line-height:1.3;margin:0 0 13pt}.reading p{margin:0}
.figure-scroll{overflow-x:auto;margin:20pt 0;padding:0 18px}figure{width:648px;margin:0 auto;padding:24px;background:CANVAS_COLOR;font:10pt/1.3 Arial,sans-serif}
figure h3{font-size:10pt;line-height:1.3;margin:0 0 4pt;font-weight:700}figure .subtitle{margin:0 0 8pt}figure img{display:block;width:600px;max-width:none;height:auto}
figcaption{margin-top:10pt}figcaption p{margin:0}figcaption .notes{margin-top:8pt;color:#666}footer{max-width:800px;margin:24px auto;padding:0 24px 24px;font-size:9pt;color:#666}
@media(max-width:700px){nav{grid-template-columns:repeat(2,1fr)}.proof-heading{padding:0 24px}.figure-scroll figure{margin:0}}
</style></head><body><header><h1>Eight blue plot backgrounds</h1>
<p>Figure background stays at <strong>#EDF4F9</strong>. Only the plot background changes. A-H progress from lighter to darker blue; all are slightly deeper than the previous #DCEAF4 plot.</p>
<p>The same chart and fictitious article are repeated for comparison. Chart type is 10 pt Arial at its native 6.25-inch width; view at 100% browser zoom.</p>
<p><a href="blue-backgrounds-in-article.pdf">Download the eight-page article proof</a> / <a href="overview.png">See all eight together</a></p>
<nav>OPTIONS</nav></header><main>SECTIONS</main>
<footer>SELECTION_NOTE Article prose is fictitious. Chart data and credits are retained from the current reference collection.</footer></body></html>'''
    (OUT / 'gallery.html').write_text(page.replace('CANVAS_COLOR', CANVAS).replace('OPTIONS', nav).replace('SECTIONS', ''.join(sections)).replace('SELECTION_NOTE', SELECTION_NOTE))


def overview(records):
    regular = ImageFont.truetype(mp.findfont(mp.FontProperties(family='Arial')), 24)
    bold = ImageFont.truetype(mp.findfont(mp.FontProperties(family='Arial', weight='bold')), 28)
    sheet = Image.new('RGB', (1800, 1418), 'white')
    draw = ImageDraw.Draw(sheet)
    draw.text((32, 22), 'Eight plot blues / fixed figure background #EDF4F9', font=bold, fill=mp.INK)
    draw.text((32, 65), 'A-H: lighter to darker. Open the PDF to inspect each in a full article page.', font=regular, fill=mp.MUTED)
    for i, r in enumerate(records):
        x = 25 + (i % 4) * 445
        y = 116 + (i // 4) * 646
        draw.text((x, y), f'{r["option"]}  {r["plot_background"]}', font=bold, fill=mp.INK)
        with Image.open(PREVIEWS / f'option-{r["option"]}.png') as im:
            im.thumbnail((420, 585), Image.Resampling.LANCZOS)
            sheet.paste(im, (x, y + 47))
    sheet.save(OUT / 'overview.png')


def render_previews(records):
    subprocess.run(['pdftoppm', '-r', '120', '-png', str(OUT / BOOK), str(TEMP / 'poppler')], check=True)
    for i, r in enumerate(records, 1):
        shutil.copyfile(TEMP / f'poppler-{i}.png', PREVIEWS / f'option-{r["option"]}.png')
    overview(records)


def main():
    for p in [OUT, CHARTS, PREVIEWS, TEMP]:
        p.mkdir(parents=True, exist_ok=True)
    assert mp.S['canvas'] == CANVAS
    assert all(luminance(a[1]) > luminance(b[1]) for a, b in zip(CANDIDATES, CANDIDATES[1:]))
    assert luminance(CANDIDATES[0][1]) < luminance('#DCEAF4')
    mp.setup()
    article.PAGE_W, article.PAGE_H = PAGE_W, PAGE_H
    article.BODY_W, article.BODY_X = BODY_W, BODY_X
    records = []
    book = fitz.open()
    for i, (letter, color) in enumerate(CANDIDATES, 1):
        record = render_chart(letter, color)
        page = render_page(record, i)
        book.insert_pdf(page)
        page.close()
        records.append(record)
        print('Rendered', letter, color, flush=True)
    book.set_metadata({'title': 'Eight blue plot backgrounds in article context', 'author': 'Plotting style study'})
    book.set_toc([[1, f'Option {r["option"]}: {r["plot_background"]}', i] for i, r in enumerate(records, 1)])
    book.save(OUT / BOOK, garbage=4, deflate=True)
    book.close()
    verify(OUT / BOOK, records)
    render_previews(records)
    write_html(records)
    (OUT / 'candidates.json').write_text(json.dumps(dict(status='selected' if SELECTED_COLOR else 'comparison_pending_selection',
        selected_option=SELECTED_OPTION, selected_plot_background=SELECTED_COLOR,
        page_background=PAGE_COLOR, figure_background=CANVAS, previous_plot_background='#DCEAF4',
        source_chart=SPEC, candidates=records), indent=2) + '\n')
    (OUT / 'validation.json').write_text(json.dumps(dict(pages=8, figure_background=CANVAS,
        candidate_order='lighter to darker', only_plot_background_varies=True,
        native_chart_dimensions_preserved=True, font='Arial', chart_font_pt=10,
        pdf_fonts_embedded=True, chart_data_unchanged=True, text_and_layout_identical=True,
        no_text_overlaps=True, no_text_outside_page=True, selected_style_unchanged=True,
        plot_and_figure_pixel_colors_verified=True, candidates=records), indent=2) + '\n')
    table = '\n'.join(f'| {r["option"]} | `{r["plot_background"]}` |' for r in records)
    (OUT / 'README.md').write_text(f'''# Blue plot-background sweep

[Eight-page PDF in article context]({BOOK}) / [Scrolling comparison](gallery.html) / [Overview](overview.png)

Eight proposed plot backgrounds, ordered from lighter to darker. The outer figure background is fixed at **{CANVAS}**, and the article page is white. **{SELECTION_NOTE}** See the [style guide](../README.md) and [selected settings](../selected-style.json).

| Option | Plot background |
|---|---|
{table}

Each page repeats the same T1 line plot and lorem ipsum prose. The original chart is 6.25 inches wide, placed without rescaling on a US Letter page. Plot and figure text remains 10 pt Arial, with bold figure and axis titles; other figure text is regular. The existing directly labeled series retain their R1 colors, line widths, markers, values and spacing. Direct labels mean this particular chart needs no legend. Article body text is 11 pt Arial, and its headline is 19 pt Arial bold.

All figure headings, sources and notes sit inside an {CANVAS} block with 18 pt padding. The title-to-subtitle gap is 4 pt, and subtitle-to-visible-chart-content clearance is 11 pt. The illustration is repeated intentionally to isolate the background change. Source credits and the existing data are preserved; lorem ipsum prose makes no claim about the data.

The PDF embeds Arial and preserves vector charts. Native PNG/PDF/SVG files are in `figures/`. The HTML embeds all SVGs and preserves native chart width, with horizontal scrolling on narrow displays. Review at 100% zoom.

Reproduce with `MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_blue_background_sweep.py`.
''')
    print('Verified', OUT / BOOK, flush=True)


if __name__ == '__main__':
    main()
