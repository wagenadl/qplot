import numpy as np
import tempfile
import os
import re
import fig
    
figs = {} # map from filename to Figure
curfig = None

def error(msg):
    raise ValueError(msg)

def write(s):
    curfig.write(s)

def writedbl(v):
    curfig.writedbl(v)



def ensure():
    # Now returns curfn as index into figs
    if curfig is None:
        figure()
    return curfig.fn



# A GLC is a tuple (cmd, arg) or (cmd, arg, arg2).
# A PTSPEC is a list of GLCS.
def gline(cmd='gline', ptspecs=[]):
    out = [cmd]
    for pt in ptspecs:
        out.append('(')
        for glc in pt:
            out.append(glc[0])
            if type(glc[1])==str:
                out.append(glc[1])
            else:
                out.append('%g' % glc[1])
            if len(glc)>=3:
                out.append('%g' % glc[2])
        out.append(')')
    write(' '.join(out))

# A VGLC is a GLC where each arg may be a vector
def gline2(cmd='gline', vglcs):
    N = None
    for vgl in vglcs:
        a1 = aslist(vgl[1])
        n = len(a1)
        if N is None:
            N = n
        elif n>1 and n!=N:
            error('Mismatching point count')
    if N is None:
        return
    pts = []
    for n in range(N):
        pts.append([])
    for vgl in vglcs:
        a1 = aslist(vgl[1])
        n = len(a1)
        if len(vgl)>=3:
            a2 = aslist(vgl[2])
        else:
            a2 = None
        if n==1:
            a1 = a1[0]
            if a2 is None:
                for n in range(N):
                    pts[n].append((vgl[0], a1))
            else:
                a2 = a2[0]
                for n in range(N):
                    pts[n].append((vgl[0], a1, a2))
        else:
            if a2 is None:
                for n in range(N):
                    pts[n].append((vgl[0], a1[n]))
            else:
                for n in range(N):
                    pts[n].append((vgl[0], a1[n], a2[n]))
    gline(cmd, pts)
                    
colormap = { 'r': 'red',
             'g': 'green',
             'b': 'blue',
             'm': 'magenta',
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

def plot(xx, yy, cmd='plot'):
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
    curfig.flush()
    curfig.updaterange(xx, yy)

def format(xx):
    '''txt = FORMAT(xx) converts a matrix of numbers to a 
list of strings using the current numfmt for the figure.'''
    ensure()
    fmt = curfig.numfmt
    return [ fmt % x for x in xx ]
    
def aslist(x):
    '''ASLIST - Convert almost anything to a list.
    y = ASLIST(x) puts scalar numbers in a list. It converts numpy
    arrays to one-dimensional as well. ASLIST does not change tuples to
    lists. It also does not change numpy arrays to lists.
    The result will have LEN defined and is indexible.'''
    if type(x)==list:
        return x
    elif type(x)==tuple:
        return x
    elif type(x)==np.array:
        return np.reshape(x, x.size)
    else:
        return [x]

def interpretcolor(color):
    '''Converts a color to #RRGGBB form. Input may be in 'RGB', 'RRGGBB',
    [r, g, b], or a single character. Color may also be '' or 'none' which
    translate to 'none', or None, which is returned unchanged.'''
    if color is None:
        return None
    elif color in colormap:
        return colormap[color]
    elif type(color)==str:
        if color=='' or color=='none':
            return 'none'
        elif alldigits(color) and len(color)==3:
            return '#%02x%02x%02x' % (int(255.999*int(color[0])/9),
    	                              int(255.999*int(color[1])/9), 
    	                              int(255.999*int(color[2])/9))
        elif alldigits(color) and len(color)==6:
            return '#%02x%02x%02x' % (int(255.999*int(color[0:2])/99), 
    	                              int(255.999*int(color[2:4])/99), 
    	                              int(255.999*int(color[4:6])/99))
        else:
             error('Bad color specification')
    else:
        return '#%02x%02x%02x' % (int(255.999*color[0]),
    	                          int(255.999*color[1]),
    	                          int(255.999*color[2]))
 
def sensiblestep(mx):
    '''dx = SENSIBLESTEP(mx) returns a sensible step size not much smaller
    than MX:

      1<=MX<2  -> DX=1
      2<=MX<5  -> DX=2
      5<=MX<10 -> DX=5
    etc.'''
    
    lg=np.log10(mx)
    ord=np.floor(lg)
    sub = 10**(lg-ord)
    if sub>5:
        sub=5
    elif sub>2:
        sub=2
    else:
        sub=1
    return sub * 10**ord

def sensibleticks(xxx, cnt=5, inc=False):
    '''SENSIBLETICKS - Coordinates of sensible ticks
    tx = SENSIBLETICKS(xxx) returns approx. 5 ticks that span the range of  
    the data XXX.
    Optional argument CNT overrides the approx. number.
    Optional argument INC, if True, makes the ticks extend past the data. (The
    default is for the ticks to not go beyond the data limits.)'''
    xd = np.array(xxx)
    x0 = np.min(xd)
    x1 = np.max(xd)
    rng = x1 - x0
    tx=[]
    scl=1
    while len(tx)<cnt:
        dx = sensiblestep(rng/scl)
        if inc:
            x0a = np.floor(x0/dx)*dx
        else:
            x0a = np.ceil(x0/dx)*dx
        if inc:
            x1a = np.ceil(x1/dx)*dx
        else:
            x1a = np.floor(x1/dx)*dx
        print(x0a, x1a, dx)
        tx = np.arange(x0a, x1a+dx/2, dx)
        scl = scl*1.5
    return tx

