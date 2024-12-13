'''LUTS - Look-up tables for image rendering

Functions: FAMILIES, FAMILY, GET, SET,  DEMO'''

import numpy as np
from collections import OrderedDict
from . import data

haveplotly = False
try:
    import plotly.colors
    haveplotly = True
except ModuleNotFoundError:
    pass

havecolorcet = False
try:
    import colorcet
    havecolorcet = True
except ModuleNotFoundError:
    pass


_cmaps = OrderedDict()

_cmaps['native'] = [ 'qpjet', 'qphsv', 'qphot', 'qpcold', 'qpcoldhot' ]

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
    'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar' ]

_cmaps['plotly.sequential'] = None
_cmaps['plotly.diverging'] = None
_cmaps['plotly.cyclical'] = None
_cmaps['carto'] = None
_cmaps['cmocean'] = None
_cmaps['colorbrewer'] = None

_cmaps['cet.linear'] = None
_cmaps['cet.diverging'] = None
_cmaps['cet.cyclic'] = None
_cmaps['cet.glassbey'] = None
_cmaps['cet.isoluminant'] = None
_cmaps['cet.rainbow'] = None

def _load_plotly_cmaps():
    for k in _cmaps:
        if _cmaps[k] is None:
            if haveplotly:
                m = k.replace('plotly.', '')
                if m not in plotly.colors.__dict__:
                    return
                mod = plotly.colors.__dict__[m]
                names = [x for x in mod.__dict__
                         if not '_' in x and x!='swatches']
                _cmaps[k] = names
            else:
                _cmaps[k] = []

                
def _load_colorcet_cmaps():
    for k in _cmaps:
        if k.startswith('cet.') and _cmaps[k] is None:
            if havecolorcet:
                pfx = k.replace('cet.', '') + '_'
                names = []
                for name in colorcet.all_original_names():
                    if name.startswith(pfx):
                        alii = colorcet.get_aliases(name).split(',')
                        if len(alii)>1:
                            names.append(alii[0])
                _cmaps[k] = names
            else:
                _cmaps[k] = []

def families():
    '''LUTS.FAMILIES - Return a list of colormap families.
    x = LUTS.FAMILIES() returns a list of family names of
    colormaps. The family names can be passed to LUTS.FAMILY to obtain the
    names of colormaps in that family.
    See also LUTS.DEMO.
    '''
    return [x for x in _cmaps.keys()]

def family(name):
    '''LUTS.FAMILY - Return a list of colormaps in a family.
    x = LUTS.FAMILY(f) returns a list of all the colormaps in the
    given family.
    Several families depend on the availability of PLOTLY. If PLOTLY is
    not installed, those families will comprise empty lists.
    See also LUTS.FAMILIES, LUTS.DEMO.
    '''
    if _cmaps[name] is None:
        _load_plotly_cmaps()
        _load_colorcet_cmaps()
    _cmaps[name].sort()
    return _cmaps[name]

def names():
    '''LUTS.NAMES - Names of all available colormaps.
    x = LUTS.NAMES() returns a list of all the available colormaps.
    See also LUTS.DEMO.'''
    nn = sum([family(x) for x in families()], [])
    nn.sort()
    return nn

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
    t = (x - mu)/sigma*np.pi/2
    y = np.zeros(x.shape)
    use = np.logical_and(t>-np.pi, t<np.pi)
    y[use] = .5 + .5*np.cos(t[use])
    return y

# import daw.colorx
# cc = daw.colorx.dhsv(64)
# for x in cc: print(f"[{x[0]:.3f},{x[1]:.3f},{x[2]:.3f}],")
# copy output as hsvdata
_hsvdata = np.array([
        [1.000,0.164,0.000], [1.000,0.257,0.000], [1.000,0.343,0.000],
        [1.000,0.430,0.000], [1.000,0.522,0.000], [1.000,0.616,0.000],
        [1.000,0.706,0.000], [1.000,0.791,0.000], [1.000,0.864,0.000],
        [1.000,0.924,0.000], [1.000,0.970,0.000], [0.998,0.999,0.000],
        [0.966,1.000,0.000], [0.918,1.000,0.000], [0.853,1.000,0.000],
        [0.773,1.000,0.000], [0.677,1.000,0.000], [0.565,1.000,0.000],
        [0.434,1.000,0.000], [0.275,1.000,0.000], [0.008,1.000,0.081],
        [0.000,1.000,0.316], [0.000,1.000,0.466], [0.000,1.000,0.591],
        [0.000,1.000,0.698], [0.000,1.000,0.790], [0.000,1.000,0.865],
        [0.000,1.000,0.925], [0.000,1.000,0.969], [0.000,0.999,0.998],
        [0.000,0.972,1.000], [0.000,0.932,1.000], [0.000,0.883,1.000],
        [0.000,0.826,1.000], [0.000,0.765,1.000], [0.000,0.703,1.000],
        [0.000,0.643,1.000], [0.000,0.585,1.000], [0.000,0.528,1.000],
        [0.000,0.470,1.000], [0.000,0.408,1.000], [0.000,0.338,1.000],
        [0.000,0.255,1.000], [0.000,0.142,1.000], [0.115,0.001,1.000],
        [0.246,0.000,1.000], [0.343,0.000,1.000], [0.431,0.000,1.000],
        [0.515,0.000,1.000], [0.599,0.000,1.000], [0.684,0.000,1.000],
        [0.770,0.000,1.000], [0.854,0.000,1.000], [0.931,0.000,1.000],
        [0.988,0.000,1.000], [1.000,0.000,0.963], [1.000,0.000,0.881],
        [1.000,0.000,0.769], [1.000,0.000,0.642], [1.000,0.000,0.516],
        [1.000,0.000,0.399], [1.000,0.000,0.292], [1.000,0.000,0.185],
        [1.000,0.000,0.069]])
def _hsv(n=256):
    X = _hsvdata.shape[0]
    cc = np.zeros((n,3))
    xx = np.arange(X)
    ii = np.arange(n)*X/n
    for c in range(3):
        cc[:,c] = np.interp(ii, xx, _hsvdata[:,c], X)
    return cc

def _hot(n=300):
    xx = np.arange(0,1,1/n)
    yy = 0*xx
    red = _rankle(xx,5,.6)
    grn = _rankle(_ankle(xx,4,.4),3,.7)
    blu = _rankle(_ankle(xx,8,.7),1,.2)
    res = np.stack((red,grn,blu), 1)
    return np.clip(res, 0, 1)

def _cold(n=300):
    xx = np.arange(0,1,1/n)
    yy = 0*xx
    blu = _rankle(_ankle(xx,.6,.2),4,.5)
    grn = _rankle(_ankle(xx,2,.2),1.8,.7)
    red = _rankle(_ankle(xx,3,.6),1.2,.5)
    blu -= .35*_cosinebump(xx, .66,.17)
    blu = _rankle(blu, .7, .1)
    res = np.stack((red,grn,blu), 1)
    return np.clip(res, 0, 1)

def _jet(n=256):
    phi = np.linspace(0, 1, n)
    B0 = .2
    G0 = .5
    R0 = .8
    SB = .2
    SG = .25
    SR = .2
    P=4
    
    blue = np.exp(-.5*(phi-B0)**P / SB**P)
    red = np.exp(-.5*(phi-R0)**P / SR**P)
    green = np.exp(-.5*(phi-G0)**P / SG**P)
    return np.column_stack((red, green, blue))

def _native(name, N, reverse):
    from . import img
    if N is None:
        N = 256
    if name=='qpjet':
        rgb = _jet(N)
    elif name=='qphsv':
        rgb = _hsv(N)
    elif name=='qphot':
        rgb = _hot(N)
    elif name=='qpcold':
        rgb = _cold(N)
    elif name=='qpcoldhot':
        rgb = np.vstack((np.flipud(_cold(N//2)), _hot(N//2)))
    else:
        return None
    if reverse:
        rgb = np.flipud(rgb)
    return rgb

def _get_mpl_cmap(name, N, reverse):
    if type(name)==str:
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
    if reverse:
        return rgb[-1::-1,:]
    else:
        return rgb

def _get_colorcet_cmap(name, N, reverse):
    if not havecolorcet:
        return None
    _load_colorcet_cmaps()
    if name not in colorcet.__dict__:
        return None
    cmap = [[int(x[1:3], 16), int(x[3:5], 16), int(x[5:], 16)]
            for x in colorcet.__dict__[name]]
    rgb = np.array(cmap).astype(float)/255.0
    if N is not None:
        kk = np.arange(K)
        xx = np.arange(N) * (K-1) / (N-1)
        res = np.zeros((N, 3))
        for c in range(3):
            res[:,c] = np.interp(xx, kk, rgb[:,c])
    else:
        res = rgb
    if reverse:
        return res[-1::-1,:]
    else:
        return res
   
    
def _get_plotly_cmap(name, N, reverse):
    if not haveplotly:
        return None
    _load_plotly_cmaps()
    name = name.replace('-', '_')
    fam = None
    for f, lst in _cmaps.items():
        if lst is not None and name in lst:
            fam = f.replace('plotly.', '')
    if fam not in plotly.colors.__dict__:
        return None
    cmap = plotly.colors.__dict__[fam].__dict__[name]
    cmap = plotly.colors.validate_colors(cmap)
    K = len(cmap)
    rgb = np.zeros((K, 3))
    for k in range(K):
        r,g,b = cmap[k]
        rgb[k,:] = [r,g,b]
    if N is not None:
        kk = np.arange(K)
        xx = np.arange(N) * (K-1) / (N-1)
        res = np.zeros((N, 3))
        for c in range(3):
            res[:,c] = np.interp(xx, kk, rgb[:,c])
    else:
        res = rgb
    if reverse:
        return res[-1::-1,:]
    else:
        return res
        
def get(name, N=None, reverse=False):
    '''LUTS.GET - Retrieve a colormap.
    cm = LUTS.GET(name) retrieves the named colormap.
    Optional argument N specifies the number of colors to return. Default is
    dependent on the particular map.
    Optional argument REVERSE specifies that the order of the colors should
    be reversed.
    Use LUTS.FAMILIES, LUTS.FAMILY, LUTS.NAMES to explore available colormaps.
    See also LUTS.SET.'''
    if '.' in name:
        fam, name = name.split('.', 1)
    else:
        fam = None

    if fam is None or fam=="native":
        cmap = _native(name, N, reverse)
        if cmap is not None:
            return cmap
    if fam is None or (not fam.startswith("plotly")
                       and not fam.startswith("cet")):
        cmap = _get_mpl_cmap(name, N, reverse)
        if cmap is not None:
            return cmap
    if fam is None or fam.startswith("plotly"):
        cmap = _get_plotly_cmap(name, N, reverse)
        if cmap is not None:
            return cmap
    if fam is None or fam.startswith("cet"):
        cmap = _get_colorcet_cmap(name, N, reverse)
        if cmap is not None:
            return cmap
    
    raise ValueError(f'Unknown color map {name}')

def set(name, N=None, reverse=False):
    '''LUTS.SET - Retrieve and apply a colormap.
    LUTS.SET(name, N, reverse) is a shortcut for the corresponding
    call to LUTS.GET, followed by a call to LUT.
    Use LUTS.FAMILIES, LUTS.FAMILY, LUTS.NAMES to learn which colormaps exist.
    '''
    
    from . import img
    cm = get(name, N, reverse)
    img.lut(cm)
    
def demo(fam=None, N=None):
    '''LUTS.DEMO - Produce tableau of colormaps.
    LUTS.DEMO(family) produces a tableau of all the colormaps in the given
    family.
    LUTS.DEMO() produces separate tableaus for all families.
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
        if Q==0:
            return
        R = int(np.ceil(Q/2))
        C = int(np.ceil(Q/R))
        figname = f'luts-{fam}'
        fig.figure(figname, 3*C, R/4)
        style.pen('none')
        for c in range(C):
            fig.relpanel(chr(65+c), (c/C, 0, 1/C, 1))
            for r in range(R):
                data.plot([0,1],[-r,-r+.5])
        for q in range(Q):
            c = q//R
            r = q%R
            fig.panel(chr(65+int(c)))
            rgb = get(names[q], N)
            N1 = rgb.shape[0]
            rgb = rgb.reshape(1, N1, 3)
            if N1 <= 20 and N is None:
                img.image(rgb, rect=(0, -r-.15, 1, .3))
                rgb = get(names[q], (256//N1)*N1) 
                N1 = rgb.shape[0]
                rgb = rgb.reshape(1, N1, 3)
                img.image(rgb, rect=(0, -r+.25, 1, .3))
            else:
                img.image(rgb, rect=(0, -r, 1, .5))
            markup.at(0, -r+.25)
            markup.align('right', 'middle')
            txt = names[q]
            txt = txt.replace('_', '-')
            style.pen('k')
            markup.text(txt, dx=-5)
            fig.shrink()
