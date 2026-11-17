from pathlib import Path
import csv
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
import pdfplumber

ROOT = Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('GuideSans','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('GuideBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
INK = colors.HexColor('#232B29'); MUTED = colors.HexColor('#55615D')
TEAL = colors.HexColor('#117C72'); GRID = colors.HexColor('#E0E6E3')

def guide(path,width):
    w=width*72; h=9*72; margin=21.6; usable=w-2*margin
    c=canvas.Canvas(str(path),pagesize=(w,h),initialFontName='GuideSans')
    c.setTitle(f'Paper figure layout rules - {width:.1f} inch preset')
    body=ParagraphStyle('body',fontName='GuideSans',fontSize=9,leading=12,textColor=INK,spaceAfter=7)
    y=h-margin
    def para(text,size=9,bold=False,after=7):
        nonlocal y
        st=ParagraphStyle('p',parent=body,fontName='GuideBold' if bold else 'GuideSans',fontSize=size,leading=size*1.35)
        p=Paragraph(text,st); _,ph=p.wrap(usable,h)
        p.drawOn(c,margin,y-ph); y-=ph+after
    def section(text):
        nonlocal y
        y-=6; para(text,10,True,6)
    def table(rows,colwidths=None):
        nonlocal y
        content=[[Paragraph(str(cell),ParagraphStyle('cell',parent=body,fontName='GuideBold' if i==0 else 'GuideSans',fontSize=8,leading=10)) for cell in row] for i,row in enumerate(rows)]
        tb=Table(content,colWidths=colwidths or [usable/len(rows[0])]*len(rows[0]))
        tb.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'GuideSans'),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,TEAL),
          ('LINEBELOW',(0,1),(-1,-1),.3,GRID),('TOPPADDING',(0,0),(-1,-1),4.5),('BOTTOMPADDING',(0,0),(-1,-1),4.5),
          ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8)]))
        _,th=tb.wrap(usable,h);tb.drawOn(c,margin,y-th);y-=th+9
    def end(page):
        c.setStrokeColor(GRID);c.line(margin,25,w-margin,25)
        c.setFont('GuideSans',7);c.setFillColor(MUTED)
        c.drawString(margin,14,'Del Alamo style study v2 | Synthetic data')
        c.drawRightString(w-margin,14,f'Guide {page}/3')
        if y<35: raise RuntimeError(f'Guide page {page} overflow: {y}')
        c.showPage()
    para('Paper figures, built to size',17,True,9)
    para(f'Physical layout specification | {width:.1f}-inch preset',9,False,12)
    para('The figure budget includes axes, titles, legends and margins. Fonts stay readable at the final size; smaller panels are reflowed rather than scaled-down copies.')
    section('1. Solve the width before drawing')
    para('Panel width = [W - (n - 1) x g] / n<br/>W = total figure width; n = panels across; g = 0.14 in gutter.')
    table([['Preset','Across','6.5 in budget','5.5 in budget'],
      ['Compact','4','1.520 in','1.270 in'],['Small','3','2.073 in','1.740 in'],
      ['Medium','2','3.180 in','2.680 in'],['Large','1','6.500 in','5.500 in']])
    para('<b>NeurIPS correction:</b> The official 2026 template uses a 5.5-inch text width. The 6.5-inch version preserves the requested custom constraint. Use the 5.5-inch exports for that NeurIPS template.')
    section('2. Hold typography constant')
    table([['Element','Physical size'],['Ticks and legend','7.5 pt Helvetica'],['Axis titles','8 pt bold'],
      ['Facet labels','8 pt bold'],['Optional assembly letters','8.5 pt bold'],['Chart headlines','Omit from paper panels; explain in caption']], [usable*.48,usable*.52])
    para('These are proposed design defaults, not conference-mandated font sizes. An 8 pt label shrunk from 6.5 to 1.52 inches becomes about 1.9 pt. Re-render at the intended width.')
    end(1);y=h-margin
    para('Spacing and visual hierarchy',17,True,12)
    table([['Relationship','Starting value'],['Outer padding','3 pt'],['Tick length','2 pt'],['Tick to label','2 pt'],
      ['Label to axis title','4 pt'],['Independent panels','0.14 in'],['Facets inside a chart','6-8 pt'],
      ['Left axis assembly','At least 0.40 in; expand when needed'],['Right end-label reserve','Half the widest x tick label + 3 pt']], [usable*.49,usable*.51])
    section('3. Measure labels, then select ticks')
    para('Use nice-number breaks. The renderer targets about 0.40 in horizontally and 0.28 in vertically between ticks; these are density targets, not hard limits. Nice-number breaks may add a tick. Check rendered labels for at least 4 pt clear separation.')
    para('Keep at least two ticks, leading zeros, consistent precision, zero references and meaningful log powers. Shorten crowded labels before shrinking type: compact categories use L/M/H for Low/Medium/High. Never change data limits, binning or smoothing to fit.')
    section('4. Make marks stronger than scaffolding')
    table([['Element','Specification'],['Frames / ticks','0.18 mm, medium gray'],['Grids','0.13 mm, light gray'],
      ['Main lines','0.40 mm'],['Point outline','0.20 mm'],['Points: compact to large','0.85 / 1.0 / 1.2 / 1.4 mm']], [usable*.49,usable*.51])
    para('A = aquamarine circles; B = orange triangles. Quantitative confidence uses cividis on fixed 50-100 limits. Headings and commentary on the following proof pages are review aids, not part of the individual figure assets.')
    end(2);y=h-margin
    para('Rules for new data and layouts',17,True,12)
    section('5. Width does not determine height')
    para('Standard starting heights: compact 1.65 in, small 1.80 in, medium 2.05 in, large 2.65 in. Increase height for many rows, facets, or dense marks. Preserve equal aspect when physical x/y distance is meaningful.')
    table([['Chart structure','Adaptation'],['Scatter / line','Reduce tick density and marker size modestly. Preserve reference lines and uncertainty.'],
      ['Box / violin / density','Preserve all observations, grouping and smoothing. Distribution shape must not change across sizes.'],
      ['Categories / intervals','Short labels; enough height per row; retain zero and interval endpoints.'],
      ['Heatmap','Keep all cells and the same color limits. Increase height or span before obscuring cells.'],
      ['Small multiples','Four vertical panels at narrow widths; 2 x 2 at medium/large. Shared scales and key.'],
      ['Density + scatter','Aligned x limits and data panels; one x-axis; scatter receives most height.']], [usable*.31,usable*.69])
    section('6. Resolve constraints in a predictable order')
    para('Identify invariant information. Solve the width equation. Measure axes and keys. Choose height. Set ticks. Then resolve overflow by shortening or wrapping labels, sharing axes/legends, reflowing facets, increasing height, or using fewer columns.')
    para('Inspect final-size PDFs and PNGs for clipped or overlapping text, mismatched panel bounds and lost scientific layers. The compact preset is a stress test: three across is often the better choice.')
    section('Using this booklet')
    para('The next twelve pages each compare one chart type at its physical export sizes. Proof sheets can be taller than a manuscript page. Use the separate panel PDF files in your paper, without further shrinking. Exact sizes are in dimensions.csv.')
    para('Source: official NeurIPS 2026 template archive, linked from neurips.cc/Conferences/2026/CallForPapers; checked 7 September 2026. Full rules and reproduction instructions: STYLE_GUIDE.md.',7.5)
    end(3);c.save()

def validate_panels(folder):
    failures=[]
    rows=list(csv.DictReader((folder/'dimensions.csv').open()))
    for row in rows:
        path=folder/'panels'/f"{row['id']}-{row['size']}.pdf"
        p=PdfReader(path).pages[0]
        assert abs(float(p.mediabox.width)/72-float(row['panel_width_in']))<.003, path
        assert abs(float(p.mediabox.height)/72-float(row['panel_height_in']))<.003, path
        assert abs(int(row['columns'])*float(row['panel_width_in'])+(int(row['columns'])-1)*float(row['gutter_in'])-float(row['figure_width_in']))<1e-8
        with pdfplumber.open(path) as doc:
            pg=doc.pages[0]
            for ch in pg.chars:
                if ch['text'].strip() and (ch['x0']<-.2 or ch['x1']>pg.width+.2 or ch['top']<-.2 or ch['bottom']>pg.height+.2):
                    failures.append(f'{path.name}: {ch["text"]!r} outside page')
    if failures: raise RuntimeError('\n'.join(failures))
    return len(rows)

if __name__=='__main__':
    (ROOT/'tmp').mkdir(exist_ok=True)
    for width,slug in [(6.5,'requested-6.5in'),(5.5,'neurips-5.5in')]:
        folder=ROOT/slug
        count=validate_panels(folder)
        gp=ROOT/'tmp'/f'guide-{width}.pdf';guide(gp,width)
        writer=PdfWriter();writer.append(gp)
        for id in 'ABCDEFGHIJKL': writer.append(folder/'proofs'/f'{id}-sizes.pdf')
        writer.add_metadata({'/Title':f'Del Alamo paper figure size studies - {width} inch','/Author':'Style study'})
        target=ROOT/f'figure-style-guide-{width}in.pdf'
        with target.open('wb') as f: writer.write(f)
        print(f'{target.name}: {len(writer.pages)} pages; {count} panel dimensions and text bounds validated')
