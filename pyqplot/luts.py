import numpy as np
import matplotlib.cm as cm
from collections import OrderedDict
from . import fig
from . import img
from . import markup

cmaps = OrderedDict()

cmaps['sequential.perceptuallyuniform'] = [
    'viridis', 'plasma', 'inferno', 'magma', 'qpjet' ]

cmaps['sequential.singlecolor'] = [
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn' ]

cmaps['sequential.other'] = [
    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper' ]

cmaps['diverging'] = [
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic' ]

cmaps['cyclic'] = [  'hsv' ]

cmaps['qualitative'] = [
    'Pastel1', 'Pastel2', 'Paired', 'Accent',
    'Dark2', 'Set1', 'Set2', 'Set3',
    'tab10', 'tab20', 'tab20b', 'tab20c' ]

cmaps['misc'] = [
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar' ]

def families():
    return [x for x in cmaps.keys()]

def family(name):
    return cmaps[name]

def cmap(name, N=None, reverse=False):
    if name=='qpjet':
        if N is None:
            rgb = img.jetlut()
        else:
            rgb = img.jetlut(N)
        if reverse:
            rgb = np.flipud(rgb)
        return rgb
    if reverse:
        name += '_r'
    name = name.replace('-', '_')
    cmap = cm.get_cmap(name, N)
    N = cmap.N
    rgb = np.zeros((N, 3))
    for n in range(N):
        rgb[n,:] = cmap(n)[:3]
    return rgb

def demo(fam=None):
    if fam is None:
        for f in families():
            demo(f)
    else:
        names = family(fam)
        Q = len(names)
        fig.figure(f'/tmp/luts-{fam}', 3, Q/4)
        for q in range(Q):
            rgb = cmap(names[q])
            N = rgb.shape[0]
            rgb = np.reshape(rgb, (1,N,3))
            img.image(rgb, rect=(0, -q, 1, .5))
            markup.at(0, -q+.25)
            markup.align('right', 'middle')
            txt = names[q]
            txt = txt.replace('_', '-')
            markup.text(txt, dx=-5)
        fig.shrink()
