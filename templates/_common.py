"""Shared CLI and output handling for the editable starter scripts."""
from pathlib import Path
import argparse
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'paper-plotting-mpl'))
import matplotlib
matplotlib.use('Agg')
import plotting_resources as ps

PARSER=argparse.ArgumentParser(description='Render the selected plotting style.')
PARSER.add_argument('--minimal',action='store_true',help='White backgrounds; omit figure title, subtitle, source and notes.')
ARGS=PARSER.parse_args()
REPO=Path(__file__).resolve().parents[1]

def output_path(script):
    folder=Path(os.environ.get('PAPER_OUTPUT_DIR',str(REPO/'build/templates')))
    if ARGS.minimal:folder=folder/'minimal'
    return folder/Path(script).stem

def export(f,path,**kwargs):
    return ps.export(f,path,minimal=ARGS.minimal,**kwargs)
