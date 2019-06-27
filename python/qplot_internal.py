import numpy as np
import tempfile
import os
import re

figs = {} # map from filename to QFigure
curfn = None

def error(msg):
    raise ValueError(msg)


def alldigits(x):
    '''ALLDIGITS - True if a string contains only digits'''
    if alldigits.regex.match(x):
        return True
    else:
        return False
alldigits.regex = re.compile('^\d+$')

def isempty(x):
    if x is None:
        return True
    elif type(x)==list:
        return len(x)==0
    elif type(x)==str:
        return len(x)==0
    elif type(x)==np.array:
        return len(x)==0
    else:
        return False

def isnscalar(x):
    '''ISNSCALAR - True if array is a real numeric scalar.
  ISNSCALAR(x) returns True if X is a scalar numeric array, False if not.'''
    try:
        ok = float(x)
        return True
    except TypeError:
        return False

def isnvector(x):
    '''ISNVECTOR - True if array is a numeric vector of real numbers.
   ISNVECTOR(x) returns True if X is an 1xN or Nx1 numeric array, 
   False if not.'''
    # THIS MUST BE IMPROVED
    try:
        if isnscalar(x):
            return True
        ok = x+0
        if np.prod(x.shape) == x.size:
            return True
        else:
            return False
    except TypeError:
        return False

def wordset(s):
    '''WORDSET splits a string up at spaces and returns a dict pointing
each word to 1.'''
    return { k: 1 for k in s.split() }

def write(s):
    fd = qdata.figs[qdata.curfn].fd
    fd.write(bytes(s, 'utf8'))

def writedbl(v):
    v = v.astype('float64')
    v.tofile(qdata.figs[qdata.curfn].fd)

def unix(s):
    os.system(s)

def flush(fn=[]):
    if isempty(fn):
        fn = qdata.curfn
    # Now what:

def reset(fn=[]):
    if isempty(fn):
        fn = qdata.curfn
    qdata.figs[fn].ticklen = 3
    qdata.figs[fn].axshift = 0
    qdata.figs[fn].ytitlerot = np.pi/2
    qdata.figs[fn].textdist = [3, 3]
    qdata.figs[fn].lastax = ''
    qdata.figs[fn].lut_nan = [1, 1, 1]
    qdata.figs[fn].panelextent = {}
    qdata.figs[fn].panel = '-'
    qdata.figs[fn].numfmt = ''
    qdata.figs[fn].legopt = []
    qdata.figs[fn].datarange = [np.nan, np.nan, np.nan, np.nan]

def updaterange(xx, yy):
    dr = qdata.figs[qdata.curfn].datarange
    mx = np.min(xx)
    Mx = np.max(xx)
    my = np.min(yy)
    My = np.max(yy)
    if np.isnan(dr[0]) or mx<dr[0]:
        dr[0] = mx
    if np.isnan(dr[1]) or Mx>dr[1]:
        dr[1] = Mx
    if np.isnan(dr[2]) or my<dr[2]:
        dr[2] = my
    if np.isnan(dr[3]) or My>dr[3]:
        dr[3] = My
    qdata.figs[qdata.curfn].datarange = dr
    
# ------------------------------------------------------
class Figure:
    fd = None
    fn = None
    istmp = False
    extent = [0,0,1,1]

def figure(fn=None, w=5, h=None):
    '''FIGURE - Open a QPlot figure
    FIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
    in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
    W defaults to 5 inches.
    fn = FIGURE([], w, h) opens a new QPlot figure of given size (in inches)
    with a temporary filename.'''
    if isempty(h):
        h = .75 * w
    MAXALLOWED = 36
    if w>MAXALLOWED or h>MAXALLOWED:
        error('Unreasonable size passed to qfigure. Units are inches!')

    if fn in qdata.figs:
        qdata.curfn = fn
        return fn

    fig = Figure
    if isempty(fn):
        (fig.fd, fig.fn) = tempfile.mkstemp(suffix='.qpt')
        fig.istmp = True
    else:
        if not fn.endswith('.qpt'):
            fn = fn + '.qpt'
        fig.fn = fn
        fig.fd = open(fn, 'wb')
        fig.istmp = False

    w *= 72
    h *= 72
    fig.extent = [0, 0, w, h]
    data.figs[fn] = fig
    data.curfn = fn
    write('figsize %g %g\n' % (w,h))
    reset()
    unix('qpclient %s' % fn)
    flush()

def ensure():
    # Now returns curfn as index into figs
    if isempty(data.curfn):
        figure()
    return data.curfn

def schmitt(xx):
    N = len(xx)
    iup = []
    idn = []
    state = False
    for n in range(N):
        if state:
            if not(xx[n]):
                idn.append(n)
                state = False
        else:
             if xx[n]:
                 iup.append(n)
                 state = True
    if state:
        idn.append(N)
    return (iup, idn)

colormap = { 'r': 'red',
             'g': 'green',
             'b': 'blue',
             'm': 'magenta'
             'y': 'yellow',
             'c': 'cyan',
             'k': 'black',
             'w': 'white'
}
def mapcolor(s):
    if s in colormap:
        return colormap[s]
    else:
        return None

def plot_(xx, yy, cmd='plot'):
    ensure()

    xx = np.array(xx)
    yy = np.array(yy)
    if not isnvector(xx):
        error('xx must be a real vector')
    if not isnvector(yy):
        error('yy must be a real vector')
    if len(xx) != len(yy):
        error('xx and yy must be equally long')
    xx=xx[:,]
    yy=yy[:,]
    if isempty(xx):
        return
    
    [iup, idn] = schmitt(np.isnan(xx+yy)==False)
    
    for k in range(len(iup)):
        N = idn[k] - iup[k]
        write('%s *%i *%i\n' % (cmd, N, N))
        writedbl(xx[iup[k]:idn[k]])
        writedbl(yy[iup[k]:idn[k]])
    flush()
    
    updaterange(xx, yy)

def format(xx):
    '''txt = FORMAT(xx) converts a matrix of numbers to a 
list of strings using the current numfmt for the figure.'''
    
    ensure()
    idx = idx
    global data
    fmt = data.figs[fn].numfmt
    
    S = size(xx)
    txt=cell(S)
    
    if isempty(fmt):
        for k=1:prod(S):
            txt{k} = num2str(xx(k))
    else:
        for k=1:prod(S):
            txt{k} = sprintf(fmt, xx(k))
    
    
