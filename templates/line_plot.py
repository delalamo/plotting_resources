"""Copy this file, replace DATA and captions, then run it."""
from _common import ps,output_path,export

X=[0,1,2,3,4,5]
DATA={'Method A':[22,42,51,56,59,61],
      'Method B':[22,29,34,37,39,40],
      'Method C':[22,24,27,29,30,31]}
TITLE='Performance across training steps'
SUBTITLE='Three methods on a common evaluation scale'
SOURCE='Source: Illustrative data; replace with your source.'
NOTES='Notes: Synthetic values demonstrate the template, not experimental results.'

def main():
    f,axes=ps.figure(grid='xy');ax=axes[0,0]
    for i,(name,y) in enumerate(DATA.items()):ps.line(ax,X,y,name,index=i)
    ax.set(xlabel='Training step',ylabel='Score',ylim=(0,70),xticks=X)
    export(f,output_path(__file__),title=TITLE,subtitle=SUBTITLE,source=SOURCE,notes=NOTES)

if __name__=='__main__':main()
