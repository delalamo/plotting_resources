"""A shared-axis grid. Change ROWS/COLS and supply one dataset per panel."""
from _common import ps,output_path,export

ROWS,COLS=2,2
CATEGORIES=['Dataset\nA','Dataset\nB','Dataset\nC']
PANELS={'Condition 1':{'Method A':[.81,.84,.79],'Method B':[.72,.77,.74]},
        'Condition 2':{'Method A':[.75,.79,.76],'Method B':[.68,.70,.72]},
        'Condition 3':{'Method A':[.86,.89,.83],'Method B':[.79,.81,.77]},
        'Condition 4':{'Method A':[.80,.82,.78],'Method B':[.73,.76,.71]}}
TITLE='Comparisons across experimental conditions'
SUBTITLE='Equal panels and a shared legend retain the same category meanings'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: All panels use the same 0-1 scale. Values are synthetic.'

def main():
    if len(PANELS)!=ROWS*COLS:raise ValueError('Supply one dataset per panel.')
    f,axes=ps.figure(ROWS,COLS,sharex=True,sharey=True)
    for i,(ax,(name,data)) in enumerate(zip(axes.flat,PANELS.items())):
        ps.grouped_bars(ax,CATEGORIES,data);ax.set_ylim(0,1)
        ps.panel_title(ax,name,chr(65+i))
        if i%COLS==0:ax.set_ylabel('Score')
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES,legend_cols=2)

if __name__=='__main__':main()
