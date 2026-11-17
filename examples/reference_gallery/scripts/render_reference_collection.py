"""Rebuild all current-style reference sets and assemble one review PDF.

Single charts remain at their native 6.25-inch width, paired on common-size
pages. The larger repository charts are placed at native scale on full pages.
Historical exploration galleries are not regenerated.
"""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/figures4papers-mpl')
import hashlib
import html
import json
import shutil
import zipfile
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import RendererAgg
import pymupdf as fitz
from PIL import Image
import render_multipanel_examples as mp
import render_urban_samples as urban

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'reference-review-10pt'
CHARTS=OUT/'figures'; TEMP=OUT/'tmp'; PREVIEWS=OUT/'previews'
BOOK='reference-figures-r1-s3-arial-10pt.pdf'
W,H=14*72,10*72
S=mp.S; INK=mp.INK; BG=mp.BG; BLUE=mp.BLUE; MUTED=mp.MUTED
DATA=json.loads((ROOT/'data.json').read_text())
HIGHLIGHTS=json.loads((ROOT/'emphasis-examples/data.json').read_text())
URBAN=json.loads((ROOT/'urban-style-samples/data-and-sources.json').read_text())
CHECKS=[]; RECORDS=[]
DASHES=[(0,(4,2)),(0,(3,1.5,1,1.5)),(0,(1,2)),(0,(6,2)),(0,(3,2,1,2))]


def axes(left=.65,right=.12,top=.30,bottom=.56,grid='xy'):
    f=plt.figure(figsize=(6.25,4.35))
    return f,mp.add_axes(f,left,bottom,6.25-left-right,4.35-top-bottom,grid)


def prepare_urban(index,wb):
    builders=[lambda:urban.make_urban_bars(wb),lambda:urban.make_urban_paired(wb),
              lambda:urban.make_urban_debt(wb),lambda:urban.make_ours_training(DATA),
              lambda:urban.make_ours_benchmark(DATA),lambda:urban.make_ours_emphasis(HIGHLIGHTS)]
    f,values=builders[index]()
    assert values==URBAN[index]['data'],URBAN[index]['id']
    ax=f.axes[0]
    # Make room for the larger current label size without shrinking any text.
    if index==0:ax.set_position([2.30/6.25,.16/4.35,(6.25-2.30-.10)/6.25,(4.35-.10-.16)/4.35])
    if index==4:ax.set_position([1.64/6.25,.16/4.35,(6.25-1.64-.10)/6.25,(4.35-.10-.16)/4.35])
    if index==5:ax.set_position([.58/6.25,.56/4.35,(6.25-.58-1.42)/6.25,(4.35-.16-.56)/4.35])
    for t in f.findobj(Text):
        t.set_fontfamily('Arial');t.set_fontsize(10);t.set_fontweight('normal')
    for label in (ax.xaxis.label,ax.yaxis.label):label.set_fontweight('bold')
    ax.xaxis.labelpad=8;ax.yaxis.labelpad=4
    return f,values


def focus(d):
    n=len(d['references'])+1
    top=.77 if n>6 else .64
    f,ax=axes(left=.69,top=top,bottom=.60)
    grays=['#'+f'{int(v):02x}'*3 for v in np.rint(np.linspace(119,183,n-1))]
    refs=[]
    for i,(ref,c) in enumerate(zip(d['references'],grays)):
        ln,=ax.plot(d['x'],ref['y'],color=c,lw=S['line'],ls=DASHES[i%len(DASHES)],
                   marker=ref.get('marker','o') if d['markers'] else None,
                   markevery=d['markevery'],ms=S['marker'],mfc=BG,mec=c,mew=.625,
                   alpha=1,zorder=2,label=ref['name'])
        refs.append(ln);assert np.array_equal(ln.get_ydata(),ref['y'])
    ln,=ax.plot(d['x'],d['focus']['y'],color=BLUE,lw=S['line'],ls='-',
               marker='o' if d['markers'] else None,markevery=d['markevery'],
               ms=S['marker'],mfc=BG,mec=BLUE,mew=.625,zorder=4,label=d['focus']['name'])
    assert np.array_equal(ln.get_ydata(),d['focus']['y'])
    ax.set(xscale=d['xscale'],xlim=d['xlim'],ylim=d['ylim'],xticks=d['xticks'],yticks=d['yticks'],
           xlabel=d['xlabel'],ylabel=d['ylabel'])
    if d['xscale']=='log':
        ax.set_xticklabels(['0.001','0.01','0.1','1','10']);ax.minorticks_off()
    handles=[ln]+refs;cols=2 if n<=4 else 3
    f.legend(handles=mp.row_major_handles(handles,cols),loc='upper left',
             bbox_to_anchor=(.69/6.25,.985,(6.25-.69-.12)/6.25,0),mode='expand',
             borderaxespad=0,borderpad=0,ncols=cols,handlelength=1.6,labelspacing=.6,columnspacing=1)
    return f,d


def original_training():
    d=DATA['posttraining'];f=plt.figure(figsize=(13,4.6))
    ax=mp.add_axes(f,.85,.60,11.9,3.30)
    ref=ax.axhline(d['results'][0][0],color='#979797',lw=S['line'],ls=(0,(4,3)),label='SFT only')
    handles=[]
    for method,color,y in zip(d['methods'],S['assignments']['methods'],d['results']):
        ln,=ax.plot(d['steps'],y,color=color,marker='o',label=method,lw=S['line'],ms=S['marker'],
                   mfc=BG,mec=color,mew=.625)
        assert np.array_equal(ln.get_ydata(),y);handles.append(ln)
    ax.set(xlabel='Post-training steps',ylabel='Performance',xticks=d['steps'],yticks=[0,20,40,60],
           ylim=(0,63),xlim=(-25,825))
    f.legend(handles=handles+[ref],loc='upper left',bbox_to_anchor=(.85/13,.985,11.9/13,0),
             mode='expand',borderaxespad=0,borderpad=0,ncols=4,handlelength=2)
    return f,d


def radar():
    d=DATA['radar'];names=list(d['results']);bench=[n.split('\n')[1] for n in names]
    levels={'POPE$_{Adv}$':[75,80,85,91],'MathVista':[30,40,50,61],'MMBench':[40,55,70,85]}
    angles=np.linspace(2*np.pi,0,len(names),endpoint=False);closed=np.r_[angles,angles[0]]
    def radius(v,b):return 45+45*np.clip((v-levels[b][0])/(levels[b][-1]-levels[b][0]),0,1)
    f=plt.figure(figsize=(13,7.5))
    f.add_artist(Rectangle((.04,.055),.92,.89,transform=f.transFigure,facecolor=BG,
                           edgecolor=S['frame_color'],lw=S['frame_width'],zorder=-1))
    ax=f.add_axes([.30,.175,.40,.64],projection='polar');ax.patch.set_visible(False)
    ax.set_theta_zero_location('N');ax.set(ylim=(45,90),xticks=[],yticks=[]);ax.grid(False)
    for sp in ax.spines.values():sp.set_visible(False)
    for a in angles:ax.plot([a,a],[45,90],color=S['grid_color'],lw=S['grid_width'],ls=':',zorder=1)
    for k in range(1,4):
        rr=[radius(levels[b][k],b) for b in bench]
        ax.plot(closed,np.r_[rr,rr[0]],color=S['grid_color'],lw=S['grid_width'],ls=':',zorder=1)
    normalized=[]
    for method,color,m in zip(d['methods'],S['assignments']['methods'],range(3)):
        rr=[radius(d['results'][n][m],b) for n,b in zip(names,bench)]
        ln,=ax.plot(closed,np.r_[rr,rr[0]],color=color,lw=S['line'],marker=['s','^','o'][m],
                    ms=S['marker'],mfc=BG,mec=color,mew=.625,label=method,zorder=3)
        ax.fill(closed,np.r_[rr,rr[0]],color=color,alpha=S['radar_alpha'],zorder=2)
        assert np.array_equal(ln.get_ydata(),np.r_[rr,rr[0]]);normalized.append(rr)
    for a,b,name in zip(angles,bench,names):
        for v in levels[b][1:]:
            ax.text(a,radius(v,b)+1.4,str(v),color=MUTED,fontsize=10,rotation=np.degrees(a),
                    rotation_mode='anchor',ha='center',va='center',clip_on=False,
                    bbox=dict(facecolor=BG,edgecolor='none',pad=.2))
        ax.text(a,101+14*abs(np.sin(a)),name,fontsize=10,ha='center',va='center',clip_on=False,linespacing=1.3)
    f.legend(*ax.get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.10,.985,.80,0),
             mode='expand',borderaxespad=0,borderpad=0,ncols=3,handlelength=2)
    f.canvas.draw();renderer=f.canvas.get_renderer()
    for text in ax.texts:
        box=text.get_window_extent(renderer)
        assert box.y0/f.bbox.height>.055 and box.y1/f.bbox.height<.945
    return f,dict(source=d,normalized_radii=normalized,benchmark_levels=levels)


def check_figure(f,spec,math=False,polar=False):
    f.canvas.draw();r=f.canvas.get_renderer();ts=[];boxes=[]
    assert np.allclose(f.get_facecolor(),mpl.colors.to_rgba(S['canvas']))
    title_text={a.get_title(loc='left') for a in f.axes}
    title_text.update(t.get_text() for a in f.axes for t in [a.xaxis.label,a.yaxis.label])
    title_text.update(['Model (see numbered color key)','Cumulative publication count'])
    for t in f.findobj(Text):
        if not t.get_visible() or not t.get_text():continue
        assert t.get_fontsize()==10,(spec['id'],t.get_text(),t.get_fontsize())
        assert t.get_fontfamily()==['Arial'],(spec['id'],t.get_text(),t.get_fontfamily())
        expected='bold' if t.get_text() in title_text else 'normal'
        assert t.get_fontweight()==expected,(spec['id'],t.get_text(),t.get_fontweight())
        box=Text.get_window_extent(t,r)
        assert box.x0>=-1 and box.y0>=-1 and box.x1<=f.bbox.width+1 and box.y1<=f.bbox.height+1,(spec['id'],t.get_text(),'outside')
        ts.append(t);boxes.append(box)
    overlaps=[(ts[i].get_text(),ts[j].get_text()) for i,a in enumerate(boxes) for j,b in enumerate(boxes[i+1:],i+1) if a.overlaps(b)]
    assert not overlaps,(spec['id'],'overlapping text',overlaps)
    if not polar:
        for a in f.axes:
            assert np.allclose(a.get_facecolor()[:3],mpl.colors.to_rgb(BG))
            assert all(s.get_visible() and s.get_linewidth()==.45 for s in a.spines.values())
    CHECKS.append(dict(id=spec['id'],slug=spec['slug'],panels=len(f.axes),size_inches=f.get_size_inches().tolist(),
                       base_font='Arial',base_size_pt=10,only_titles_bold=True,math=math,
                       text_inside_canvas=True,text_overlaps=0,spacing=f._layout_audit,
                       canvas_color=S['canvas'],panel_color=BG))


def save_chart(f,spec,values,math=False,polar=False):
    if not hasattr(f,'_layout_audit'):mp.compact_layout(f,spec['slug'])
    check_figure(f,spec,math,polar)
    for ext in ['pdf','png','svg']:
        with mpl.rc_context({'svg.fonttype':'path' if math else 'none'}):
            f.savefig(CHARTS/f'{spec["slug"]}.{ext}',dpi=300)
    plt.close(f)
    RECORDS.append({k:v for k,v in spec.items() if k!='builder'}|{'data':values})


def wrap(text,width,weight='normal',size=10):
    renderer=RendererAgg(10,10,72);prop=FontProperties(family='Arial',size=size,weight=weight)
    lines=[]
    for para in text.split('\n'):
        line=''
        for word in para.split():
            candidate=(line+' '+word).strip()
            if line and renderer.get_text_width_height_descent(candidate,prop,ismath=False)[0]>width:
                lines.append(line);line=word
            else:line=candidate
        lines.append(line)
    return '\n'.join(lines)


def page_text(f,x,top,text,width=936,bold=False,color=INK,size=10):
    weight='bold' if bold else 'normal'
    t=f.text(x/W,1-top/H,wrap(text,width,weight,size),ha='left',va='top',fontsize=size,
             fontweight=weight,color=color,linespacing=1.3)
    f.canvas.draw();bottom=H-t.get_window_extent(f.canvas.get_renderer()).y0*72/f.dpi
    return bottom


def page_base(number,title):
    f=plt.figure(figsize=(14,10))
    page_text(f,36,18,'REFERENCE FIGURES  /  R1 + S3  /  10 PT ARIAL',color=BLUE)
    page_text(f,36,40,title,bold=True)
    page_text(f,36,692,'Native chart scale preserved. Math scripts use conventional reduced sizes.',color=MUTED)
    page_text(f,946,692,f'{number:02}',width=26,color=MUTED)
    return f


def compose_page(f,placements,name):
    path=TEMP/f'{name}.pdf';f.savefig(path);plt.close(f);page=fitz.open(path)
    for spec,x,top in placements:
        with fitz.open(CHARTS/f'{spec["slug"]}.pdf') as chart:
            cw,ch=chart[0].rect.width,chart[0].rect.height
            page[0].show_pdf_page(fitz.Rect(x,top,x+cw,top+ch),chart,0)
    return page


def pair_page(left,right,number,title):
    if mp.MINIMAL:
        f=plt.figure(figsize=(14,10))
        return compose_page(f,[(left,36,36),(right,522,36)],f'page-{number:02}')
    f=page_base(number,title);placements=[]
    # Each chart is 6.25 inches wide. No resize is applied during insertion.
    header_bottoms=[]
    for x,s in zip([36,522],[left,right]):
        bottom=page_text(f,x,80,s['id']+'  '+s['title'],450,bold=True)
        bottom=page_text(f,x,bottom+3,s['subtitle'],450)
        assert bottom<157,(s['id'],'header too tall',bottom)
        header_bottoms.append(bottom)
    top=max(header_bottoms)+6
    for x,s in zip([36,522],[left,right]):
        placements.append((s,x,top))
        with fitz.open(CHARTS/f'{s["slug"]}.pdf') as d:ch=d[0].rect.height
        bottom=page_text(f,x,top+ch+10.5,s['source'],450,size=mp.T['sources_pt'])
        bottom=page_text(f,x,bottom+6,s['notes'],450,color=MUTED,size=mp.T['notes_pt'])
        assert bottom<675,(s['id'],'notes too tall',bottom)
    return compose_page(f,placements,f'page-{number:02}')


def wide_page(s,number):
    if mp.MINIMAL:return fitz.open(CHARTS/f'{s["slug"]}.pdf')
    f=plt.figure(figsize=(14,10))
    bottom=page_text(f,36,15,s['id']+'  /  '+s['group'].upper(),color=BLUE)
    with fitz.open(CHARTS/f'{s["slug"]}.pdf') as d:cw=d[0].rect.width
    bottom=page_text(f,36,bottom+8,s['title'],width=cw,bold=True)
    bottom=page_text(f,36,bottom+3,s['subtitle'],width=cw)
    top=bottom+6
    with fitz.open(CHARTS/f'{s["slug"]}.pdf') as d:ch=d[0].rect.height
    bottom=page_text(f,36,top+ch+7.5,s['source'],width=cw,size=mp.T['sources_pt'])
    bottom=page_text(f,36,bottom+6,s['notes'],width=cw,color=MUTED,size=mp.T['notes_pt'])
    assert bottom<681,(s['id'],'wide-page overflow',bottom)
    page_text(f,36,692,'Native chart scale preserved. Math scripts use conventional reduced sizes.',color=MUTED)
    page_text(f,946,692,f'{number:02}',width=26,color=MUTED)
    return compose_page(f,[(s,36,top)],f'page-{number:02}')


def intro():
    f=page_base(1,'Current Plotting References - Complete Review Collection')
    y=page_text(f,36,82,'Sixteen examples rebuilt with the selected style. The collection includes the earlier Urban/template samples, all four blue-and-gray references, the remaining repository templates, and the four multi-panel figures.',660)
    y=page_text(f,36,y+20,'Typography',bold=True)
    y=page_text(f,36,y+10,'Figure labels and values are 10 pt Arial; source credits and notes are 8 pt Arial. Figure, panel and axis titles are bold. Other text is regular weight. Equations use Arial and Arial Italic letters, with STIX only for symbols Arial lacks; their base is 10 pt and scripts reduce conventionally.',660)
    y=page_text(f,36,y+20,'Reading This Document',bold=True)
    y=page_text(f,36,y+10,'Every page is 14 x 10 inches. Paired single charts are each 6.25 inches wide; figures 11, 12 and 16 now use text width too. Three dense multi-panel exceptions remain 13 inches wide. All charts are inserted at native size. The font size is therefore identical across pages at the same PDF zoom. Sources and synthetic-data labels accompany every figure.',660)
    y=page_text(f,36,y+24,'Contents',bold=True)
    contents=[('02','U1-U2','Spending categories and policy scenarios'),('03','U3-T1','Home-equity debt and directly labeled training curves'),
              ('04','T2-T3','Ranked benchmark and directly labeled focus example'),('05','H1-H2','Blue-and-gray benchmark and learning curves'),
              ('06','H3-H4','Trajectory context and crossing response curves'),('07','P1','Repository radar comparison'),
              ('08','P2','Repository post-training comparison'),('09-12','M1-M4','Four multi-panel repository figures'),('13','Style','Typography, palette and export notes')]
    for p,ids,title in contents:
        y+=20;page_text(f,36,y,p,width=54);page_text(f,104,y,ids,width=74);page_text(f,190,y,title,width=730)
    return compose_page(f,[],'intro')


def style_page(number):
    f=page_base(number,'Style and Verification Notes')
    y=80
    for heading,body in [
        ('Type','10 pt Arial Regular for values, annotations, ticks, legends and subtitles. Source credits and notes use 8 pt Arial Regular. Arial Bold for figure, panel and axis titles. Arial Italic supplies mathematical variables; STIX supplies missing mathematical symbols. Equations have a 10 pt base, with conventional 7 pt scripts.'),
        ('Marks and Panels',f'Plot panels {BG}; full figure background {S["canvas"]}, including titles, legends and source notes. Four-sided frame #566C7B at 0.45 pt; dotted grid #CBD6DF at 0.45 pt. Curves 1.25 pt; error bars 0.65 pt with 2 pt caps; open markers 3.5 pt. The radar uses radial guides inside a rectangular panel.'),
        ('Emphasis','The emphasized series is cobalt #285F96. Comparisons use opaque neutral grays from #777777 to #B7B7B7. All curves remain 1.25 pt. Solid cobalt is drawn last; reference lines use dashes. Choosing a focus does not imply that it has the highest value.'),
        ('Layout','Legends sit below the plots, 7.5 pt beneath the lowest axis label; multiple legend groups have 4.5 pt between them. Titles and subtitles have a 3 pt gap. Subtitles sit 8.25 pt above the chart content, including panel headings. Direct labels remain in T1 and T3. Comparable panels retain equal sizes and scales, 6 pt horizontal gaps and 6 pt x-axis and 4 pt y-axis title padding.'),
        ('Data and Exports','Existing arrays and supplied uncertainty values are unchanged. H2-H4 and T3 are explicitly synthetic. The radar preserves the original benchmark-specific radial scales. PDF fonts are embedded; SVGs with math use outlined glyphs for portability. PNGs are 300 dpi. Validation covers font sizes and weights, page bounds, label overlaps and source data.'),
    ]:
        y=page_text(f,36,y,heading,bold=True)+10
        y=page_text(f,36,y,body,890)+22
    page_text(f,36,y,'Core R1 Colors',bold=True);y+=26
    for i,(name,c) in enumerate(zip(S['palette']['names'],S['palette']['colors'])):
        x=36+i*150
        f.add_artist(Rectangle((x/W,1-(y+20)/H),110/W,20/H,transform=f.transFigure,
                               facecolor=c,edgecolor=S['frame_color'],lw=.45))
        page_text(f,x,y+27,name,140);page_text(f,x,y+44,c,140,color=MUTED)
    assert y+60<680,y
    return compose_page(f,[],f'page-{number:02}')


def append_page(book,page,index):
    page[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(PREVIEWS/f'page-{index:02}.png')
    book.insert_pdf(page);page.close()


def verify_pdf(path):
    report=[]
    with fitz.open(path) as doc:
        for i,page in enumerate(doc):
            fonts=set();sizes=set();count=0
            for font in page.get_fonts():assert doc.extract_font(font[0])[-1],(i,font)
            for b in page.get_text('dict')['blocks']:
                for line in b.get('lines',[]):
                    for span in line['spans']:
                        size=round(span['size'],3);sizes.add(size);fonts.add(span['font']);count+=1
                        assert size in ([7,10] if path.parent==CHARTS else [7,8,10]),(path,i,span)
                        if size==8:assert span['font']=='ArialMT',span
                        assert span['font'] in ['ArialMT','Arial-BoldMT','Arial-ItalicMT','STIXGeneral-Regular','STIXNonUnicode-Italic'],(path,i,span)
                        box=fitz.Rect(span['bbox']);assert box.x0>=-1 and box.y0>=-1 and box.x1<=page.rect.width+1 and box.y1<=page.rect.height+1,(path,i,span)
            report.append(dict(page=i+1,fonts=sorted(fonts),sizes_pt=sorted(sizes),spans=count,fonts_embedded=True,text_inside_page=True))
    return report


def gallery():
    cards=[]
    for i in range(1,14):
        cards.append(f'<section><h2>Page {i:02}</h2><a href="previews/page-{i:02}.png"><img src="previews/page-{i:02}.png" alt="Review page {i}"></a></section>')
    (OUT/'gallery.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Complete reference review</title>
<style>body{font:10pt/1.5 Arial,sans-serif;color:#282828;background:'''+S['canvas']+''';margin:30px}main{max-width:1344px;margin:auto}h1,h2{font-size:10pt}a{color:#285F96}img{width:100%;border:1px solid #CBD6DF}section{margin:30px 0}nav{display:flex;gap:24px;flex-wrap:wrap}</style>
<main><h1>Current-style reference figures</h1><p>Sixteen figures in one document. Figure type is 10 pt Arial, with 8 pt source/notes; mathematical symbols use the documented fallback. Pages and charts retain a consistent physical scale.</p>
<nav><a href="'''+BOOK+'''">Complete PDF</a><a href="reference-figures-source.zip">Figures and source code</a><a href="README.md">Details</a></nav>'''+''.join(cards)+'</main></html>')


def main():
    for folder in [OUT,CHARTS,TEMP,PREVIEWS]:folder.mkdir(parents=True,exist_ok=True)
    mp.setup();urban.axes=axes;wb=urban.workbook_sheets()
    singles=[]
    for i,record in enumerate(URBAN):
        spec={k:v for k,v in record.items() if k!='data'}
        if 'rule' in spec:spec['rule']=spec['rule'].replace('an above-chart legend','a below-chart legend (our layout override)')
        f,values=prepare_urban(i,wb);save_chart(f,spec,values);singles.append(spec)
        print('Rendered',spec['id'],flush=True)
    for d in HIGHLIGHTS:
        titles={'H1':'Original Benchmark','H2':'Learning Curves','H3':'A Trajectory in Context','H4':'Crossing Response Curves'}
        spec=dict(id=d['id'],slug='focus-'+d['slug'],title=titles[d['id']],subtitle=d['subtitle'],
                  group='Blue-and-gray reference',source='Source: '+d['origin'],
                  notes='Cobalt identifies the focus; gray series are comparisons. Every source array is retained. '+('Synthetic illustrative data.' if d['synthetic'] else 'Original repository benchmark values.'))
        f,values=focus(d);save_chart(f,spec,values);singles.append(spec);print('Rendered',spec['id'],flush=True)
    wider=[dict(id='P1',slug='repository-radar',title='Method Comparison Across Models and Benchmarks',
                subtitle='Original 12-spoke radar; each benchmark retains its own scale',group='Repository reference',
                source='Source: Chen Liu, figures4papers / figure_VIGIL/plot_comparison_radar.py. CC BY-NC 4.0.',
                notes='All 36 scores and benchmark-specific radial mappings are preserved. POPE uses 75-91, MathVista 30-61, and MMBench 40-85. Polygon areas are not comparable across benchmarks.',builder=radar),
           dict(id='P2',slug='repository-posttraining',title='Post-Training Performance with the R1 Categorical Palette',
                subtitle='Original five training steps, three methods and the SFT-only baseline',group='Repository reference',
                source='Source: Chen Liu, figures4papers / figure_VIGIL/plot_posttraining.py. CC BY-NC 4.0.',
                notes='All original values are retained. This is the full categorical treatment; T1 uses direct labels and H1 demonstrates blue-and-gray emphasis.',builder=original_training)]
    for i,s in enumerate(wider):
        f,values=s['builder']();save_chart(f,s,values,math=i==0,polar=i==0);print('Rendered',s['id'],flush=True)
    for i,original in enumerate(mp.EXAMPLES):
        spec=original|dict(id=f'M{i+1}',group='Multi-panel repository reference',notes=original['note'])
        f,values=spec['builder']();mp.compact_layout(f,spec['slug']);mp.validate(f,spec,values);save_chart(f,spec,values,math=i==2)
        wider.append(spec);print('Rendered',spec['id'],flush=True)
    book=fitz.open();append_page(book,intro(),1)
    pair_titles=['Urban References: Bars and Policy Comparisons','Urban and Template References: Categorical Lines',
                 'Template References: Ranked Bars and a Highlighted Curve','Emphasis References: Benchmarks and Learning',
                 'Emphasis References: Trajectories and Parameter Response']
    for i in range(5):append_page(book,pair_page(singles[2*i],singles[2*i+1],i+2,pair_titles[i]),i+2)
    for i,s in enumerate(wider,7):append_page(book,wide_page(s,i),i)
    append_page(book,style_page(13),13)
    book.set_metadata({'title':'Current reference figures - R1 / S3 / Arial 10 pt','author':'Sources credited with each figure'})
    toc=[[1,'Contents and typography',1]]
    toc += [[1,t,i+2] for i,t in enumerate(pair_titles)]
    toc += [[1,s['id']+' '+s['title'],i] for i,s in enumerate(wider,7)]
    toc += [[1,'Style and verification notes',13]];book.set_toc(toc)
    book.save(OUT/BOOK,garbage=4,deflate=True);book.close()
    report=verify_pdf(OUT/BOOK)
    for path in CHARTS.glob('*.pdf'):verify_pdf(path)
    (OUT/'font-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'validation.json').write_text(json.dumps(dict(figures=CHECKS,source_data_sha256=hashlib.sha256((ROOT/'data.json').read_bytes()).hexdigest(),
        emphasis_data_sha256=hashlib.sha256((ROOT/'emphasis-examples/data.json').read_bytes()).hexdigest(),
        urban_workbook_sha256=hashlib.sha256((ROOT/'urban-style-samples/sources/StyleGuideGraphs.xlsx').read_bytes()).hexdigest()),indent=2)+'\n')
    (OUT/'data-and-sources.json').write_text(json.dumps(RECORDS,indent=2)+'\n')
    shutil.copyfile(ROOT/'selected-style.json',OUT/'selected-style.json')
    (OUT/'README.md').write_text('''# Complete current-style reference review

[Complete PDF](reference-figures-r1-s3-arial-10pt.pdf) · [Page gallery](gallery.html) · [Figures and source](reference-figures-source.zip)

Sixteen reference figures across thirteen pages: six Urban/template examples, four blue-and-gray samples, two additional repository figures and four multi-panel figures. Current R1/S3 styling is applied throughout. The full figure and page background is #EDF4F9, a paler blue behind titles, subtitles, legends and source notes; plot panels retain #D8E8F4. Prior palette/background explorations are excluded.

Figure text uses 10 pt Arial, except source credits and notes, which use 8 pt Arial Regular. Figure/panel/axis titles are bold; other text is regular. Math uses Arial letters and Arial Italic variables, with STIX symbols only where Arial lacks the glyph. Math has a 10 pt base with conventional 7 pt scripts. The exact fonts in each exported PDF page are recorded in font-verification.json.

Every page is 14 x 10 inches. Single references are paired at native 6.25-inch width; larger repository charts are 13 inches wide. No chart is rescaled when placed in the document. Legends sit below the plots with 7.5 pt clearance from axis labels and 4.5 pt between separate legend groups. Titles and subtitles have a 3 pt gap; subtitles sit 8.25 pt above the chart content. Native chart dimensions retain the approved 75%-height layout. Complete article blocks now fit 8 pt source/notes with equal 13.5 pt top and bottom padding; chart geometry, widths and mark sizes remain fixed. PDF fonts are embedded, PNGs are 300 dpi, and SVGs containing math use outlined glyphs. Other SVGs retain editable text.

Sources, original arrays, synthetic-data disclosures and display adaptations accompany the figures and appear in data-and-sources.json. The Urban workbook is retained; all earlier sample arrays are checked. The radar retains benchmark-specific radial scales. Original repository code/data remain under CC BY-NC 4.0.

Reproduce with `MPLCONFIGDIR=/private/tmp/figures4papers-mpl python figures4papers-minimal/render_reference_collection.py`. Dependencies: Matplotlib, NumPy, SciPy, PyMuPDF, Pillow and installed Arial Regular/Bold/Italic. The renderer imports render_urban_samples.py and render_multipanel_examples.py; source archives contain all required data and the upstream concept code.
''')
    gallery()
    with zipfile.ZipFile(OUT/'reference-figures-source.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in OUT.rglob('*'):
            if path.is_file() and path.suffix!='.zip' and TEMP not in path.parents:z.write(path,'figures4papers-minimal/'+path.relative_to(ROOT).as_posix())
        for rel in ['README.md','text_width.py','figure_height.py','figure-height-baseline.json','render_reference_collection.py','render_urban_samples.py','render_multipanel_examples.py','selected-style.json','data.json',
                    'emphasis-examples/data.json','urban-style-samples/data-and-sources.json','urban-style-samples/sources/StyleGuideGraphs.xlsx',
                    'upstream/figure_VIGIL/plot_concept.py','upstream/LICENSE']:
            z.write(ROOT/rel,'figures4papers-minimal/'+rel)
    print('Complete:',OUT/BOOK,flush=True)


if __name__=='__main__':main()
