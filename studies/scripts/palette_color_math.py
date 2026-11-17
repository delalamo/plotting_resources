"""Small, dependency-free color tools for the palette study (NumPy only).

Oklab equations: https://bottosson.github.io/posts/oklab/
Machado et al. (2009), DOI 10.1109/TVCG.2009.113, severity-100 matrices:
https://raw.githubusercontent.com/njsmith/colorspacious/master/colorspacious/cvd.py
These are numerical screening tools, not accessibility certification.
"""
import numpy as np
from matplotlib.colors import to_rgb, to_hex

M1 = np.array([[.4122214708,.5363325363,.0514459929],
               [.2119034982,.6806995451,.1073969566],
               [.0883024619,.2817188376,.6299787005]])
M2 = np.array([[.2104542553,.7936177850,-.0040720468],
               [1.9779984951,-2.4285922050,.4505937099],
               [.0259040371,.7827717662,-.8086757660]])
CVD = {
    "protan": np.array([[.152286,1.052583,-.204868],[.114503,.786281,.099216],[-.003882,-.048116,1.051998]]),
    "deutan": np.array([[.367322,.860646,-.227968],[.280085,.672501,.047413],[-.011820,.042940,.968881]]),
    "tritan": np.array([[1.255528,-.076749,-.178779],[-.078411,.930809,.147602],[.004733,.691367,.303900]]),
}

def linear(rgb):
    x=np.asarray(rgb, dtype=float)
    return np.where(x<=.04045, x/12.92, ((x+.055)/1.055)**2.4)

def encoded(rgb):
    x=np.clip(np.asarray(rgb, dtype=float),0,1)
    return np.where(x<=.0031308,12.92*x,1.055*np.power(x,1/2.4)-.055)

def luminance(rgb):
    return linear(rgb) @ np.array([.2126,.7152,.0722])

def contrast(a,b):
    x,y=float(luminance(to_rgb(a))),float(luminance(to_rgb(b)))
    return (max(x,y)+.05)/(min(x,y)+.05)

def oklab(rgb):
    return np.cbrt(linear(rgb) @ M1.T) @ M2.T

def from_oklab(lab):
    return encoded((np.asarray(lab) @ np.linalg.inv(M2).T)**3 @ np.linalg.inv(M1).T)

def gamut_map(lab):
    """Reduce chroma, preserving L and hue, until the color is inside sRGB."""
    lab=np.array(lab, dtype=float)
    for _ in range(150):
        lin=(lab @ np.linalg.inv(M2).T)**3 @ np.linalg.inv(M1).T
        if np.all(lin>=-1e-8) and np.all(lin<=1+1e-8):
            return encoded(lin)
        lab[1:]*=.97
    raise ValueError("No in-gamut color found")

def ramp(scheme, diverging=False, n=257):
    primary=oklab(to_rgb(scheme['colors'][0]));primary[0]=.42
    light=oklab(to_rgb('#FAF6EE'));light[0]=.965
    if not diverging:
        points=np.linspace(light,primary,n)
    else:
        other=oklab(to_rgb(scheme['colors'][1]));other[0]=.42
        points=np.vstack([np.linspace(other,light,n//2+1),np.linspace(light,primary,n//2+1)[1:]])
    return np.array([gamut_map(v) for v in points])

def simulate(rgb, mode):
    rgb=np.asarray(rgb)
    if mode=='normal': return rgb
    if mode=='gray': return encoded(np.repeat(luminance(rgb)[...,None],3,axis=-1))
    return encoded(linear(rgb) @ CVD[mode].T)

def audit(scheme, background):
    colors=scheme['colors']+scheme['extra']
    checks={'opaque_contrast_on_cream':{h:round(contrast(h,background),3) for h in colors},
            'three_color_core':[scheme['colors'][i] for i in (0,1,2)],
            'closest_core_pair':{}, 'expanded_close_pairs':{}}
    for mode in ('normal','protan','deutan','tritan','gray'):
        lab=oklab(simulate(np.array([to_rgb(h) for h in colors]),mode))
        distances=[(float(np.linalg.norm(lab[a]-lab[b])),a,b) for a in range(9) for b in range(a+1,9)]
        core=min(p for p in distances if p[1]<3 and p[2]<3)
        checks['closest_core_pair'][mode]={'oklab_distance':round(core[0],4),
            'colors':[colors[core[1]],colors[core[2]]]}
        # 0.06 is only a conservative editorial review flag, not a perceptual standard.
        checks['expanded_close_pairs'][mode]=[{'colors':[colors[a],colors[b]],'distance':round(d,4)}
            for d,a,b in sorted(distances) if d<.06]
    seq,div=ramp(scheme),ramp(scheme,True)
    checks['sequential_luminance_decreases']=bool(np.all(np.diff(luminance(seq))<0))
    checks['diverging_luminance_increases_to_center']=bool(np.all(np.diff(luminance(div[:129]))>0))
    checks['diverging_luminance_decreases_from_center']=bool(np.all(np.diff(luminance(div[128:]))<0))
    checks['sequential_9_stops']=[to_hex(v).upper() for v in seq[::32]]
    checks['diverging_9_stops']=[to_hex(v).upper() for v in div[::32]]
    return checks
