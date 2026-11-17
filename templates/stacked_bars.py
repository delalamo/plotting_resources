"""Stack supplied values; the helper never silently renormalizes them."""
from _common import ps,output_path,export

CATEGORIES=['Condition A','Condition B','Condition C','Condition D']
DATA={'Outcome 1':[.28,.36,.42,.39],'Outcome 2':[.32,.30,.28,.27],
      'Outcome 3':[.25,.22,.20,.22],'Outcome 4':[.15,.12,.10,.12]}
TITLE='Composition across conditions'
SUBTITLE='Four outcomes on the same probability scale'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: Values are used as supplied. These illustrative columns sum to one.'

def main():
    f,axes=ps.figure();ax=axes[0,0]
    ps.stacked_bars(ax,CATEGORIES,DATA)
    ax.set(ylabel='Probability',ylim=(0,1),yticks=[0,.25,.5,.75,1])
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES,legend_cols=2)

if __name__=='__main__':main()
