"""One cobalt series with gray comparisons; replace the arrays and captions."""
from _common import ps,output_path,export

X=[1,2,3,4,5,6]
FOCUS=[54,66,73,78,81,82]
REFERENCES={'Baseline A':[52,61,68,72,74,75],
            'Baseline B':[57,67,75,81,85,87],
            'Baseline C':[49,63,72,78,80,81]}
TITLE='A highlighted result in context'
SUBTITLE='Cobalt identifies the focal series; comparison curves are gray'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: The focal series need not be the highest-valued series.'

def main():
    f,axes=ps.figure(grid='xy');ax=axes[0,0]
    ps.emphasis_lines(ax,X,FOCUS,REFERENCES,focus_label='Selected method')
    ax.set(xlabel='Training epoch',ylabel='Score',xticks=X,ylim=(40,95))
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES,legend_cols=2)

if __name__=='__main__':main()
