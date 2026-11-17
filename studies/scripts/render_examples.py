"""Regenerate six README examples with beige panels and thin black frames.

Run: python render_examples.py
Outputs: figures/{original_name}.{png,pdf,svg}, gallery.pdf, and data.json.
The upstream snapshot is unmodified and is never executed as __main__.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/figures4papers-mpl")
import matplotlib
matplotlib.use("Agg")
import importlib.util
import json
import sys
import shutil
from dataclasses import asdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Patch, Rectangle

from minimal_theme import FONT, FONT_FAMILIES, T, PALETTES, apply_theme, restyle_diagram, style_axes, recolor_manifold


def source(relative):
    path = ROOT / "upstream" / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


raw = source("figure_ImmunoStruct/raw_data.py")
brute = source("figure_Brainteaser/plot_brute_force.py")
radar = source("figure_VIGIL/plot_comparison_radar.py")
post = source("figure_VIGIL/plot_posttraining.py")
concept = source("figure_VIGIL/plot_concept.py")
trend = source("figure_ophthal_review/plot_trend.py")


def bars():
    d = raw.data_comparison_IEDB
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
    fig.subplots_adjust(left=.055, right=.77, bottom=.15, top=.88, wspace=.35)
    limits = [(.5, .9), (.15, .75), (.18, .55)]
    ticks = [[.5, .6, .7, .8, .9], [.2, .3, .4, .5, .6, .7], [.2, .3, .4, .5]]
    for j, ax in enumerate(axes):
        ax.bar(np.arange(9), d['mean'][:, j], width=.77, color=PALETTES['comparison'],
               yerr=d['std'][:, j], edgecolor='none',
               error_kw=dict(elinewidth=T.error, ecolor=T.ink,
                             capsize=2, capthick=T.error))
        ax.set(ylim=limits[j], xticks=[], yticks=ticks[j], ylabel=d['metrics'][j])
        style_axes(ax)
    handles = [Patch(facecolor=c, edgecolor='none', label=n.replace(
        r'BigMHC$_\text{retrained}$', 'BigMHC retrained')) for c,n in zip(PALETTES['comparison'],d['methods'])]
    fig.legend(handles=handles, loc='center left', bbox_to_anchor=(.79,.51),
               labelspacing=.65, handlelength=1.2)
    return fig


def composition():
    fig, axes = plt.subplots(2, 4, figsize=(12, 6.2), sharex=True, sharey=True)
    fig.subplots_adjust(left=.065, right=.99, bottom=.25, top=.92, hspace=.32, wspace=.18)
    colors = PALETTES['composition']
    # Repeated strokes ensure the small PDF legend keys show each pattern.
    hatches = ['/' * 3, '\\' * 3, '', 'x' * 2]
    for row, d in enumerate((brute.data_brute_force_math, brute.data_brute_force_logic)):
        for col, prompt in enumerate(d['prompts']):
            ax = axes[row,col]
            vals=d['result'][prompt]
            bottom=np.zeros(7)
            for subtype in range(4):
                ax.bar(np.arange(7), vals[:,subtype], bottom=bottom, color=colors,
                       width=.78, hatch=hatches[subtype], edgecolor='#707070',
                       linewidth=T.outline, alpha=1 if subtype==0 else .8)
                bottom += vals[:,subtype]
            # Same highlighted quantity as upstream. Place it in a beige callout
            # above the first segment; no yellow type or thick black text halo.
            for x,value in enumerate(vals[:,0]):
                ax.text(x, value+.012, f'{value:.3f}', ha='center', va='bottom',
                        fontsize=6.7, color=T.ink,
                        bbox=dict(facecolor=T.background, edgecolor='none', pad=.4, alpha=.98))
            ax.set(ylim=(0,1.015), xticks=[], yticks=[0,.25,.5,.75,1])
            if row==0:
                ax.set_title(prompt)
            if col==0:
                ax.set_ylabel(('Math' if row==0 else 'Logic')+'\nProbability')
            style_axes(ax)
    method_handles=[Patch(facecolor=c, edgecolor='none', label=n) for c,n in zip(
        colors,brute.data_brute_force_math['methods'])]
    fig.legend(handles=method_handles,loc='lower center',bbox_to_anchor=(.5,.075),
               ncols=3,fontsize=8,handlelength=1.1,columnspacing=1.5)
    subtype_names=['Only model brute force','Only human brute force','Neither brute force','Both brute force']
    subtype_handles=[Patch(facecolor=T.background, edgecolor='#707070', linewidth=T.outline,
                           hatch=h,label=n) for h,n in zip(hatches,subtype_names)]
    fig.legend(handles=subtype_handles,loc='lower center',bbox_to_anchor=(.5,.005),ncols=4,
               fontsize=8,handleheight=1.1)
    return fig


def radar_plot():
    d=radar.data_comparison
    benchmarks={'POPE$_{Adv}$':[75,80,85,91],'MathVista':[30,40,50,61],'MMBench':[40,55,70,85]}
    names=list(d['results'])
    angles=np.linspace(2*np.pi,0,len(names),endpoint=False)
    closed=np.r_[angles,angles[0]]
    bench=[n.split('\n')[1] for n in names]
    def radius(value,b):
        ticks=benchmarks[b]
        return 45+45*np.clip((value-ticks[0])/(ticks[-1]-ticks[0]),0,1)
    fig=plt.figure(figsize=(8.8,7.4))
    # A rectangular panel encloses the radial plot and its outside spoke labels.
    # Keep the polar patch transparent so the beige panel is continuous.
    fig.add_artist(Rectangle((.025,.095),.95,.875,transform=fig.transFigure,
                   facecolor=T.background,edgecolor=T.frame_color,
                   linewidth=T.frame,zorder=-1))
    ax=fig.add_axes([.22,.19,.56,.66],projection='polar')
    ax.patch.set_visible(False)
    ax.set_theta_zero_location('N')
    ax.set(ylim=(45,90),xticks=[],yticks=[])
    ax.grid(False)
    for spine in ax.spines.values(): spine.set_visible(False)
    for a in angles:
        ax.plot([a,a],[45,90],color=T.grid_color,lw=T.grid,zorder=1)
    for k in range(1,4):
        rr=[radius(benchmarks[b][k],b) for b in bench]
        ax.plot(closed,np.r_[rr,rr[0]],color=T.grid_color,lw=T.grid,zorder=1)
    for m,(method,color) in enumerate(zip(d['methods'],PALETTES['methods'])):
        values=[radius(d['results'][n][m],b) for n,b in zip(names,bench)]
        ax.plot(closed,np.r_[values,values[0]],color=color,lw=T.line,
                marker='o',markersize=2.8,label=method,zorder=3)
        ax.fill(closed,np.r_[values,values[0]],color=color,alpha=.035,zorder=2)
    for a,b,n in zip(angles,bench,names):
        for v in benchmarks[b][1:]:
            ax.text(a,radius(v,b)+1.1,str(v),fontsize=6.8,color=T.muted,
                    rotation=np.degrees(a),ha='center',va='center',clip_on=False)
        ax.text(a,90+9+11*abs(np.sin(a)),n,fontsize=T.small,
                ha='center',va='center',clip_on=False,linespacing=1.3)
    fig.legend(*ax.get_legend_handles_labels(),loc='lower center',
               bbox_to_anchor=(.5,.055),ncols=3)
    fig.text(.5,.025,'Each benchmark retains its original radial scale.',
             ha='center',fontsize=8,color=T.muted)
    return fig


def lines():
    d=post.data_posttraining
    fig,ax=plt.subplots(figsize=(5.8,4.6))
    fig.subplots_adjust(left=.16,right=.97,bottom=.16,top=.86)
    ax.axhline(d['results'][0,0],color='#888888',lw=.8,ls=(0,(4,3)),label='SFT only')
    for method,color,y in zip(d['methods'],PALETTES['methods'],d['results']):
        ax.plot(d['steps'],y,color=color,marker='o',label=method,lw=T.line,markersize=T.marker)
    ax.set(xlabel='Post-training steps',ylabel='Performance on highly\nvision-dependent tasks '+r'$\uparrow$',
           xticks=d['steps'],yticks=[0,20,40,60],ylim=(0,63),xlim=(-25,825))
    style_axes(ax)
    fig.legend(*ax.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.55,.99),
               ncols=2,columnspacing=2)
    return fig


def concepts():
    fig,(left,right)=plt.subplots(1,2,figsize=(12,4.5),gridspec_kw={'width_ratios':[1,1.35]})
    fig.subplots_adjust(left=.065,right=.98,bottom=.16,top=.88,wspace=.24)
    # Use exactly the upstream illustrative curves and KDE/manifold generator.
    x=np.linspace(0,1,1000)
    yy=[concept._gauss(x,.30,.07),.30*concept._gauss(x,.30,.12)+.22,concept._gauss(x,.72,.07)]
    labels=[r'$P(y\mid x_t)$',r'$P(y\mid x_v^{\emptyset},x_t)$',r'$P(y\mid x_v,x_t)$']
    for y,c,l in zip(yy,[T.taupe,T.rust,T.teal],labels):
        left.plot(x,y,color=c,label=l,lw=T.line)
        left.fill_between(x,0,y,color=c,alpha=.10,linewidth=0)
    star=.72
    low=np.interp(star,x,yy[1]);high=np.interp(star,x,yy[2])
    left.vlines(star,0,1,lw=.65,linestyle=':',color=T.muted)
    left.annotate('',xy=(star,high),xytext=(star,low),
                  arrowprops=dict(arrowstyle='<->',lw=.75,color=T.ink))
    left.text(star+.045,(low+high)/2,'VIG',fontsize=T.small,va='center')
    left.set(xlim=(0,1.05),ylim=(0,1.08),xticks=[0,.5,1],xticklabels=[-1,0,1],
             yticks=[0,.2,.4,.6,.8,1],xlabel='Answer space (arbitrary units)',ylabel='Probability')
    style_axes(left)
    left.legend(loc='lower left',bbox_to_anchor=(-.02,1.03),ncols=3,fontsize=8,
                handlelength=1.2,columnspacing=1.1)
    concept.plot_manifold(right)
    restyle_diagram(right)
    recolor_manifold(right)
    # Reserve right-side room for the two endpoint labels in the upstream code.
    xmin,xmax=right.get_xlim();right.set_xlim(xmin-.8,xmax+2.0)
    right.set_axis_on()
    right.set_xticks([]);right.set_yticks([])
    style_axes(right,grid='')
    for text in right.texts:
        if text.get_text().startswith('Multimodal manifold'):
            text.set_transform(right.transAxes);text.set_position((.04,.96))
            text.set_verticalalignment('top')
        elif text.get_text().startswith('Textual manifold'):
            text.set_transform(right.transAxes);text.set_position((.04,.04))
            text.set_verticalalignment('bottom')
    return fig


def trends():
    d=trend.DATA
    fig,axes=plt.subplots(2,1,figsize=(11,6.7),sharex=True)
    fig.subplots_adjust(left=.085,right=.98,bottom=.10,top=.89,hspace=.45)
    months=trend.month_year_list(2022,11,d['pub_by_month'].shape[1]);x=np.arange(len(months))
    for row,ax in enumerate(axes):
        method=np.cumsum(d['pub_by_month'][row*2]);evaluation=np.cumsum(d['pub_by_month'][row*2+1])
        ax.fill_between(x,0,evaluation,color=T.rust,alpha=.28,linewidth=0)
        ax.fill_between(x,0,method,color=T.teal,alpha=.40,linewidth=0)
        ax.plot(x,evaluation,color=T.rust,lw=T.line,label='Evaluation / application')
        ax.plot(x,method,color=T.teal,lw=T.line,label='Methodological contribution')
        ax.set(ylim=(0,125 if row==0 else 25),xlim=(-1.4,32.7),
               ylabel='Cumulative publication count',yticks=[0,25,50,75,100] if row==0 else [0,5,10,15,20])
        ax.set_title('Text-only' if row==0 else 'Multimodal')
        style_axes(ax)
        # Preserve effective upstream events: no invented release dates or labels.
        events=d['dates_llm' if row==0 else 'dates_vlm']
        for date,label in events.items():
            if date not in months: continue
            i=months.index(date)
            dy=10.5 if row==0 else 2.4
            dy*=1+.8*label.count('*')
            ax.annotate(label.replace('*',''),xy=(i,evaluation[i]),
                        xytext=(i,evaluation[i]+dy),ha='center',va='bottom',fontsize=7.2,
                        arrowprops=dict(arrowstyle='-|>',lw=.55,color=T.muted,mutation_scale=5))
        ax.set_xticks(x[2::6],months[2::6])
        ax.tick_params(labelbottom=True)
    handles=[Patch(facecolor=T.rust,alpha=.45,label='Evaluation / application'),
             Patch(facecolor=T.teal,alpha=.55,label='Methodological contribution')]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.53,.995),ncols=2)
    return fig


EXAMPLES=[('bars_comparison_IEDB','Quantitative comparison',bars),
          ('brute_force','Composition breakdown',composition),
          ('comparison_radar','Radar comparison',radar_plot),
          ('comparison_posttraining','Post-training curves',lines),
          ('concept','Concept plots',concepts),
          ('trend_by_month','Publication trends',trends)]


def serialize(o):
    if isinstance(o,np.ndarray): return o.tolist()
    raise TypeError(type(o).__name__)


def main():
    apply_theme()
    out=ROOT/'figures';out.mkdir(exist_ok=True)
    # Remove stale exports of the example explicitly discarded by the user.
    for ext in ('png','pdf','svg'):
        (out/f'illustration.{ext}').unlink(missing_ok=True)
    data={'comparison_IEDB':raw.data_comparison_IEDB,
          'brute_force_math':brute.data_brute_force_math,
          'brute_force_logic':brute.data_brute_force_logic,
          'radar':radar.data_comparison,'posttraining':post.data_posttraining,'trends':trend.DATA}
    (ROOT/'data.json').write_text(json.dumps(data,default=serialize,indent=2)+'\n')
    metrics=[]
    with PdfPages(ROOT/'gallery.pdf',metadata={'Title':'Figures for Papers — B / light cream, six examples',
                   'Author':'Adapted from Chen Liu; cowplot-inspired styling'}) as gallery:
        for name,title,render in EXAMPLES:
            fig=render()
            # Fixed physical canvases: bbox_inches='tight' would change export sizes.
            fig.canvas.draw()
            for ext in ('png','pdf','svg'):
                fig.savefig(out/f'{name}.{ext}',dpi=300)
            gallery.savefig(fig,dpi=300)
            metrics.append({'name':name,'title':title,'width_in':fig.get_figwidth(),
                            'height_in':fig.get_figheight(),'axes':len(fig.axes)})
            print(f'Rendered {name}',flush=True)
            plt.close(fig)
    shutil.copyfile(ROOT/'gallery.pdf',ROOT/'gallery-beige.pdf')
    (ROOT/'render-info.json').write_text(json.dumps({'font':FONT,'font_preference':FONT_FAMILIES,
        'font_weight':'normal','math_font':'DejaVu Sans, italic variables','python':sys.version,
        'style':'B / light cream with thin black frames','selected_shade':'B',
        'theme':asdict(T),'palettes':PALETTES,
        'matplotlib':matplotlib.__version__,'numpy':np.__version__,'figures':metrics},indent=2)+'\n')


if __name__=='__main__':
    main()
