"""Build an isolated workspace for the exact historical reference renderers.

The legacy renderers expect inputs, sibling scripts and outputs under one root.
Copying them into build/ preserves their proven layout without writing generated
files into the tracked source directories. No saved export is required.
"""
from pathlib import Path
import shutil
import json

REPO=Path(__file__).resolve().parents[2]
WORK=REPO/'build/reference-gallery/figures4papers-minimal'


def copy_tree(source,target):
    if source.exists():
        shutil.copytree(source,target,dirs_exist_ok=True,
            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))


def prepare(minimal=False):
    global WORK
    WORK=REPO/('build/reference-gallery/minimal/figures4papers-minimal' if minimal else 'build/reference-gallery/figures4papers-minimal')
    WORK.mkdir(parents=True,exist_ok=True)
    copy_tree(REPO/'studies/records',WORK)
    copy_tree(REPO/'examples/data/inputs',WORK)
    copy_tree(REPO/'third_party/figures4papers',WORK/'upstream')
    copy_tree(REPO/'templates',WORK/'templates')
    copy_tree(REPO/'src/plotting_resources',WORK/'src/plotting_resources')
    for folder in [REPO/'studies/scripts',REPO/'examples/reference_gallery/scripts']:
        for path in folder.glob('*.py'):shutil.copyfile(path,WORK/path.name)
    for name in ['pyproject.toml','LICENSE']:shutil.copyfile(REPO/name,WORK/name)
    shutil.copyfile(REPO/'src/plotting_resources/selected_style.json',WORK/'selected-style.json')
    shutil.copyfile(REPO/'docs/style-guide.md',WORK/'README.md')
    (WORK/'paper_style.py').write_text('"""Compatibility import; the maintained implementation is the package."""\nfrom plotting_resources import *\n')
    settings=json.loads((WORK/'selected-style.json').read_text())
    settings['rendering']['minimal']=minimal
    if minimal:
        settings['style'].update(canvas='#FFFFFF',panel='#FFFFFF')
        settings['style']['theme']['background']='#FFFFFF'
    (WORK/'selected-style.json').write_text(json.dumps(settings,indent=2)+'\n')
    return WORK
