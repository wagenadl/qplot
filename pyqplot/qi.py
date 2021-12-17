import numpy as np
import tempfile
import os
import re
import subprocess
from . import utils

here = "/".join(__file__.replace("\\", "/").split("/")[:-2])
exe = f"{here}/bin/qplot.exe"
if not os.path.exists(exe):
    exe = "qplot"

class Figure:
    global_interactive = True
    def interactive(k):
        Figure.global_interactive = k
    
    def reset(self):
        self.ticklen = 3
        self.axshift = 0
        self.ytitlerot = np.pi/2
        self.textdist = (3, 5)
        self.lastax = None
        self.lut_nan = np.array([255, 255, 255], dtype='uint8')
        self.lut = np.transpose(np.tile(np.arange(0,256,dtype='uint8'), (3,1)))
        self.clim = (0, 1)
        self.panels = {} # Map from id to extent
        self.panel = None
        self.numfmt = '%g'
        self.legopt = None
        self.datarange = None
        self.atx = None
        self.aty = None
        self.legopt = None
        self.imrect = None
        self.cbar = None
        self.overlinedist = 7
        self.overlinemin = 3
        self.linewidth = 0
        self.fontfamily = 'Helvetica'
        self.fontsize = 10
        self._xtransform = None # lambda x: x
        self._ytransform = None # lambda y: y

    def xtransform(self, x):
        if self._xtransform is not None:
            x = self._xtransform(x)
        if np.any(np.isinf(x)):
            raise Exception('Infinity')
        return x
    
    def ytransform(self, y):
        if self._ytransform is not None:
            y = self._ytransform(y)
        if np.any(np.isinf(y)):
            raise Exception('Infinity')
        return y

    def write(self, s):
        # Can take either a string or a list of strings.
        # In the latter case, spaces are interpolated and newline is added.
        if type(s)==list:
            s = ' '.join(s) + '\n'
        self.flushcounter = len(self.flushwaitre.findall(s))
        self.fd.write(bytes(s, 'utf8'))
        if True or self.flushcounter==0:
            self.fd.flush()
    flushcounter=0
    flushwaitre = re.compile(r' \*(uc)?\d')

    def writedbl(self, v):
        buf = np.array(v).astype('float64').tobytes(order='C')
        self.fd.write(buf)
        self.flushcounter -= 1
        if self.flushcounter<=0:
            self.fd.flush()
    def writeuc(self, v):
        buf = np.array(v).astype('uint8').tobytes(order='C')
        self.fd.write(buf)
        self.flushcounter -= 1
        if self.flushcounter<=0:
            self.fd.flush()
            
    def updaterange(self, xx, yy):
        if len(xx)==0 or len(yy)==0:
            return
        mx = np.min(xx)
        Mx = np.max(xx)
        my = np.min(yy)
        My = np.max(yy)
        if np.isnan(mx) or np.isnan(Mx) or np.isnan(my) or np.isnan(My):
            return
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
        self.is_interactive = Figure.global_interactive
        self.is_pipe = False
        self.is_tempfile = False
        if h is None:
            h = .75 * w
        MAXALLOWED = 36
        if w>MAXALLOWED or h>MAXALLOWED:
            error('Unreasonable size passed to qfigure. Units are inches!')
        w *= 72
        h *= 72
        self.extent = (0, 0, w, h)
        self.reset()

        if self.is_interactive:
            # Create a pipe
            if utils.isempty(fn):
                fn = tempfile.mktemp(dir='')
            self.fn = fn
            self.pipe = subprocess.Popen([exe, "--title", fn, "-"],
                                        stdin=subprocess.PIPE)
            self.fd = self.pipe.stdin
            self.is_pipe = True
        else:
            if utils.isempty(fn):
                (fd, self.fn) = tempfile.mkstemp(suffix='.qpt')
                self.is_tempfile = True
            else:
                if not fn.endswith('.qpt'):
                    fn = fn + '.qpt'
                self.fn = fn
            self.fd = open(fn, 'wb')
    
        self.write('figsize %g %g\n' % (w,h))


    def clf(self):
        if not self.is_pipe:
            self.fd.close()
            self.fd = open(self.fn, 'wb')
        self.reset()
        self.write('figsize %g %g\n' % (self.extent[2], self.extent[3]))

    def close(self):
        if self.is_pipe:
            self.pipe.terminate()
            self.is_pipe = False
            self.fd = None
        elif self.fd is not None:
            self.fd.close()
            self.fd = None

    def tofront(self):
        pass

    def save(self, ofn, reso=None, qual=None):
        if self.is_pipe:
            cmd = f'save "{ofn}"';
            if reso is not None:
                cmd += f' {reso}'
                if qual is not None:
                    cmd += f' {qual}'
            self.write(cmd + '\n')
        else:
            cmd = ['qplot']
            if reso is not None:
                cmd.append('-r')
                cmd.append('%i' % reso)
            if qual is not None:
                cmd.append('-q')
                cmd.append('%i' % qual)
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
        for fn in figs:
            f = figs[fn]
            return
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

markermap = { 'o': 'circle',
            's': 'square',
            'd': 'diamond',
            '<': 'left',
            '>': 'right',
            '^': 'up',
            'v': 'down',
            'p': 'penta',
            'h': 'hexa',
            '+': 'plus',
            'x': 'cross',
            '-': 'hbar',
            '|': 'vbar'
}

def mapmarker(s):
    '''MAPMARKER - Map a matlab style marker to qplot internal'''
    if s in markermap:
        return markermap[s]
    else:
        return None

def interpretcolor(color):
    '''Converts a color to #RRGGBB form. Input may be in 'RGB', 'RRGGBB',
    [r, g, b], or a single character. Color may also be '' or 'none' which
    translate to 'none', or None, which is returned unchanged.'''
    if color is None:
        return None
    elif type(color)==str:
        if color in colormap:
            return colormap[color]        
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
    
    ensure()
    N = len(xx)
    f.write('%s *%i *%i\n' % (cmd, N, N))
    if cmd=='plot' or cmd=='patch':
        xx = f.xtransform(xx)
        yy = f.ytransform(yy)
    f.writedbl(xx)
    f.writedbl(yy)
    f.updaterange(xx, yy)

def figisopen(fn):
    if fn is None:
        return False
    f1 = None
    if fn in figs:
        f1 = figs[fn]
    elif not fn.endswith('.qpt'):
        fn = fn + '.qpt'
        if fn in figs:
            f1 = figs[fn]
    if f1 is None:
        return False
    try:
        f1.pipe.wait(0)
    except subprocess.TimeoutExpired:
        return True # Still open
    # We're here, so evidently, the figure got closed externally
    f1.close()
    del figs[fn]
    return False

def refigure(fn, w, h):
    f1 = None
    if fn in figs:
        f1 = figs[fn]
    elif not fn.endswith('.qpt'):
        fn = fn + '.qpt'
        if fn in figs:
            f1 = figs[fn]
    if f1 is None:
        f1 = qi.Figure(fn, w, h)
        figs[f1.fn] = f1
        return f1

    if h is None:
        h = .75 * w
    w = w*72
    h = h*72
    f1.extent = (0, 0, w, h)
    f1.clf()
    return f1
