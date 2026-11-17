"""Ranked bars with optional uncertainty; highlight uses a zero-based index."""
from _common import ps,output_path,export

LABELS=['Selected method','Comparison with a longer name','Comparison B','Comparison C','Comparison D']
VALUES=[.83,.79,.76,.69,.61]
ERRORS=[.014,.020,.018,.025,.022]  # Use None to omit uncertainty.
HIGHLIGHT=0
TITLE='Performance across methods'
SUBTITLE='Direct labels show the central estimates'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: Synthetic values. Error bars indicate the supplied uncertainty.'

def main():
    f,axes=ps.figure(grid='');ax=axes[0,0]
    ps.bars(ax,LABELS,VALUES,errors=ERRORS,horizontal=True,highlight=HIGHLIGHT,value_format='.2f')
    ax.set(xlabel='Score',xticks=[])
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES,legend=False)

if __name__=='__main__':main()
