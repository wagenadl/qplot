import numpy as np
import tempfile
import os
import re
import utils

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
        self.lut_nan = [255, 255, 255]
        self.lut = np.repeat(np.reshape(np.arange(0,256),(256,1)),3,1)
        self.clim = (0, 1)
        self.panels = {} # Map from id to extent
        self.panel = None
        self.numfmt = '%g'
        self.legopt = None
        self.datarange = None
        self.atx = None
        self.aty = None
        self.legopt = None

    def write(self, s):
        # Can take either a string or a list of strings.
        # In the latter case, spaces are interpolated and newline is added.
        if type(s)==list:
            s = ' '.join(s) + '\n'
        self.fd.write(bytes(s, 'utf8'))
            
    def writedbl(self, v):
        v.astype('float64').tofile(self.fd)
    def writeuc(self, v):
        v.astype('uint8').tofile(self.fd)
        
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

    def format(self, xx):
        '''txt = FORMAT(xx) converts a matrix of numbers to a 
        list of strings using the current numfmt for the figure.'''
        return [ self.numfmt % x for x in xx ]

    def __init__(self, fn=None, w=5, h=None):
        if h is None:
            h = .75 * w
        MAXALLOWED = 36
        if w>MAXALLOWED or h>MAXALLOWED:
            error('Unreasonable size passed to qfigure. Units are inches!')
        w *= 72
        h *= 72
        self.extent = (0, 0, w, h)
        self.reset()
    
        if utils.isempty(fn):
            (fd, self.fn) = tempfile.mkstemp(suffix='.qpt')
            self.fd = open(fd, 'wb')
            self.istmp = True
        else:
            if not fn.endswith('.qpt'):
                fn = fn + '.qpt'
            self.fn = fn
            self.fd = open(fn, 'wb')
            self.istmp = False
    
        self.write('figsize %g %g\n' % (w,h))
        utils.unix('qpclient %s' % self.fn)

    def clf(self):
        self.fd.close()
        self.reset()
        self.fd = open(self.fn, 'wb')
        self.write('figsize %g %g\n' % (self.extent[2], self.extent[3]))

    def close(self):
        self.fd.close()
        self.fd = None
        utils.unix('qpclose %s' % self.fn)

    def tofront(self):
        utils.unix('touch %s' % fn) # This supposedly signals qplot to raise it

    def save(self, ofn, reso=None): 
        cmd = ['qplotml']
        if reso is not None:
            cmd.append('-r')
            cmd.append('%i' % reso)
        cmd.append(self.fn)
        cmd.append(ofn)
        s = utils.unix(' '.join(cmd))
        if s:
            error('qplot failed')
        
figs = {} # map from filename to Figure
f = None

def error(msg):
    raise ValueError(msg)

def ensure():
    global f, figs
    if f is None:
        f = Figure()
        figs[f.fn] = f

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
    '''MAPCOLOR - Map a matlab style color to qplot internal'''
    if s in colormap:
        return colormap[s]
    else:
        return None

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
        elif utils.alldigits(color) and len(color)==3:
            return '#%02x%02x%02x' % (int(255.999*int(color[0])/9),
    	                              int(255.999*int(color[1])/9), 
    	                              int(255.999*int(color[2])/9))
        elif utils.alldigits(color) and len(color)==6:
            return '#%02x%02x%02x' % (int(255.999*int(color[0:2])/99), 
    	                              int(255.999*int(color[2:4])/99), 
    	                              int(255.999*int(color[4:6])/99))
        else:
             error('Bad color specification')
    else:
        return '#%02x%02x%02x' % (int(255.999*color[0]),
    	                          int(255.999*color[1]),
    	                          int(255.999*color[2]))
 
def plot(xx, yy, cmd='plot'):
    xx = np.array(xx)
    yy = np.array(yy)
    if not utils.isnvector(xx):
        error('xx must be a real vector')
    if not utils.isnvector(yy):
        error('yy must be a real vector')
    if len(xx) != len(yy):
        error('xx and yy must be equally long')
    xx=xx[:,]
    yy=yy[:,]
    if utils.isempty(xx):
        return
    
    [iup, idn] = utils.schmitt(np.isnan(xx+yy)==False)
    
    ensure()
    for k in range(len(iup)):
        N = idn[k] - iup[k]
        f.write('%s *%i *%i\n' % (cmd, N, N))
        f.writedbl(xx[iup[k]:idn[k]])
        f.writedbl(yy[iup[k]:idn[k]])
    f.updaterange(xx, yy)
