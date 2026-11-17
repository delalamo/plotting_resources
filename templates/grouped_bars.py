"""Grouped bars: one value per category in each series."""
from _common import ps,output_path,export

CATEGORIES=['Dataset A','Dataset B','Dataset C']
DATA={'Method A':[.78,.83,.80],'Method B':[.72,.77,.76],'Method C':[.67,.70,.71]}
ERRORS={'Method A':[.02,.01,.02],'Method B':[.03,.02,.02],'Method C':[.02,.03,.02]}
TITLE='Comparing methods across datasets'
SUBTITLE='Shared colors and a zero baseline support comparison'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: Replace the uncertainty arrays with the quantities appropriate to your study.'

def main():
    f,axes=ps.figure();ax=axes[0,0]
    ps.grouped_bars(ax,CATEGORIES,DATA,errors=ERRORS)
    ax.set(ylabel='Score',ylim=(0,1))
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES)

if __name__=='__main__':main()
