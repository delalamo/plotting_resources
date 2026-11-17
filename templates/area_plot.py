"""Cumulative area/line series; replace the observations, not the style."""
from _common import ps,output_path,export

X=[2020,2021,2022,2023,2024,2025]
DATA={'Evaluation / application':[2,6,14,29,48,65],
      'Methodological contribution':[1,2,5,8,12,17]}
TITLE='Cumulative activity over time'
SUBTITLE='Two categories retain the same scale'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: Synthetic cumulative totals. The areas overlap; they are not stacked.'

def main():
    f,axes=ps.figure();ax=axes[0,0]
    for i,((name,y),color) in enumerate(zip(DATA.items(),[ps.BRICK,ps.BLUE])):
        ps.area(ax,X,y,name,index=i,color=color)
    ax.set(xlabel='Year',ylabel='Cumulative count',ylim=(0,75),xticks=X)
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES,legend_cols=2)

if __name__=='__main__':main()
