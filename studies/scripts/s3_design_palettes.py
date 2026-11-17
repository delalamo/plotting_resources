"""Mixed warm/cool palettes grounded in actual pale-blue design precedents.

The S3 panel is #EBF1F5 in every proposal. None of the references is claimed to
use that exact hex. Proposed sRGB marks are authored adaptations, not sampled
paint colors or replicas of a complete brand palette.
"""
from copy import deepcopy
from style_directions import DIRECTIONS

S3 = deepcopy(next(s for s in DIRECTIONS if s['id']=='S3'))
COLOR_FIELDS = {'id','slug','name','palette','caption','best','tradeoff'}
FIXED = {k:v for k,v in S3.items() if k not in COLOR_FIELDS}

SOURCES = [
    dict(id='G', title='Gisbert Poppler: Garden Home, reported by Yatzer',
         url='https://www.yatzer.com/garden-house-gisbert-poppler',
         kind='Design publication with designer interview and project photographs',
         finding='The project combines light blue, crimson red and mustard yellow; green and orange appear elsewhere.',
         application='R1 keeps blue/red/gold as its core and uses the other hue families in the expanded set.'),
    dict(id='P', title='Pinterest Palette 2026',
         url='https://business.pinterest.com/pinterest-palette/',
         kind='Primary source: published digital palette',
         finding='Cool Blue #D7EFFF appears with Plum Noir #351E28, Persimmon #FF5C34, Wasabi #E9F056 and Jade #AEB8A0.',
         application='R2 borrows the plum/orange/yellow-green relationship. Orange and citron are darkened for thin marks; the full source palette is not copied.'),
    dict(id='T', title='Temp Project: Gunia showroom, architect-supplied description',
         url='https://www.archdaily.com/1039360/gunia-project-showroom-temp-project',
         kind='Primary source: description provided by the architects',
         finding='The architects describe greens, blues, pale pinks and soft beige alongside retained wooden panels and mahogany cabinets.',
         application='R3 uses cocoa, rose and jade on S3, adapting the material/color relationships into darker plotting inks.'),
    dict(id='H', title='Gunia Project: Hospitality Design project report',
         url='https://hospitalitydesign.com/news/gunia-project-store-kyiv-ukraine/183578/',
         kind='Design publication: project report',
         finding='The report specifically identifies chocolate brown with pale blue, and also describes sky blue, green and flower pink.',
         application='This supports the pale-blue/brown relationship in R3; rose and jade keep its categories varied.'),
    dict(id='B', title='Benjamin Moore: complementary color combinations',
         url='https://www.benjaminmoore.com/en-us/color-overview/color-insights/complementary-colors-guide',
         kind='Primary source: manufacturer design guidance',
         finding='A blue room illustration opens into orange; another example pairs turquoise tiles with orange-red cabinetry.',
         application='R4 shifts that relationship to petrol and coral on a pale blue-gray panel.'),
    dict(id='L', title='Little Greene: blue walls and yellow woodwork',
         url='https://www.littlegreene.com/advice-hub/8-interior-wall-and-skirting-board-colour-combinations',
         kind='Primary source: manufacturer design guidance',
         finding='The blue/yellow example uses Grey Stone and Woad with Sunlight; another combines blue-purple with yellow highlights.',
         application='Saffron is the authored third plotting color in R4, drawing on this blue/yellow pairing.'),
    dict(id='A', title='Benjamin Moore: historical living-room color schemes',
         url='https://www.benjaminmoore.com/en-us/benjamin-moore-co-archives/living-room-color-schemes',
         kind='Primary source: manufacturer archive',
         finding='The circa-1930 room has a light blue ceiling, gray-green rug, red upholstery and bright blue bookcases.',
         application='R5 interprets those accents as wine, olive and denim. These are original contemporary sRGB choices.'),
]

def proposal(id,slug,name,colors,names,extra,neutral,caption,best,tradeoff,refs,precedent):
    s=deepcopy(S3)
    s.update(id=id,slug=slug,name=name,caption=caption,best=best,tradeoff=tradeoff)
    s['palette']=dict(id=id,name=name,colors=colors,names=names,extra=extra,
                      neutral=neutral,sources=refs,precedent=precedent)
    return s

PROPOSALS=[
    proposal('R1','cobalt-brick-gold','Cobalt / brick / gold',
        ['#285F96','#B9413A','#A68517','#2B7C70','#9E638C','#685B80'],
        ['Cobalt','Brick red','Old gold','Malachite','Heather rose','Violet slate'],
        ['#717B7F','#A96E45','#5B713C'],'#7A7770',
        'Clear blue with warm brick and mustard-gold.',
        'A confident blue/red/yellow identity with a recognizable warm-cool balance.',
        'Blue and red can have similar grayscale value; retain the marker shapes.',['G'],
        'Garden Home: light blue + crimson + mustard'),
    proposal('R2','plum-orange-citron','Plum / orange / citron',
        ['#6E354F','#BC5430','#8B9026','#417899','#43775B','#B2638A'],
        ['Plum wine','Persimmon ink','Citron','Mineral blue','Garden green','Dahlia'],
        ['#687B85','#806147','#8671AA'],'#7B716E',
        'Deep plum, orange-red and yellow-green; the most adventurous mix.',
        'The largest shift from S3 without changing its quiet background.',
        'Orange and citron move closer under red-green color-vision simulation.',['P'],
        'Pinterest: icy blue + plum + persimmon + yellow-green'),
    proposal('R3','cocoa-rose-jade','Cocoa / rose / jade',
        ['#67463B','#B96588','#338269','#4E7C9D','#A68234','#7B6C9D'],
        ['Cocoa','Rose velvet','Jade','Glazed blue','Brass','Smoked lilac'],
        ['#768072','#9E5B4D','#44636C'],'#80766F',
        'Warm cocoa, rose and green against the blue-gray surface.',
        'A material-inspired direction that moves the signature color away from blue.',
        'Rose and jade need their distinct markers in grayscale.',['T','H'],
        'Gunia showroom: pale blue + dark wood + pink + green'),
    proposal('R4','petrol-coral-saffron','Petrol / coral / saffron',
        ['#155D68','#C85745','#AE811C','#5469A1','#9B5C85','#6A8142'],
        ['Petrol','Coral','Saffron','Ultramarine','Orchid','Leaf green'],
        ['#74818A','#7B5643','#8874A1'],'#7D7970',
        'Deep petrol balances two brighter, warmer accents.',
        'A lively mix for curves, bars and area fills, with a dark anchor.',
        'The two warm colors are less distinct without hue; keep labels and dashes.',['B','L'],
        'Benjamin Moore + Little Greene: blue/orange and blue/yellow'),
    proposal('R5','wine-olive-denim','Wine / olive / denim',
        ['#863B50','#6F813B','#5185A6','#B97638','#2D706B','#9F6C88'],
        ['Wine','Olive leaf','Denim','Copper','Deep jade','Rosewood'],
        ['#776B61','#7F709D','#A7594A'],'#7D786D',
        'Wine red, olive and denim; an earthy but more varied direction.',
        'Closest to the original balance, with a red signature instead of blue.',
        'Wine and olive need redundant encoding for red-green color-vision differences.',['A'],
        'Benjamin Moore archive: pale blue + red + gray-green + blue'),
]

for s in PROPOSALS:
    assert {k:v for k,v in s.items() if k not in COLOR_FIELDS}==FIXED
