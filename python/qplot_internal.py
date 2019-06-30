import numpy as np
import tempfile
import os
import re

# ------------------------------------------------------
class Figure:
    fd = None
    fn = None
    istmp = False
    extent = [0,0,1,1]
    def reset(self):
        self.ticklen = 3
        self.axshift = 0
        self.ytitlerot = np.pi/2
        self.textdist = (3, 3)
        self.lastax = None
        self.lut_nan = [1, 1, 1]
        self.panelextent = {}
        self.panel = '-'
        self.numfmt = '%g'
        self.legopt = None
        self.datarange = None
        self.atx = None
        self.aty = None
    def __init__(self):
        self.reset()
    def write(self, s):
        self.fd.write(bytes(s, 'utf8'))
        if not s.endswith('\n'):
            self.fd.write(b'\n')
    def writedbl(self, v):
        v.astype('float64').tofile(self.fd)
    def flush(self):
        pass
    def updaterange(self, xx, yy):
        mx = np.min(xx)
        Mx = np.max(xx)
        my = np.min(yy)
        My = np.max(yy)
        if self.datarange is None:
            self.datarange = [mx, Mx, my, My]
        else:
            if mx<self.datarange[0]:
                self.datarange[0] = mx
            if Mx>self.datarange[1]:
                self.datarange[1] = Mx
            if my<self.datarange[2]:
                self.datarange[2] = my
            if My>self.datarange[3]:
                self.datarange[3] = My

class CBar:
    clim = [0, 1]
    orient = 'x'
    xywh_d = [0,0,1,1]
    xywh_p = [0,0,1,1]
    rev = False
    def ctodat(self, cc):
        crel = (cc-self.clim[0]) / (self.clim[1]-self.clim[0])
        if self.orient=='y':
            rng = self.xywh_d[3]
            d0 = self.xywh_d[1]
        elif self.orient=='x':
            rng = self.xywh_d[2]
            d0 = self.xywh_d[0]
        if self.rev:
            d0 = d0+rng
            rng = -rng
        return d0 + rng*crel

    def ctopap(self, cc):
        crel = (cc-self.clim[0]) / (self.clim[1]-self.clim[0])
        if self.orient=='y':
            rng = self.xywh_p[3]
            d0 = self.xywh_p[1]
        elif self.orient=='x':
            rng = self.xywh_p[2]
            d0 = self.xywh_p[0]
        if not self.rev:
            d0 = d0+rng
            rng = -rng
        return d0 + rng*crel
    
figs = {} # map from filename to Figure
curfig = None

def error(msg):
    raise ValueError(msg)

def write(s):
    curfig.write(s)

def writedbl(v):
    curfig.writedbl(v)

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

def unix(s):
    os.system(s)


def ensure():
    # Now returns curfn as index into figs
    if curfig is None:
        figure()
    return curfig.fn

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

def startgroup():
    ensure()
    write('group')

def endgroup():
    ensure()
    write('endgroup')

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

def axis(orient='x', lim_d=None, tick_d=None, tick_p=None,
         tick_lbl=None, ttl='',
         ticklen=3, lbldist=3, ttldist=3,
         coord_d=None, coord_p=0,
         ttlrot=0,
         cbar=None):
    '''QI.AXIS - Internal backend for axis rendering
    QI.AXIS(...) draws an axis according to the parameters:
      orient: 'x' or 'y'
      lim_d (2x1) limits of the axis in data coordinates (in the direction
                              of ORIENT)
      lim_p (2x1) shift of those limits in paper coordinates
      tick_d (Nx1) data coordinates (in the direction of ORIENT) of ticks
      tick_p (Nx1) shift of those coords in paper coordinates
      tick_lbl {Nx1} labels to be placed at those ticks
      ttl (string) title
      ticklen (scalar) length of ticks, +ve is down/right
      lbldist (scalar) dist b/w labels and axis/ticks, +ve is down/right
      ttldist (scalar) dist b/w title and labels/axis/ticks, +ve is down/right
      coord_d (scalar) position of the axis in data coords (in the direction
                                         orthogonal to ORIENT)
      coord_p (scalar) shift of that position in paper coordinates
      ttlrot (scalar) rotation of title: 0=normal +ve=CCW -ve=CW
          cbar (struct) optional reference to colorbar'''

    ensure()
    curfig.lastax = { 'orient': orient,
                      'lim_d': lim_d,
                      'tick_d': tick_d,
                      'tick_p': tick_p,
                      'tick_lbl': tick_lbl,
                      'ttl': ttl,
                      'ticklen': ticklen,
                      'lbldist': lbldist,
                      'ttldist': ttldist,
                      'coord_d': coord_d,
                      'coord_p': coord_p,
                      'ttlrot': ttlrot,
                      'cbar': cbar
                      }
                      
    if orient=='x':
        ishori=1
        isvert=0
    elif orient=='y':
        ishori=0
        isvert=1
    else:
        error("orient must be 'x' or 'y'")    
    if isempty(lim_d):
        lim_d = np.zeros(lim_p.shape) + np.nan
    elif isempty(lim_p):
        lim_p = np.zeros(lim_d.shape)
    
    if isempty(tick_d):
        tick_d = np.zeros(tick_p.shape) + nan
    elif isempty(tick_p):
        tick_p = np.zeros(tick_d.shape)
    
    startgroup()
    
    tickdx = tick_d
    tickdy = np.zeros(tickdx.shape)+coord_d
    tickpx = tick_p
    tickpy = np.zeros(tickpx.shape)+coord_p
    ticklx = 0
    tickly = ticklen
    lbllx = 0
    lblly = lbldist
    
    if np.sign(tickly)==np.sign(lblly):
        lblly=lblly+tickly
    
    # Axis line position (x and y may be flipped later!)
    limdx = lim_d
    limdy = coord_d+np.zeros((2))
    limpx = lim_p
    limpy = coord_p+np.zeros((2))
    
    if not isempty(lim_d) and not np.isnan(lim_d[0]):
        ttldx = np.mean(limdx)
    elif not isempty(tick_d) and not isnan(tick_d[0]):
        ttldx = mean([tickdx[0] tickdx[-1]])
    else:
        ttldx = np.nan
    ttldy = coord_d
    
    if not isempty(lim_p):
        ttlpx = np.mean(limpx)
    elif not isempty(tick_p)
        ttlpx = np.mean([tickpx[0] tickpx[-1]])
    else:
        ttlpx = 0
    ttlpy = coord_p
    
    # Draw an axis line if desired
    if not isempty(lim_d):
        if isvert:
            (limdx, limdy) = (limdy, limdx)
            (limpx, limpy) = (limpy, limpx)
        gline(absdatax=limdx, absdatay=limdy,
              relpaperx=limpx, relpapery=limpy)
    
    # Draw ticks if desired
    if isvert:
        [tickdx, tickdy] = identity(tickdy, tickdx)
        [tickpx, tickpy] = identity(tickpy, tickpx)
        [ticklx, tickly] = identity(tickly, ticklx)
        [lbllx, lblly]     = identity(lblly, lbllx)
    if ticklen~=0:
        for k=1:length(tickdx):
            qgline({ 'absdata',    tickdx(k), tickdy(k), ...
    	         'relpaper', tickpx(k), tickpy(k) }, ...
    	     { 'absdata',    tickdx(k), tickdy(k), ...
    	         'relpaper', tickpx(k)+ticklx, tickpy(k)+tickly })
    
    # Draw labels if desired
    if ~isempty(tick_lbl):
        qgroup
        [xa, ya] = qpa_align(ishori, lbllx, lblly)
        qalign(xa, ya)
        if ishori:
            reftxt=''
            for k=1:length(tick_lbl):
                if str2double(tick_lbl{k}) < 0:
    	tick_lbl{k} = [ tick_lbl{k} ' ' ]
                reftxt = [ reftxt tick_lbl{k} ]
            qreftext(reftxt)
    
        for k=1:length(tick_lbl):
            qat(tickdx(k), tickdy(k))
            qtext(tickpx(k)+lbllx, tickpy(k)+lblly, tick_lbl{k})
    
        qreftext('')
        qendgroup
    
    # Draw title if desired
    if ~isempty(ttl):
        ttllx = 0
        ttlly = ttldist
        if isvert:
            [ttlpx, ttlpy] = identity(ttlpy, ttlpx)
            [ttllx, ttlly] = identity(ttlly, ttllx)
            [ttldx, ttldy] = identity(ttldy, ttldx)
    
    
        if isempty(tick_lbl) || sign(ttldist)~=sign(lbldist):
            # Ignore labels when placing title: not on same side
            if sign(ttldist)==sign(ticklen):
                ttllx = ttllx + ticklx
                ttlly = ttlly + tickly
            qat(ttldx, ttldy, -pi/2*sign(ttlrot))
        else:
            if ishori:
                ttlpy=0
            else:
                ttlpx=0
            [xa, ya] = qpa_align(ishori, -ttldist)
            if ishori:
                qat(ttldx, ya, -pi/2*sign(ttlrot))
            else:
                qat(xa, ttldy, -pi/2*sign(ttlrot))
        if ttlrot==0:
            [xa, ya] = qpa_align(ishori, ttldist)
        else:
            [xa, ya] = qpa_align(isvert, ttldist*sign(ttlrot))
        qalign(xa, ya)
        if ttlrot:
            qtext(-sign(ttlrot)*(ttlpy+ttlly), ...
    	sign(ttlrot)*(ttlpx+ttllx), ttl)
        else:
            qtext(ttlpx+ttllx, ttlpy+ttlly, ttl)
    qendgroup
