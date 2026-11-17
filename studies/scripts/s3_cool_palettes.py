"""Original cool-color proposals on the unchanged S3 Mineral grid surface.

The references inform hue relationships, not copied brand palettes. These are
sRGB screen/print-figure colors, not measured paint-color conversions.
"""
from copy import deepcopy
from style_directions import DIRECTIONS

S3 = deepcopy(next(s for s in DIRECTIONS if s['id'] == 'S3'))

SOURCES = [
    dict(id='N', title='Nord: Colors and Palettes',
         url='https://www.nordtheme.com/docs/colors-and-palettes/',
         observation='Frost pairs blue-green, cyan and muted blue with pale blue-gray Snow Storm surfaces.',
         tones='Frost: #8FBCBB, #88C0D0, #81A1C1, #5E81AC.',
         adaptation='C1 uses the related-hue idea with substantially darker marks for a light plotting panel.'),
    dict(id='I', title='IBM Carbon: Data visualization color palettes',
         url='https://www.carbondesignsystem.com/building-blocks/data-visualization/color-palettes',
         observation='Carbon separates categories with purple, cyan and deep teal, alongside other families; sequence matters.',
         tones='Examples: purple #6929C4, cyan #1192E8, teal #005D5D.',
         adaptation='C5 uses this wider cool-hue spacing, with original, quieter colors. It is not the Carbon palette.'),
    dict(id='J', title='Jotun: Calm blue, fresh and airy bedroom colours',
         url='https://www.jotun.com/in-en/decorative/inspiration/indoor/rooms/bedroom/calm-bluefresh-and-airy',
         observation='The interior guidance groups blue, lavender, mint and green with white and light gray.',
         tones='Hue families, not paint-to-hex conversions: blue / lavender / mint / green.',
         adaptation='C2, C3 and C4 explore these relationships in darker ink-like colors appropriate to small marks.'),
    dict(id='U', title='USWDS: System color tokens',
         url='https://designsystem.digital.gov/design-tokens/color/system-tokens/',
         observation='The blue-cool family spans a pale surface through medium and deep blue-green shades.',
         tones='Examples: #E7F2F5 at grade 5; #3A7D95 at 50; #224A58 at 70.',
         adaptation='Across the proposals, use depth as well as hue to distinguish marks on a pale blue surface.'),
]

def candidate(id, slug, name, colors, names, extra, neutral, caption, best, tradeoff, sources):
    s = deepcopy(S3)
    s.update(id=id, slug=slug, name=name, caption=caption, best=best, tradeoff=tradeoff)
    s['palette'] = dict(id=id, name=name, colors=colors, names=names, extra=extra,
                        neutral=neutral, sources=sources)
    return s

COOL = [
    candidate('C1', 'fjord', 'Fjord',
        ['#274E70','#216F7A','#71839B','#496B8C','#487F75','#626988'],
        ['Deep fjord','Glacier teal','Dusty steel','Harbor blue','Sea pine','Storm iris'],
        ['#52616E','#8A8297','#284B53'], '#74828D',
        'Navy, glacier teal and dusty steel; the quietest option.',
        'A restrained blue-gray identity close to the panel color.',
        'The related blues rely more on marker shapes and labels.', ['N','U']),
    candidate('C2', 'glacial-iris', 'Glacial iris',
        ['#414F86','#237F78','#947AA5','#527EAA','#526A94','#497C92'],
        ['Indigo ink','Deep sea glass','Dusty iris','Clear slate','Dusk blue','Blue spruce'],
        ['#677887','#725B87','#2E5461'], '#74808D',
        'Indigo, sea glass and dusty iris; calm with a distinct identity.',
        'My preferred balance of cohesion and category separation.',
        'Expanded palettes still need stable labels when many series overlap.', ['J','N','U']),
    candidate('C3', 'sea-glass', 'Sea glass',
        ['#205B63','#4B8176','#668DB4','#3A728D','#6C8992','#405C7B'],
        ['Deep lagoon','Mineral jade','Glazed blue','Ocean blue','Weathered aqua','Marine slate'],
        ['#5D6D72','#748676','#304C56'], '#72858A',
        'Lagoon, muted jade and glazed blue; the greenest cool option.',
        'A soft marine identity with little violet.',
        'Adjacent teal/green hues are less distinct in dense categorical plots.', ['J','N','U']),
    candidate('C4', 'blue-hour', 'Blue hour',
        ['#343E70','#5974AF','#9581A3','#46658D','#597B98','#5A5B8F'],
        ['Night indigo','Periwinkle','Ash violet','Deep denim','Lake slate','Smoky iris'],
        ['#69768E','#89879B','#3E5265'], '#798293',
        'Indigo, periwinkle and ash violet; a more tonal blue-purple look.',
        'A distinctive violet-leaning direction for a small number of series.',
        'Dense blue-purple categories need careful labels and ordering.', ['J','U']),
    candidate('C5', 'arctic-signal', 'Arctic signal',
        ['#184D91','#188C9A','#8055A7','#3D82AE','#426F70','#5C60A3'],
        ['Arctic blue','Deep cyan','Mineral violet','Glacier blue','Ocean green','Cold iris'],
        ['#5F748B','#8A719D','#254F66'], '#6E8092',
        'Clear blue, deep cyan and mineral violet; the most vivid option.',
        'More visible color separation and a stronger digital presence.',
        'The saturated accents draw more attention than the quieter options.', ['I','U']),
]

COLOR_FIELDS = {'id','slug','name','palette','caption','best','tradeoff'}
FIXED = {k:v for k,v in S3.items() if k not in COLOR_FIELDS}
for s in COOL:
    assert {k:v for k,v in s.items() if k not in COLOR_FIELDS} == FIXED
