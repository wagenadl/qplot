import numpy as np
import tempfile
import os
import re
import subprocess
import time
from . import utils
import sys


here = "/".join(__file__.replace("\\", "/").split("/")[:-2])
exe = f"{here}/bin/qplot.exe"
if not os.path.exists(exe):
    exe = "qplot"


    
class Figure:
    latest_fn = None
    global_interactive = True
    
    def interactive(k):
        Figure.global_interactive = k
        

    global_degrees = False
    def use_degrees():
        Figure.global_degrees = True
    def use_radians():
        Figure.global_degrees = False
    
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
        self.linewidth = 0.5 # match with default in style.pen()
        self.fontfamily = 'Helvetica'
        self.fontsize = 10
        self._xtransform = None # lambda x: x
        self._ytransform = None # lambda y: y
        self.reftext = ''

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
        if self.flushcounter==0:
            self.fd.flush()

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
        mx = np.nanmin(xx)
        Mx = np.nanmax(xx)
        my = np.nanmin(yy)
        My = np.nanmax(yy)
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

    def __init__(self, fn, w, h):
        self.is_interactive = Figure.global_interactive
        self.is_pipe = False
        self.pid = None
        self.is_tempfile = False
        MAXALLOWED = 36
        if w>MAXALLOWED or h>MAXALLOWED:
            error('Unreasonable size passed to qfigure. Units are inches!')
        w *= 72
        h *= 72
        self.extent = (0, 0, w, h)
        self.reset()

        if self.is_interactive:
            if fn is not None and fn.startswith("/"):
                # Create a file
                if not fn.endswith('.qpt'):
                    fn = fn + '.qpt'
                self.fn = fn
                self.fd = open(fn, 'wb')
                self.pid = subprocess.Popen([exe, fn])
                # We use the "pipe" as a pid, but is_pipe is False
            else:
                # Create a pipe
                if utils.isempty(fn):
                    fn = tempfile.mktemp(dir='')
                self.fn = fn
                self.pid = subprocess.Popen([exe, "--title", fn, "-"],
                                            stdin=subprocess.PIPE)
                self.fd = self.pid.stdin
                self.is_pipe = True
        else:
            if fn is None or fn=='':
                (fd, self.fn) = tempfile.mkstemp(suffix='.qpt')
                self.is_tempfile = True
            else:
                if not fn.endswith('.qpt'):
                    fn = fn + '.qpt'
                    if "/" not in fn:
                        self.is_tempfile = True
                self.fn = fn
            self.fd = open(self.fn, 'wb')
    
        self.write('figsize %g %g\n' % (w,h))
        Figure.latest_fn = self.fn

    def raise_on_stopped(self):
        if self.pid is None:
            return
        try:
            ret = self.pid.wait(0)
            if ret < 0:
                raise BrokenPipeError("QPlot subprocess died")
        except subprocess.TimeoutExpired:
            pass
            

    def clf(self):
        if not self.is_pipe:
            self.fd.close()
            self.fd = open(self.fn, 'wb')
        self.reset()
        self.write('figsize %g %g\n' % (self.extent[2], self.extent[3]))

    def close(self):
        self.raise_on_stopped()
        if self.fd is not None:
            self.fd.close()
            self.fd = None
        if self.pid is not None and self.is_pipe:
            try:
                ret = self.pid.wait(2)
                self.pid = None
            except subprocess.TimeoutExpired:
                print("timeout", time.time())
        if self.pid is not None:
            self.pid.terminate()
            self.pid.wait()
            self.pid = None
        self.is_pipe = False
        if self.is_tempfile:
            os.unlink(self.fn)


    def tofront(self):
        pass

    def check_save_success(self, stt, ofn):
        t0 = time.time()
        while time.time() < t0 + 5:
            self.raise_on_stopped()
            if os.path.exists(ofn):
                if stt is None:
                    return # New file created, happy
                stt1 = os.stat(ofn)
                if stt1.st_mtime > stt.st_mtime:
                    return # File updated, happy
        raise BrokenPipeError("QPlot failed to save")


    def save(self, ofn, reso=None, qual=None):
        if self.is_pipe:
            cmd = f'save "{ofn}"'
            if reso is not None:
                cmd += f' {reso}'
                if qual is not None:
                    cmd += f' {qual}'
            if os.path.exists(ofn):
                stt = os.stat(ofn)
            else:
                stt = None
            self.write(cmd + '\n')
            self.check_save_success(stt, ofn)
        else:
            if self.fd is not None:
                self.fd.flush()
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
                raise BrokenPipeError('qplot failed')

        
figs = {} # map from filename to Figure
f = None


def to_radians(angle):
    if Figure.global_degrees:
        return np.pi * angle / 180
    else:
        return angle


def error(msg):
    raise ValueError(msg)

def ensure():
    global f, figs
    if f is None:
        for fn in figs:
            f = figs[fn]
            if f.pid is None:
                return # Non-interactive figure, hope for the best
            if f.pid.poll() is None: # hopefully this is fast??
                return # Figure still open
            else:
                f.close() # User has closed it; close it from our end

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
        f.updaterange(xx, yy)
    f.writedbl(xx)
    f.writedbl(yy)

def hatch(xx, yy, pattern, angle, spacing, offset, cmd='hatch'):
    angle = to_radians(angle)
    if pattern=='|':
        pass
    elif pattern=='/':
        angle = np.pi/4
    elif pattern=='-':
        angle = np.pi/2
    elif pattern=='\\':
        angle = -np.pi/4
    elif pattern=='x':
        hatch(xx, yy, '/', angle=0, spacing=spacing, offset=offset, cmd=cmd)
        angle = -np.pi/4
    elif pattern=='+':
        hatch(xx, yy, '-', angle=0, spacing=spacing, offset=offset, cmd=cmd)
        angle = 0
    elif pattern=='*':
        angle = '*'
    elif pattern==':':
        angle = ':'
    else:
        print("hatch", pattern, angle)
        raise ValueError("Hatch pattern must be one of | / - \\ + x * :")
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
    if type(angle)==str:
        f.write('%s *%i *%i "%s" %g %g\n' % (cmd, N, N, angle, spacing, offset))
    else:
        f.write('%s *%i *%i %g %g %g\n' % (cmd, N, N, angle, spacing, offset))
    if cmd=='hatch':
        xx = f.xtransform(xx)
        yy = f.ytransform(yy)
        f.updaterange(xx, yy)
    f.writedbl(xx)
    f.writedbl(yy)
    

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
        f1.pid.wait(0)
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
        f1 = Figure(fn, w, h)
        figs[f1.fn] = f1
        return f1

    if h is None:
        h = .75 * w
    w = w*72
    h = h*72
    f1.extent = (0, 0, w, h)
    f1.clf()
    return f1


def test_jupyter():
    if "IPython" not in sys.modules:
        return False
    ipy = sys.modules["IPython"].core.getipython.get_ipython()
    if ipy.__class__.__name__ != "ZMQInteractiveShell":
        return False
    
    Figure.interactive(False)
    ipy.events.register("post_run_cell", post_jupyter)
    # print("QPlot running in notebook")

    
def post_jupyter(cel_):
    if Figure.latest_fn not in figs:
        return
    f = figs[Figure.latest_fn]
    (fd1, fn1) = tempfile.mkstemp(suffix='.png')
    f.save(fn1, 216)
    disp = sys.modules["IPython"].display
    disp.display(disp.Image(fn1, retina=True))
    os.unlink(fn1)
    if not Figure.global_interactive:
        f.close()
        del figs[Figure.latest_fn]
    Figure.latest_fn = None


test_jupyter()
        
