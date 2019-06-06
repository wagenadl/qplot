import numpy as np
import tempfile
import os

class QPData:
    figs = {} # map from filename to QFigure
    curfn = None

qdata = QPData

def error(msg):
    raise ValueError(msg)

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

def qp_allnumeric(x):
    for c in x:
        if c<'0' or c>'9':
            return False
    return True

# ------------------------------------------------------
#  function fn = qp_idx(autofig)
def qp_idx(autofig=False):
    if isempty(qp_data.curfn):
        if autofig:
            qfigure()
        else:
            error('No open window')
    
    return qp_data.curfn
        
# ------------------------------------------------------
#  function yes=isnscalar(x)
def isnscalar(x):
    '''
ISNSCALAR  True if array is a numeric scalar.
  ISNSCALAR(x) returns True if X is a scalar numeric array, False if not.
'''
    try:
        ok = float(x)
        return True
    except TypeError:
        return False

# ------------------------------------------------------
#  function yes=isnvector(x)
def isnvector(x):
    '''
ISNVECTOR  True if array is a numeric vector.
   ISNVECTOR(x) returns True if X is an 1xN or Nx1 numeric array, 
   False if not.
'''
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

def qp_write(s):
    fd = qdata.figs[qdata.curfn].fd
    fd.write(bytes(s, 'utf8'))

def qp_writedbl(v):
    v = v.astype('float64')
    v.tofile(qdata.figs[qdata.curfn].fd)

def qp_unix(s):
    os.system(s)

def qp_flush(fn=[]):
    if isempty(fn):
        fn = qdata.curfn
    # Now what:

def qp_reset(fn=[]):
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

def qp_updaterange(xx, yy):
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
class QFigure:
    fd = None
    fn = None
    istmp = False
    extent = [0,0,1,1]

def qfigure(fn=None, w=5, h=None):
    '''
QFIGURE - Open a QPlot figure
   QFIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
   in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
   W defaults to 5 inches.
   fn = QFIGURE([], w, h) opens a new QPlot figure of given size (in inches)
   with a temporary filename.
'''
    if isempty(h):
        h = .75 * w
    MAXALLOWED = 36
    if w>MAXALLOWED or h>MAXALLOWED:
        error('Unreasonable size passed to qfigure. Units are inches!')

    if fn in qdata.figs:
        qdata.curfn = fn
        return fn

    qfig = QFigure
    if isempty(fn):
        (qfig.fd, qfig.fn) = tempfile.mkstemp(suffix='.qpt')
        qfig.istmp = True
    else:
        if not fn.endswith('.qpt'):
            fn = fn + '.qpt'
        qfig.fn = fn
        qfig.fd = open(fn, 'wb')
        qfig.istmp = False

    w *= 72
    h *= 72
    qfig.extent = [0, 0, w, h]
    qdata.figs[fn] = qfig
    qdata.curfn = fn
    qp_write('figsize %g %g\n' % (w,h))
    qp_reset()
    qp_unix('qpclient %s' % fn)
    qp_flush()

def qp_ensure():
    # Now returns curfn as index into figs
    if isempty(qdata.curfn):
        qfigure()
    return qdata.curfn

def qp_schmitt(xx):
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

def qp_mapcolor(s):
    if s=='r':
        return 'red'
    elif s=='g':
        return 'green'
    elif s=='b':
        return 'blue'
    elif s== 'm':
        return 'magenta'
    elif s== 'y':
        return 'yellow'
    elif s== 'c':
        return 'cyan'
    elif s== 'k':
        return 'black'
    elif s== 'w':
        return 'white'
    else:
        return None

def qp_plot(xx, yy, cmd='plot'):
    '''
QPLOT - Draw a line series in data space
   QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
   coordinates. See also QLINE and QGLINE.
'''
    qp_ensure()

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
    
    [iup, idn] = qp_schmitt(np.isnan(xx+yy)==False)
    
    for k in range(len(iup)):
        N = idn[k] - iup[k]
        qp_write('%s *%i *%i\n' % (cmd, N, N))
        qp_writedbl(xx[iup[k]:idn[k]])
        qp_writedbl(yy[iup[k]:idn[k]])
    qp_flush()
    
    qp_updaterange(xx, yy)
    
def qplot(xx, yy=None):
    '''
QPLOT - Draw a line series in data space
   QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
   coordinates. See also QLINE and QGLINE.
'''
    if yy is None:
        yy = xx
        xx = range(len(yy))
    qp_plot(xx, yy, 'plot')

def qarea(xx, yy):
    '''
QAREA - Draw a polygon in paper space
   QAREA(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
   is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
   The polygon is filled with the current brush.
   XX and YY are given in postscript points. See also QPATCH and QGAREA.
'''
    qp_plot(xx, yy, 'area')

def qpatch(xx, yy):
    '''
QPATCH - Draw a polygonal patch in data space
   QPATCH(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
   is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
   The polygon is filled with the current brush.
   XX and YY are given in data coordinates. See also QAREA and QGAREA.
'''
    qp_plot(xx, yy, 'patch')
    
def qarrow(l=8, w=None, dl=0, dimple=0, dw=0):
    '''
QARROW - Draw an arrowhead
  QARROW draws an arrow head pointing to the current anchor set by QAT.
  QARROW(l, w) specifies length and (full) width of the arrow head
  These are specified in points, and default to L=8, W=5.
  QARROW(l, w, dl) specifies that the arrow is to be displaced from the
  anchor by a distance DL along the arrow's axis.
  QARROW(l, w, dl, dimple) specifies that the back of the arrow head is
  indented by DIMPLE points.
  QARROW(l, w, dl, dimple, dw) specifies that the arrow is to be displaced
  from the anchor by DW points in the orthogonal direction of the arrow's
  axis.
'''
    if w is None:
        w = .6 * l
    qarea(np.array([0, -l, dimple-l, -l]) - dl,
          np.array([0, w, 0, -w])/2+dw)
    
class CBarInfo:
    clim = [0, 1]
    orient = 'x'
    xywh_d = [0,0,1,1]
    rev = False

class AxisInfo:
    orient='x'
    lim_d=None
    tick_d=None
    tick_p=None
    tick_lbl=None
    ttl=''
    ticklen=3
    lbldist=3
    ttldist=3
    coord_d=None
    coord_p=0
    ttlrot=0
    cbar=None

def qxlim(x0=None, x1=None):
    '''
QXLIM - Set x-axis limits
  QXLIM(x0, x1) sets x-axis limits in the current panel.
'''
    if x0 is None:
        error('Usage: qxlim x0 x1')    
    if x1 is None:
        x1 = x0[1]
        x0 = x0[0]

    qp_write('xlim %g %g\n' % (x0, x1))
    qp_flush()

def qylim(y0=None, y1=None):
    '''
QYLIM - Set y-axis limits
  QYLIM(y0, y1) sets y-axis limits in the current panel.
'''
    if y0 is None:
        error('Usage: qylim y0 y1')    
    if y1 is None:
        y1 = y0[1]
        y0 = y0[0]

    qp_write('ylim %g %g\n' % (y0, y1))
    qp_flush()

def qat(*args):
    '''
QAT - Specify location for future text
   QAT(x, y) specifies that future text will be placed at data location (x,y)
   QAT(x, y, phi) specifies that the text will be rotated by phi radians
   QAT(x, y, dx, dy) specifies that the text will be rotated s.t. the baseline
   points in the data direction (dx,dy).
   QAT(id, x, y) specifies coordinates in a specific subplots
   QAT(id, x, y, phi) specifies coordinates in a specific subplots
   QAT without arguments reverts to absolute placement relative to topleft.
   Either X or Y may also be nan (or '-') to have absolute placement in
   one dimension
'''
    nargin = len(args)
    qp_ensure()
    if nargin==0:
        qp_write('at -\n')
    
    if nargin<1 or nargin>4:
        error('Cannot interpret arguments to QAT')
    
    s = 'at'
    atcoord = np.zeros((nargin,)) + np.nan
    if type(args[0])==str and args[0]>='A' and args[0]<='Z':
        s += ' ' + args[0]
        if nargin>3:
            error('Cannot interpret QAT arguments following ID')
        for k in range(1,nargin):
            a = args[k]
            if isnscalar(a):
                s += ' %g' % a
            else:
                error('Cannot interpret arguments following ID')
    else:
        if nargin<2:
            error('Cannot interpret arguments to QAT')
        # at x y [dx dy]|[angle]|[ID]
        xtype = 'left right center abs absolute'.split()
        ytype = 'top bottom middle abs absolute'.split()
        for k in range(nargin):
            a = args[k]
            if nargin==3 and k==2 and type(a)==str and len(a)==1:
                s += ' ' + a
            elif isnscalar(a):
                s += ' %g' % a
                atcoord[k] = a
            elif k==0 and type(a)==str and a in xtype:
                s += ' ' + a
            elif k==1 and type(a)==str and a in type:
                s += ' ' + a
            elif k<2 and ((type(a)==str and a=='-')
                          or isnscalar(a) and np.isnan(a)):
                s += ' -'
            else:
                error('Cannot interpret arguments')
    qp_write(s)
    qdata.figs[qdata.curfn].atcoord = atcoord

def qaxshift(pt=None):
    '''
QAXSHIFT - Specifies shift of drawn axis for QXAXIS and QYAXIS
   QAXSHIFT(len) specifies shift (in points) for QXAXIS and
   QYAXIS. Positive means down or left, negative means up or right.
   pt = QAXSHIFT returns current setting.
'''
    fn = qp_ensure()
    if isempty(pt):
        pt = qdata.figs[fn].axshift
    elif isnscalar(pt):
        qdata.figs[fn].axshift = pt
    else:
        error('QAXSHIFT needs real number')
    return pt
    
def qalign(*args):
    '''
QALIGN - Set alignment for following text
  QALIGN left|right|center|top|bottom|middle|base sets alignment for
  subsequent QTEXT commands.
'''
    allowed = 'left right center top bottom middle base'.split()
    usage = 'Usage: qalign ' + str.join('|', allowed) + ' ...'
    if isempty(args):
        error(usage)
    
    txt = 'align'
    for a in args:
        if a in allowed:
            txt += ' ' + a
        else:
            error(usage)

    qp_write(txt + '\n')
    qp_flush()

def qbars(xx, yy, w, y0=0):
    '''
QBARS - Bar plot with bar width specified in data coordinates
   QBARS(xx, yy, w) draws a bar graph of YY vs XX with bars
   of width W specified in data coordinates.
   QBARS(xx, yy, w, y0) specifies the baseline of the plot;
   default for Y0 is 0. Y0 may also be a vector (which must
   then be the same size as XX and YY). This is useful for
   creating stacked bar graphs.
'''

    if isnscalar(y0):
        y0=np.zeros(yy.shape) + y0
    
    for k in range(xx.size):
        qpatch(np.array([-.5, .5, .5, -.5])*w + xx[k],
               np.array([0, 0, 1, 1])*yy[k] + y0[k])

def qbrush(*args):
    '''
QBRUSH - Set brush for QPlot
   QBRUSH id | color | 'none' | opacity  chooses or changes a brush for
   QPlot. ID must be a single capital letter. COLOR may be a named color
   (i.e., one of krgbcmyw), or a 3-digit or a 6-digit string. 
   OPACITY must be a number between 0 and 1.
'''
    first = True
    out = ['brush']
    for a in args:
        if type(a)==str:
            if len(a)==1 and a>='A' and a<='Z' and first:
                out.append(a) # This is ID, so good
            elif a=='none':
                out.append(a) # This is a known keyword, so good
            elif not isempty(qp_mapcolor(a)):
                # This is a good color
                out.append(qp_mapcolor(a))
            elif qp_allnumeric(a):
                # This is a number
                if len(a)==3:
                    out.append('#%02x%02x%02x' % 
    	                       (int(255.999*int(a[0])/9),
    	                        int(255.999*int(a[1])/9), 
    	                        int(255.999*int(a[2])/9)))
                elif len(a)==6:
                    out.append('#%02x%02x%02x' % 
    	                       (int(255.999*int(a[0:2])/99), 
    	                        int(255.999*int(a[2:4])/99), 
    	                        int(255.999*int(a[4:6])/99)))
                else:
                    error('Cannot interpret argument for qbrush')
            else:
                error('Cannot interpret argument for qbrush')
        elif isnscalar(a):
            # This is opacity
            out.append('%g' % a)
        elif isnvector(a) and len(a)==3:
            out.append('##02x#02x#02x' %
    	               (int(255.999*a[0]),
    	                int(255.999*a[1]),
    	                int(255.999*a[2])))
        else:
            error('Cannot interpret argument for qbrush')
        first = False
    qp_write(str.join(' ', out) + '\n')

def qpen(*args):
    '''
QPEN - Selects a new pen for QPlot
   QPEN id | join | cap | pattern | color | width | -alpha | 'none'
   selects a new pen.
   ID must be a single capital letter
   JOIN must be one of: miterjoin beveljoin roundjoin
   CAP must be one of: flatcap squarecap roundcap
   PATTERN must be one of: solid dash dot none
      dash may optionally be followed by a vector of stroke and space lengths
      dot may optionally be followed by a vector of space lengths
   COLOR may be a single character matlab color, or a 3- or 6-digit RGB
   specification. 
   WIDTH is linewidth in points, or 0 for hairline.
   ALPHA specifies transparency between 0 and 1.
'''
    out = [ 'pen' ]
    first = True
    for a in args:
        if type(a)==str:
            if len(a)==1 and a>='A' and a<='Z' and First:
                out.append(a)
            elif a in 'miterjoin beveljoin roundjoin flatcap squarecap roundcap solid none'.split()
                cmd = [ cmd ' ' a ]
            elif strmatch(a, strtoks('dash dot'), 'exact')
                cmd = [ cmd ' ' a ]
                vec=[]
                while n<nargin:
    	if isnvector(varargin{n+1}):
    	    vec = [ vec; varargin{n+1}(:); ]
    	elif ischar(varargin{n+1}) && ~isnan(str2double(varargin{n+1}))
    	    vec = [ vec; str2double(varargin{n+1}) ]
    	else:
    	    break
    	n=n+1
                if isempty(vec):
    	vec = 3
                cmd = [ cmd ' [' sprintf(' #g', vec) ' ]']
            elif ~isempty(qp_mapcolor(a))
                ; # This is a good color
                cmd = [ cmd ' ' qp_mapcolor(a) ]
            elif ~isnan(str2double(a))
                # This is a number
                if length(a)==3    && all(a>='0') && all(a<='9'):
    	# This is a three-digit color
    	cmd = [ cmd ' ' sprintf('##02x#02x#02x', ...
    	        floor(255.999*atoi(a(1))/9), ...
    	        floor(255.999*atoi(a(2))/9), ...
    	        floor(255.999*atoi(a(3))/9))]
                elif length(a)==6 && all(a>='0') && all(a<='9')
    	# This is a six-digit color
    	cmd = [ cmd ' ' sprintf('##02x#02x#02x', ...
    	        floor(255.999*atoi(a(1:2))/99), ...
    	        floor(255.999*atoi(a(3:4))/99), ...
    	        floor(255.999*atoi(a(5:6))/99))]
                else:
    	; # This is pen width
    	cmd = [ cmd ' ' a ]
            else:
                error([ 'Cannot interpret ' a ' as an argument for qpen' ])
        elif isnscalar(a) && isreal(a)
            ; # This is a pen width
            cmd = [ cmd ' ' sprintf('#g', a)]
        elif isnvector(a) && isreal(a) && length(a)==3
            # This is a color
            cmd = [ cmd ' ' sprintf('##02x#02x#02x', ...
    	    floor(255.999*a))]
        else:
            error([ 'Cannot interpret ' disp(a) ' as an argument for qpen' ])
        n=n+1
    
    fprintf(fd, '#s\n', cmd)

def qytitlerot(pt=None):
    '''
QYTITLEROT - Specifies the rotation of y-axis titles.
   QYTITLEROT(phi) specifies the rotation of y-axis titles, in degrees:
   phi=0 means upright,
   phi>0 means rotated 90 degrees to the left,
   phi<0 means rotated 90 degrees to the right.
'''
    fn = qp_ensure()
    if pt is None:
        pt = qdata.figs[fn].ytitlerot
    else:
        if not isnscalar(pt):
            error('ytitlerot must be a real scalar')
    
    qdata.figs[fn].ytitlerot = np.sign(pt)*np.pi/2
    
def qtitle(ttl):
    '''
QTITLE - Render a title on the current QPlot
   QTITLE(text) renders the given text centered along the top of the
   current QPlot figure.
   For more control over placement, use QTEXT and friends.
'''
    qat()
    pid = qdata.figs[qdata.curfn].panel
    if pid=='-':
        xywh = qdata.figs[qdata.curfn].extent
    else:
        xywh = qdata.figs[qdata.curfn].panelextent[pid]
    
    qalign top center
    qtext(xywh(1) + xywh(3)/2, xywh(2) + 5, ttl)

def qticklen(pt=None):
    '''
QTICKLEN - Specifies length of ticks for QXAXIS and QYAXIS
   QTICKLEN(len) specifies length of ticks (in points) for QXAXIS and
   QYAXIS. Positive means down or left, negative means up or right.
   pt = QTICKLEN returns current setting.
'''
    fn = qp_ensure()
    if pt is None:
        pt = qdata.figs[fn].ticklen
    else:
        if not isnscalar(pt):
            error('ticklen must be a real scalar')
        qdata.figs[fn].ticklen = pt
    return pt
    
#======================================================================
if __name__ == '__main__':
    print('qplot test')
    qfigure('hello', 4, 3)
    qplot([1,2,3,4], [1,3,2,4])
    
    qbrush('555')
    qpatch([1,2,1,1],[1,1,2,1])
