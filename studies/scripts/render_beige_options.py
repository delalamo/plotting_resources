"""Five background proofs, with all other theme settings held fixed.

Run: python figures4papers-minimal/render_beige_options.py
Writes beige-options/; never replaces the accepted theme or its current exports.
"""
from contextlib import contextmanager
from dataclasses import replace
from html import escape
from pathlib import Path
import hashlib
import json

import render_examples as r
import minimal_theme as theme
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle
import numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'beige-options'
SHADES=[
    {'id':'A','name':'Ivory','color':'#FCFAF5','note':'Lightest'},
    {'id':'B','name':'Light cream','color':'#FAF6EE','note':'Selected'},
    {'id':'C','name':'Original beige','color':'#F7F2E8','note':'Previous'},
    {'id':'D','name':'Soft sand','color':'#F0E8DA','note':'Darker'},
    {'id':'E','name':'Warm linen','color':'#E8DDCA','note':'Darkest'},
]


@contextmanager
def shade_context(shade):
    saved_theme,saved_render=theme.T,r.T
    variant=replace(saved_theme,background=shade['color'])
    try:
        theme.T=r.T=variant
        with mpl.rc_context():
            theme.apply_theme()
            yield
    finally:
        theme.T=saved_theme
        r.T=saved_render


def overview():
    """Native vector charts, identical positions and sizes in all five columns."""
    theme.apply_theme()
    fig,axes=plt.subplots(2,5,figsize=(17.5,8.0))
    fig.subplots_adjust(left=.045,right=.985,bottom=.13,top=.73,
                        hspace=.48,wspace=.30)
    fig.text(.045,.95,'Beige options — B selected',fontsize=22,weight='normal')
    fig.text(.045,.905,'Same data, colors, borders, grids, and type. Only the panel background changes.',
             fontsize=11,color=theme.T.muted)
    d=r.post.data_posttraining
    bars=r.raw.data_comparison_IEDB
    for col,shade in enumerate(SHADES):
        left=axes[0,col].get_position().x0
        fig.add_artist(Rectangle((left,.805),.033,.052,transform=fig.transFigure,
                                 facecolor=shade['color'],edgecolor='black',linewidth=.55))
        fig.text(left+.043,.843,f"{shade['id']}  {shade['name']}",fontsize=11,
                 weight='bold' if shade['id']=='B' else 'normal')
        fig.text(left+.043,.816,shade['color'],fontsize=9,color=theme.T.muted)
        fig.text(left,.767,shade['note'],fontsize=9,color=theme.T.muted)
        with shade_context(shade):
            ax=axes[0,col]
            ax.axhline(d['results'][0,0],color='#888888',lw=.8,ls=(0,(4,3)))
            for color,y in zip(theme.PALETTES['methods'],d['results']):
                ax.plot(d['steps'],y,color=color,marker='o',markersize=3.5,lw=1.15)
            ax.set(xlim=(-25,825),ylim=(0,63),xticks=[0,400,800],yticks=[0,20,40,60],
                   xlabel='Post-training steps')
            if col==0: ax.set_ylabel('Performance')
            theme.style_axes(ax)
            ax=axes[1,col]
            ax.bar(np.arange(9),bars['mean'][:,0],width=.77,
                   color=theme.PALETTES['comparison'],edgecolor='none',
                   yerr=bars['std'][:,0],
                   error_kw=dict(elinewidth=.65,ecolor=theme.T.ink,capsize=2,capthick=.65))
            ax.set(ylim=(.5,.9),yticks=[.5,.6,.7,.8,.9],xticks=[],xlabel='Same nine methods')
            if col==0: ax.set_ylabel('AUROC')
            theme.style_axes(ax)
    fig.text(.045,.055,'B / light cream (#FAF6EE) is the approved background. C is the earlier beige.',
             fontsize=10,color=theme.T.muted)
    fig.text(.045,.025,'Figures adapted from Chen Liu / figures4papers. Original data retained. CC BY-NC 4.0.',
             fontsize=8,color=theme.T.muted)
    return fig


def html_gallery():
    buttons=[]
    for shade in SHADES:
        sid=shade['id']
        buttons.append(f'''<button type="button" data-shade="{sid}" aria-pressed="{'true' if sid=='B' else 'false'}">
          <span class="swatch" style="background:{shade['color']}"></span>
          <b>{sid} · {shade['name']}</b><small>{shade['note']} · {shade['color']}</small></button>''')
    sections=[]
    for name,title,_ in r.EXAMPLES:
        sections.append(f'''<section><h2>{escape(title)}</h2><div class="pair">
          <figure><figcaption>B · Approved light cream · #FAF6EE</figcaption>
            <a href="B/{name}.png"><img src="B/{name}.png" alt="{escape(title)} in approved light cream"></a></figure>
          <figure><figcaption class="chosen-caption">B · Light cream · #FAF6EE</figcaption>
            <a class="chosen-link" data-name="{name}" href="B/{name}.png">
            <img class="chosen-image" data-name="{name}" src="B/{name}.png" alt="{escape(title)} in selected beige"></a></figure>
          </div></section>''')
    pdf_links=' · '.join(f'<a href="{s["id"]}/gallery.pdf">{s["id"]}: {s["name"]}</a>' for s in SHADES)
    html='''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Beige options A–E</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#fafafa;color:#282828;font:15px/1.5 Helvetica,Arial,sans-serif}
main{max-width:1500px;margin:auto;padding:36px 28px}h1{font-weight:400;font-size:34px;margin:0 0 8px}h2{font-size:20px;font-weight:400}p{color:#666}a{color:#246c68;text-underline-offset:3px}
.chooser{display:flex;gap:10px;position:sticky;top:0;background:#fafafa;padding:14px 0;z-index:5;flex-wrap:wrap}
button{flex:1;min-width:160px;text-align:left;background:white;border:1px solid #d5d5d5;border-radius:4px;padding:12px;cursor:pointer;font:inherit;color:inherit}
button[aria-pressed=true]{outline:2px solid #246c68;outline-offset:-2px}button b{display:block;font-weight:500}button small{display:block;color:#666}.swatch{display:block;height:30px;border:1px solid #000;margin-bottom:8px}
section{background:white;padding:20px;margin-top:24px;border:1px solid #e5e5e5}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}figcaption{font-size:12px;color:#666;margin-bottom:12px}img{display:block;width:100%;height:auto}.overview{margin:20px 0}.links{font-size:13px}
@media(max-width:800px){.pair{grid-template-columns:1fr}.chooser{position:static}main{padding:20px 12px}}
</style><main><h1>Beige options — B selected</h1>
<p>B / light cream (#FAF6EE) is the approved background. The alternatives remain available for reference.
Select a shade to compare all six figures against the approved background.</p>
<p><a href="comparison.pdf">Comparison sheet (PDF)</a> · <a href="comparison.png">Comparison sheet (PNG)</a></p>
<div class="chooser">'''+''.join(buttons)+'''</div>
<p class="links">Complete six-figure PDF sets: '''+pdf_links+'''</p>
<a href="comparison.png"><img class="overview" src="comparison.png" alt="Five beige shades compared on identical line and bar charts"></a>
'''+''.join(sections)+'''
<p class="links">Adapted from Chen Liu / figures4papers, CC BY-NC 4.0. The main gallery uses the approved shade B.</p>
</main><script>
const shades='''+json.dumps({s['id']:s for s in SHADES})+''';
document.querySelectorAll('[data-shade]').forEach(button=>button.addEventListener('click',()=>{
  const id=button.dataset.shade,s=shades[id];
  document.querySelectorAll('[data-shade]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  document.querySelectorAll('.chosen-caption').forEach(c=>c.textContent=`${id} · ${s.name} · ${s.color}`);
  document.querySelectorAll('.chosen-image').forEach(i=>i.src=`${id}/${i.dataset.name}.png`);
  document.querySelectorAll('.chosen-link').forEach(a=>a.href=`${id}/${a.dataset.name}.png`);
}));
</script></html>'''
    (OUT/'gallery.html').write_text(html)


def main():
    OUT.mkdir(exist_ok=True)
    protected=[ROOT/'gallery.pdf',ROOT/'gallery-beige.pdf',ROOT/'minimal_theme.py']
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    checks=[]
    fig=overview()
    fig.savefig(OUT/'comparison.png',dpi=180)
    fig.savefig(OUT/'comparison.pdf')
    plt.close(fig)
    for shade in SHADES:
        dest=OUT/shade['id'];dest.mkdir(exist_ok=True)
        with shade_context(shade),PdfPages(dest/'gallery.pdf',metadata={
                'Title':f"Beige {shade['id']} - {shade['name']} {shade['color']}",
                'Author':'Adapted from Chen Liu / figures4papers'}) as pdf:
            for name,title,render in r.EXAMPLES:
                fig=render()
                for ax in fig.axes:
                    if ax.name!='polar':
                        assert np.allclose(ax.get_facecolor(),to_rgba(shade['color']))
                for artist in fig.artists:
                    if isinstance(artist,Rectangle):
                        assert np.allclose(artist.get_facecolor(),to_rgba(shade['color']))
                fig.savefig(dest/f'{name}.png',dpi=180)
                pdf.savefig(fig,dpi=300)
                checks.append(f"{shade['id']}/{name}: correct panel background")
                plt.close(fig)
        print(f"Rendered {shade['id']}: {shade['name']} {shade['color']}",flush=True)
    html_gallery()
    after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    assert before==after,'Accepted style or gallery changed'
    (OUT/'shades.json').write_text(json.dumps({'shades':SHADES,'selected_id':'B','fixed_settings':{
        'font':theme.FONT,'frame_pt':theme.T.frame,'grid_color':theme.T.grid_color,
        'palettes':theme.PALETTES},'checks':checks,'accepted_files_unchanged':before==after},indent=2)+'\n')


if __name__=='__main__':
    main()
