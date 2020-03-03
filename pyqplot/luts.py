import numpy as np
from collections import OrderedDict

_cmaps = OrderedDict()

_cmaps['native'] = [ 'qpjet' ]

_cmaps['sequential.perceptuallyuniform'] = [
    'viridis', 'plasma', 'inferno', 'magma' ]

_cmaps['sequential.singlecolor'] = [
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn' ]

_cmaps['sequential.other'] = [
    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper' ]

_cmaps['diverging'] = [
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic' ]

_cmaps['cyclic'] = [  'hsv' ]

_cmaps['qualitative'] = [
    'Pastel1', 'Pastel2', 'Paired', 'Accent',
    'Dark2', 'Set1', 'Set2', 'Set3',
    'tab10', 'tab20', 'tab20b', 'tab20c' ]

_cmaps['misc'] = [
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar' ]

_cmaps['plotly.sequential'] = None
_cmaps['plotly.diverging'] = None
_cmaps['plotly.cyclical'] = None
_cmaps['carto'] = None
_cmaps['cmocean'] = None
_cmaps['colorbrewer'] = None

def _load_plotly_cmaps():
    for k in _cmaps:
        if _cmaps[k] is None:
            m = k.replace('plotly.', '')
            import plotly.colors as pc
            mod = pc.__dict__[m]
            names = [x for x in mod.__dict__ if not '_' in x and x!='swatches']
            _cmaps[k] = names

def families():
    '''FAMILIES - Return a list of colormap families.
    x = FAMILIES() returns a list of family names of colormaps. The family
    names can be passed to FAMILY to obtain the names of colormaps in that
    family.'''
    return [x for x in _cmaps.keys()]

def family(name):
    '''FAMILY - Return a list of colormaps in a family.
    x = FAMILY(f) returns a list of all the colormaps in the given family.'''
    if _cmaps[name] is None:
        _load_plotly_cmaps()
    return _cmaps[name]

def _native(name, N, reverse):
    from . import img
    if N is None:
        rgb = img.jetlut()
    else:
        rgb = img.jetlut(N)
    if reverse:
        rgb = np.flipud(rgb)
    return rgb

def _get_mpl_cmap(name, N, reverse):
    if reverse:
        name += '_r'
    name = name.replace('-', '_')
    import matplotlib.cm as cm
    try:
        cmap = cm.get_cmap(name, N)
    except ValueError:
        return None
    N = cmap.N
    rgb = np.zeros((N, 3))
    for n in range(N):
        rgb[n,:] = cmap(n)[:3]
    return rgb

def _get_plotly_cmap(name, N, reverse):
    import plotly.colors as pc
    _load_plotly_cmaps()
    if reverse:
        name += '_r'
    name = name.replace('-', '_')
    fam = None
    for f in _cmaps:
        lst = _cmaps[f]
        if name in lst:
            fam = f.replace('plotly.', '')
    cmap = pc.__dict__[fam].__dict__[name]
    cmap = pc.validate_colors(cmap)
    K = len(cmap)
    rgb = np.zeros((K, 3))
    for k in range(K):
        r,g,b = cmap[k]
        rgb[k,:] = [r,g,b]
    if N is None:
        return rgb
    xx = np.arange(N) * (K-1) / (N-1)
    res = np.zeros((N, 3))
    for n in range(N):
        k0 = int(np.floor(xx[n]))
        k1 = int(np.ceil(xx[n]))
        dx = xx[n] - k0
        res[n,:] = rgb[k0,:]*(1-dx) + rgb[k1,:]*dx
    return res
        
def get(name, N=None, reverse=False):
    '''GET - Retrieve a colormap.
    cm = GET(name) retrieves the named colormap.
    Optional argument N specifies the number of colors to return. Default is
    dependent on the particular map.
    Optional argument REVERSE specifies that the order of the colors should
    be reversed.
    See also SET.'''
    if name=='qpjet':
        return _native(name, N, reverse)
    cmap = _get_mpl_cmap(name, N, reverse)
    if cmap is None:
        cmap = _get_plotly_cmap(name, N, reverse)
    if cmap is None:
        raise ValueError(f'Unknown color map {name}')
    return cmap

def set(name, N=None, reverse=False):
    '''SET - Retrieve and apply a colormap.
    SET(name, N, reverse) is a shortcut for the corresponding call to GET,
    followed by a call to LUT.'''
    
    from . import img
    cm = get(name, N, reverse)
    img.lut(cm)
    
def demo(fam=None, N=None):
    '''DEMO - Produce tableau of colormaps.
    DEMO(family) produces a tableau of all the colormaps in the given family.
    DEMO() produces separate tableaus for all families.
    Optional argument N specifies the number of colors to request for each
    colormap. The default is to render each map with its own default.'''
    
    from . import fig
    from . import img
    from . import markup
    from . import style
    
    if fam is None:
        for f in families():
            demo(f)
    else:
        names = family(fam)
        Q = len(names)
        C = int(np.ceil(Q/10))
        R = int(np.ceil(Q/C))
        fig.figure(f'/tmp/luts-{fam}', 3*C, R/4)
        style.pen('none')
        for c in range(int(C)):
            fig.relpanel(chr(65+c), (c/C, 0, 1/C, 1))
        for q in range(Q):
            c = q//R
            r = q%R
            fig.panel(chr(65+int(c)))
            rgb = get(names[q], N)
            N = rgb.shape[0]
            rgb = np.reshape(rgb, (1,N,3))
            img.image(rgb, rect=(0, -r, 1, .5))
            markup.at(0, -r+.25)
            markup.align('right', 'middle')
            txt = names[q]
            txt = txt.replace('_', '-')
            style.pen('k')
            markup.text(txt, dx=-5)
            fig.shrink()
