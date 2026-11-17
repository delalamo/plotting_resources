"""Scaffold for custom Matplotlib content; keep the shared final layout/export."""
from _common import ps,output_path,export
import numpy as np

TITLE='A custom scientific illustration'
SUBTITLE='Ordinary Matplotlib drawing commands inherit the approved style'
SOURCE='Source: Illustrative equations and seeded synthetic points.'
NOTES='Notes: Math uses the approved Arial/STIX setup. Replace the drawing sections with your own content.'

def main():
    f,axes=ps.figure(1,2,panel_height=2.2,grid='xy');left,right=axes[0]
    # EDIT THIS PANEL: functions, custom annotations, or your own data.
    x=np.linspace(-3,3,150)
    for i,mu in enumerate([-.8,.8]):
        ps.line(left,x,np.exp(-.5*(x-mu)**2)/np.sqrt(2*np.pi),f'Distribution {i+1}',index=i,marker=False)
    left.set(xlabel='Value',ylabel='Density')
    left.text(.03,.92,r'$p(x\mid\mu)=\mathcal{N}(\mu,1)$',transform=left.transAxes,va='top')
    # EDIT THIS PANEL: ordinary Matplotlib scatter, shapes, arrows, etc.
    rng=np.random.default_rng(42);x=rng.normal(size=80);y=.65*x+rng.normal(scale=.45,size=80)
    right.scatter(x,y,s=ps.STYLE['marker']**2,facecolors=ps.STYLE['panel'],edgecolors=ps.BLUE,linewidths=.625)
    right.set(xlabel='Feature 1',ylabel='Feature 2')
    for i,(ax,title) in enumerate(zip(axes.flat,['Conditional\ndistribution','Illustrative\nobservations'])):
        ps.panel_title(ax,title,chr(65+i))
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES,legend_cols=2)

if __name__=='__main__':main()
