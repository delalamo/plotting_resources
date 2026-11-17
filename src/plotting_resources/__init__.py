"""Reusable scientific plotting in the selected R1/S3 style."""
from .theme import ROOT,SETTINGS,STYLE,TYPE,LAYOUT,COLORS,BLUE,BRICK,GOLD,apply_theme,style_axes
from .charts import figure,panel_title,line,emphasis_lines,bars,grouped_bars,stacked_bars,area,radar
from .layout import finish,export

__version__ = "0.1.0"
