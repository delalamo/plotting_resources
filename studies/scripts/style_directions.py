"""Eight complete visual directions. Typography is fixed to the approved style."""
from copy import deepcopy
from palette_schemes import SCHEMES

P={s['id']:s for s in SCHEMES}

def direction(id,slug,name,palette,**changes):
    s=dict(id=id,slug=slug,name=name,palette=deepcopy(P[palette]),
           panel='#FAF6EE',canvas='#FFFFFF',ink='#282828',muted='#666666',
           grid_color='#E3DCCF',frame_color='#000000',line=1.15,error=.65,
           grid_width=.45,frame_width=.55,frame='box',grid='y',grid_style='-',
           ticks=0,marker=3.5,marker_fill='filled',dashes=True,bar_width=.77,
           bar_edge=0,cap=2,fill_alpha=.16,area_alpha=[.28,.40],radar_alpha=.035,
           hatch_color='#707070',hatch_width=.4,composition_alpha=.8,
           emphasis=False,caption='',best='',tradeoff='')
    s.update(changes)
    return s

DIRECTIONS=[
    direction('S1','porcelain','Porcelain precision','P1',
        panel='#FFFFFF',canvas='#FFFFFF',line=.85,error=.55,frame_width=.45,
        frame='left-bottom',grid='none',ticks=2.5,marker=3.0,marker_fill='open',
        dashes=False,bar_width=.62,cap=1.5,fill_alpha=.04,area_alpha=[.08,.13],radar_alpha=0,
        caption='White paper, open axes, delicate strokes and hollow markers.',
        best='Compact paper figures and dense technical comparisons.',
        tradeoff='Fine strokes are less prominent on projected slides.'),
    direction('S2','warm-editorial','Warm editorial','P2',
        panel='#F6F0E4',canvas='#F6F0E4',line=1.65,error=.8,frame_width=.65,
        grid_color='#DED5C5',grid_width=.4,marker=4.0,bar_width=.76,
        fill_alpha=.12,area_alpha=[.20,.30],
        caption='Continuous warm paper, aubergine accents and medium-weight curves.',
        best='A balanced research identity across papers and talks.',
        tradeoff='The tinted page is more visible when inserted into a white manuscript.'),
    direction('S3','mineral-grid','Mineral grid','P1',
        panel='#EBF1F5',canvas='#FFFFFF',frame_color='#566C7B',frame_width=.45,
        grid_color='#CBD6DF',grid_width=.45,grid='xy',grid_style=':',
        line=1.25,error=.65,marker=3.5,marker_fill='open',ticks=2,
        bar_width=.70,bar_edge=.35,fill_alpha=.08,area_alpha=[.14,.22],
        caption='Cool blue-gray panels, fine dotted grids and restrained frames.',
        best='Technical comparisons where reading values matters.',
        tradeoff='The denser grid adds structure but can compete with complex data.'),
    direction('S4','sage-field','Sage field','P2',
        panel='#EBF0E3',canvas='#F7F9F2',grid_color='#FFFFFF',grid_width=.8,
        frame='bottom',frame_color='#5B6755',frame_width=.65,line=1.55,error=.75,
        marker=4,marker_fill='filled',ticks=0,dashes=False,bar_width=.82,
        fill_alpha=.20,area_alpha=[.27,.39],radar_alpha=.055,
        caption='Pale sage fields, white reference lines and an open top edge.',
        best='Soft, distinctive plots and conceptual illustrations.',
        tradeoff='White gridlines are deliberately subtle; small print needs inspection.'),
    direction('S5','rose-atlas','Rose atlas','P4',
        panel='#F5E9E8',canvas='#FCF8F5',grid_color='#DECBCB',grid_width=.4,
        frame='left-bottom',frame_color='#715C61',frame_width=.6,
        line=1.4,error=.7,marker=4.5,marker_fill='open',ticks=2.5,
        dashes=False,bar_width=.72,fill_alpha=.10,area_alpha=[.18,.28],
        caption='Rose paper, petrol curves, hollow markers and open axes.',
        best='A calm editorial alternative with more color in the surface.',
        tradeoff='Rose and gold need redundant labels when hues become hard to distinguish.'),
    direction('S6','sandstone','Sandstone bold','P3',
        panel='#EADCC4',canvas='#EADCC4',ink='#29251F',muted='#655D51',
        frame_color='#393128',frame_width=1.05,grid='none',line=2.25,error=1.0,
        marker=5.1,marker_fill='filled',ticks=3.5,bar_width=.84,bar_edge=.4,cap=3,
        fill_alpha=.25,area_alpha=[.30,.46],radar_alpha=.065,
        hatch_color='#62594B',hatch_width=.5,
        caption='Deeper sand, strong borders, larger markers and substantial curves.',
        best='Presentations and figures that need presence at a distance.',
        tradeoff='Heavier strokes and fill can crowd dense radar or composition figures.'),
    direction('S7','graphite','Graphite + one accent','P2',
        panel='#F0F1EF',canvas='#FFFFFF',frame='none',grid_color='#FFFFFF',
        grid_width=.9,line=1.8,error=.8,marker=4.2,marker_fill='open',ticks=0,
        bar_width=.66,bar_edge=0,fill_alpha=.06,area_alpha=[.10,.24],
        emphasis=True,caption='Quiet grayscale comparisons, one plum accent and no enclosing frame.',
        best='Focusing attention on a target method without a nine-color legend.',
        tradeoff='Dense category plots require numbered positions; gray alone is insufficient.'),
    direction('S8','night-studio','Night studio','P5',
        panel='#202B35',canvas='#17212A',ink='#F3EEE5',muted='#B6C1C7',
        grid_color='#42505B',grid_width=.55,frame_color='#71808C',frame_width=.6,
        line=2.0,error=.9,marker=4.8,marker_fill='open',ticks=2,
        bar_width=.76,bar_edge=.35,cap=2.5,fill_alpha=.20,area_alpha=[.22,.32],
        radar_alpha=.07,hatch_color='#26333D',hatch_width=.45,
        caption='Ink-dark surfaces, pale luminous colors and confident curves.',
        best='Dark slides, digital reading and figure presentations.',
        tradeoff='A presentation variant; it needs a separate light export for conventional print.'),
]

# Palette changes are explicit; no brightness inversion is applied at export.
DIRECTIONS[3]['palette'].update(colors=['#5F3C61','#9B6135','#377264','#986C77','#6C7B42','#496D8A'],
    extra=['#737A6C','#966651','#4F5D49'],neutral='#767D6E')
DIRECTIONS[5]['palette'].update(colors=['#79343F','#365D7A','#6C6B35','#8B6038','#6F577D','#326B5E'],
    extra=['#6D675F','#965C55','#48555B'],neutral='#766A5B')
DIRECTIONS[6]['palette'].update(colors=['#74394F','#777A75','#454D53','#6B6369','#83817B','#62686D'],
    extra=['#858580','#5C6264','#747A75'],neutral='#858580')
DIRECTIONS[7]['palette'].update(colors=['#D5B7DE','#E5AA76','#80C7CF','#E49AAF','#BEC985','#AAADE5'],
    extra=['#B5BABD','#D4BD8D','#89BFA7'],neutral='#A8B5BD')

BACKGROUNDS=[('White','#FFFFFF'),('Porcelain','#F7F7F2'),('Approved cream B','#FAF6EE'),
             ('Warm paper','#F6F0E4'),('Sand','#EADCC4'),('Blue mist','#EBF1F5'),
             ('Sage','#EBF0E3'),('Rose','#F5E9E8'),('Lavender fog','#EEEBF4')]
LINE_WEIGHTS=[.65,.85,1.15,1.5,1.9,2.3]
