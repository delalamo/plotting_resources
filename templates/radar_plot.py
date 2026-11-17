"""Radar with a common scale; heterogeneous benchmark scales need explicit normalization."""
from _common import ps,output_path,export

CATEGORIES=['Accuracy','Recall','Precision','Robustness','Coverage']
DATA={'Method A':[83,75,88,72,80],'Method B':[76,81,73,68,79],'Method C':[70,68,77,83,71]}
TITLE='Profiles across evaluation dimensions'
SUBTITLE='Every dimension uses the same 0-100 scale'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: Synthetic comparable scores; no per-axis normalization is applied.'

def main():
    f,axes=ps.figure(projection='polar',grid='xy',panel_height=2.6);ax=axes[0,0]
    ps.radar(ax,CATEGORIES,DATA)
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES)

if __name__=='__main__':main()
