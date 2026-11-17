"""Render every starter, validate its PDF, and build a preview book and gallery."""
from pathlib import Path
import hashlib
import html
import json
import runpy
import zipfile
import pymupdf as fitz
from _common import ps,output_path,ARGS,REPO

HERE=Path(__file__).resolve().parent
NAMES=['line_plot','emphasis_lines','horizontal_bars','grouped_bars','stacked_bars',
       'area_plot','multi_panel','radar_plot','custom_panels']


def main():
    out=output_path(__file__).parent;out.mkdir(parents=True,exist_ok=True)
    book=fitz.open();report=[];cards=[]
    for name in NAMES:
        runpy.run_path(str(HERE/f'{name}.py'),run_name='__main__')
        path=out/f'{name}.pdf'
        layout=json.loads(path.with_suffix('.layout.json').read_text())
        with fitz.open(path) as doc:
            page=doc[0];w,h=page.rect.width,page.rect.height;sizes=set();fonts=set();footer_spans=0
            for font in page.get_fonts():assert doc.extract_font(font[0])[-1],(name,font)
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        size=round(span['size'],3);sizes.add(size);fonts.add(span['font'])
                        assert size in [7,8,10],(name,span)
                        assert span['font'] in ['ArialMT','Arial-BoldMT','Arial-ItalicMT','STIXGeneral-Regular','STIXNonUnicode-Italic'],(name,span)
                        rect=fitz.Rect(span['bbox'])
                        assert page.rect.contains(rect),(name,'outside page',span)
                        if layout['footer_top_pt'] is not None and rect.y0>=layout['footer_top_pt']-2:
                            assert size==8 and span['font']=='ArialMT',(name,span)
                            footer_spans+=1
            assert (footer_spans==0 if ARGS.minimal else footer_spans>=2) and 10 in sizes,(name,sizes)
            sheet=book.new_page(width=14*72,height=max(10*72,h+72))
            sheet.show_pdf_page(fitz.Rect((sheet.rect.width-w)/2,36,(sheet.rect.width+w)/2,36+h),doc,0)
            report.append(dict(template=name,width_pt=w,height_pt=h,fonts=sorted(fonts),
                font_sizes_pt=sorted(sizes),footer_spans=footer_spans,pdf_fonts_embedded=True,
                text_inside_page=True,layout=layout))
        cards.append(f'<section><h2>{html.escape(name)}.py</h2><p><a href="../../../templates/{name}.py">Starter script</a> · <a href="{name}.pdf">PDF</a> · <a href="{name}.png">PNG</a> · <a href="{name}.svg">SVG</a></p><div class="scroll"><img src="{name}.svg" width="{w*96/72:.4f}" height="{h*96/72:.4f}" alt="{html.escape(name.replace("_"," "))} template"></div></section>')
        print('Rendered and verified',name,flush=True)
    book.set_toc([[1,name.replace('_',' ').title(),i+1] for i,name in enumerate(NAMES)])
    book.set_metadata({'title':'Reusable plotting templates - selected R1 style','author':'plotting_resources'})
    book.save(out/'template-examples.pdf',garbage=4,deflate=True);book.close()
    (out/'gallery.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reusable plotting templates</title><style>
body{font:11pt/1.5 Arial,sans-serif;background:white;color:#282828;margin:32px}main{max-width:1320px;margin:auto}h1{font-size:22pt}h2{font-size:16pt}a{color:#285F96}.scroll{overflow-x:auto}img{display:block;max-width:none}section{margin:36px 0 56px}p{max-width:760px}
</style><main><h1>Reusable plotting templates</h1><p>Nine starters using the selected blue backgrounds, R1 palette, 10 pt Arial and 8 pt source/notes. Edit the data and captions; the shared module handles layout and exports. All values here are illustrative.</p><p><a href="../../../templates/README.md">Quick start</a> · <a href="template-examples.pdf">Combined PDF</a> · <a href="plotting-template-starter-kit.zip">Portable starter kit</a></p><p>Images retain native dimensions. View at 100% zoom; wide figures scroll on smaller screens.</p>'''+''.join(cards)+'</main></html>')
    (out/'validation.json').write_text(json.dumps(dict(templates=report,
        selected_style_sha256=hashlib.sha256((ps.ROOT/'selected_style.json').read_bytes()).hexdigest()),indent=2)+'\n')
    with zipfile.ZipFile(out/'plotting-template-starter-kit.zip','w',zipfile.ZIP_DEFLATED) as archive:
        paths=[REPO/'pyproject.toml',REPO/'LICENSE',REPO/'README.md',*HERE.glob('*.py'),HERE/'README.md',HERE/'requirements.txt']
        paths.extend(p for p in (REPO/'src/plotting_resources').glob('*') if p.is_file())
        for path in paths:archive.write(path,'plotting_resources/'+path.relative_to(REPO).as_posix())
    print('Complete:',out/'template-examples.pdf',flush=True)


if __name__=='__main__':main()
