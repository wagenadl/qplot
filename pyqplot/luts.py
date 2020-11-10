import numpy as np
from collections import OrderedDict

_cmaps = OrderedDict()

_cmaps['native'] = [ 'qpjet', 'qphot', 'qpcold', 'qpcoldhot' ]

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

def _ankle(x, gamma, x0):
    '''
    Let's say that 0 ≤ x ≤ 1.
    Take a linear function f(x) = A*x + 1-A that passes through (1,1).
    Take a power function g(x) = B*x^gamma that passes through (0,0).
    We want these to join at x = x0, so we must have:
      f(x0) = g(x0)
      f'(x0) = g'(x0)
    Thus:
      A*x0 + 1 - A = B x0^gamma
      A               = B gamma x0^(gamma-1)
    Thus:
     1 = (x0^gamma + gamma x0^(gamma-1) - gamma x0^gamma) B'''
    B = 1 / (x0**gamma + gamma * x0**(gamma-1) - gamma * x0**gamma)
    A = B * gamma * x0**(gamma-1)
    y = A*x + 1-A
    y[x<x0] = B*x[x<x0]**gamma
    return y

def _rankle(x, gamma, x0):
    return 1 - _ankle(1-x, gamma, x0)

def _cosinebump(x, mu, sigma):
    #return np.exp(-.5*(x-mu)**2/sigma**2)
    t = (x - mu)/sigma*np.pi/2
    y = np.zeros(x.shape)
    use = np.logical_and(t>-np.pi, t<np.pi)
    y[use] = .5 + .5*np.cos(t[use])
    return y

def _hot(n=300):
    xx = np.arange(0,1,1/n)
    yy = 0*xx
    zz = 1+yy
    red = _rankle(xx,5,.6)
    grn = _rankle(_ankle(xx,4,.4),3,.7)
    blu = _rankle(_ankle(xx,8,.7),1,.2)
    return np.stack((red,grn,blu), 1)

def _cold(n=300):
    xx = np.arange(0,1,1/n)
    yy = 0*xx
    zz = 1+yy
    blu = _rankle(_ankle(xx,.6,.2),4,.5)
    grn = _rankle(_ankle(xx,2,.2),1.8,.7)
    red = _rankle(_ankle(xx,3,.6),1.2,.5)
    blu -= .35*_cosinebump(xx, .66,.17)
    blu = _rankle(blu, .7, .1)
    return np.stack((red,grn,blu), 1)

def _native(name, N, reverse):
    from . import img
    if N is None:
        N = 256
    if name=='qpjet':
        rgb = img.jetlut(N)
    elif name=='qphot':
        rgb = _hot(N)
    elif name=='qpcold':
        rgb = _cold(N)
    elif name=='qpcoldhot':
        rgb = np.vstack((np.flipud(_cold(N//2)), _hot(N//2)))
    else:
        raise ValueError('Unknown colormap')
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
    if name in _cmaps['native']:
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
