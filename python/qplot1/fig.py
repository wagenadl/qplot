import numpy as np
import tempfile
import os
import re
import core

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

    def __init__(fn, w, h):
        if h is None:
            h = .75 * w
        MAXALLOWED = 36
        if w>MAXALLOWED or h>MAXALLOWED:
            qi.error('Unreasonable size passed to qfigure. Units are inches!')
    
        if qi.isempty(fn):
            (self.fd, self.fn) = tempfile.mkstemp(suffix='.qpt')
            self.istmp = True
        else:
            if not fn.endswith('.qpt'):
                fn = fn + '.qpt'
            self.fn = fn
            self.fd = open(fn, 'wb')
            self.istmp = False
    
        w *= 72
        h *= 72
        self.extent = [0, 0, w, h]
        qi.write('figsize %g %g\n' % (w,h))
        qi.unix('qpclient %s' % fn)
        self.flush()
