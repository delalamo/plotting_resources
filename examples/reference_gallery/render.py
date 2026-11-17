"""Rebuild the four multi-panel and all 16 reference/article examples."""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from _workspace import prepare


def main():
    os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'plotting-resources-mpl'))
    os.environ.setdefault('MPLBACKEND','Agg')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minimal',action='store_true',help='White backgrounds and no figure captions, sources or notes.')
    args=parser.parse_args()
    work=prepare(minimal=args.minimal)
    for name in ['render_multipanel_examples.py','render_reference_collection.py',
                 'render_article_context.py','build_gallery.py']:
        subprocess.run([sys.executable,str(work/name)],cwd=work,check=True)
    print('Gallery:',work/'gallery.html')
    print('Article proof:',work/'article-context/all-16-figures-in-article-context.pdf')


if __name__=='__main__':main()
