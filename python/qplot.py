import numpy as np
import tempfile
import os
import re
import qplot_internal as qi

def plot(xx, yy=None):
    '''PLOT - Draw a line series in data space
    PLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
    coordinates.
    PLOT(yy) plots the data against x = 1..N.
    See also LINE and GLINE.'''
    if yy is None:
        yy = xx
        xx = range(len(yy))
    qi.plot(xx, yy, cmd='plot')

def area(xx, yy):
    '''AREA - Draw a polygon in paper space
    AREA(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
    The polygon is filled with the current brush.
    XX and YY are given in postscript points. See also PATCH and GAREA.'''
    qi.plot(xx, yy, cmd='area')

def patch(xx, yy):
    '''PATCH - Draw a polygonal patch in data space
    PATCH(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
    The polygon is filled with the current brush.
    XX and YY are given in data coordinates. See also AREA and GAREA.'''
    qi.plot(xx, yy, cmd='patch')
    
def arrow(l=8, w=None, dl=0, dimple=0, dw=0):
    '''ARROW - Draw an arrowhead
    ARROW draws an arrow head pointing to the current anchor set by AT.
    ARROW(l, w) specifies length and (full) width of the arrow head
    These are specified in points, and default to L=8, W=5.
    Optional arguments:
      DL - specifies that the arrow is to be displaced from the
           anchor by a distance DL along the arrow's axis.
      DIMPLE - specifies that the back of the arrow head is
           indented by DIMPLE points.
      DW - specifies that the arrow is to be displaced from the anchor 
           by DW points in the orthogonal direction of the arrow's
           axis.'''
    if w is None:
        w = .6 * l
    area(np.array([0, -l, dimple-l, -l]) - dl,
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

def xlim(x0=None, x1=None):
    '''XLIM - Set x-axis limits
    XLIM(x0, x1) or XLIM([x0, x1]) sets x-axis limits in the current panel.'''
    if x0 is None:
        qi.error('Usage: xlim x0 x1')    
    if x1 is None:
        x1 = x0[1]
        x0 = x0[0]

    qi.write('xlim %g %g\n' % (x0, x1))
    qi.flush()

def ylim(y0=None, y1=None):
    '''YLIM - Set y-axis limits
    YLIM(y0, y1) or YLIM([y0, y1]) sets y-axis limits in the current panel.'''
    if y0 is None:
        qi.error('Usage: ylim y0 y1')    
    if y1 is None:
        y1 = y0[1]
        y0 = y0[0]

    qi.write('ylim %g %g\n' % (y0, y1))
    qi.flush()

def at(x=None, y=None, phi=None, along=None, id=None):
    '''AT - Specify location for future text
    AT(x, y) specifies that future text will be placed at data location (x,y)
    Optional arguments:
      PHI - specifies that the text will be rotated by phi radians.
      ALONG - must be a tuple (dx,dy), meaning that the text will be
            rotated s.t. the baseline points in the data direction (dx,dy).
      ID - coordinates are specified relative to a subplot
    X may also be one of 'left,' 'right,' 'center,' 'abs,' 'absolute.'
    Y may also be one of 'top,' 'bottom,' 'middle,' 'abs,' 'absolute.'
    If X and/or Y is omitted, placements reverts to absolute in those
    dimensions.
    '''
    qi.ensure()
    qi.curfig.atx = None
    qi.curfig.aty = None
    if x is None and y is None:
        qi.write('at -\n')
        return
    cmd = ['at']
    if id is not None:
        cmd.append(id)
    if type(x)==str:
        if x in at.xtype:
            cmd.append(x)
        else:
            qi.error('Bad specification for x')
    else:
        cmd.append('%g' % x)
        qi.curfig.atx = x
    if type(y)==str:
        if y in at.ytype:
            cmd.append(y)
        else:
            qi.error('Bad specification for y')
    else:
        cmd.append('%g' % y)
        qi.curfig.aty = y
    if phi is not None:
        cmd.append('%g' % phi)
    elif along is not None:
        cmd.append('%g %g' % (along[0], along[1]))
    qi.write(' '.join(cmd))
    
at.xtype = qi.wordset('left right center abs absolute')
at.ytype = qi.wordset('top bottom middle abs absolute')

def axshift(pt=None):
    '''AXSHIFT - Specifies shift of drawn axis for XAXIS and YAXIS
   AXSHIFT(len) specifies shift (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = AXSHIFT returns current setting.'''
    qi.ensure()
    if qi.isempty(pt):
        pt = qi.curfig.axshift
    elif isnscalar(pt):
        qi.curfig.axshift = pt
    else:
        qi.error('AXSHIFT needs real number')
    return pt
    
def align(*args):
    '''ALIGN - Set alignment for following text
  ALIGN left|right|center|top|bottom|middle|base sets alignment for
  subsequent TEXT commands.'''
    allowed = 'left right center top bottom middle base'.split()
    usage = 'Usage: align ' + str.join('|', allowed) + ' ...'
    if qi.isempty(args):
        qi.error(usage)
    
    txt = 'align'
    for a in args:
        if a in allowed:
            txt += ' ' + a
        else:
            qi.error(usage)

    qi.write(txt + '\n')
    qi.flush()

def bars(xx, yy, w, y0=0):
    '''BARS - Bar plot with bar width specified in data coordinates
   BARS(xx, yy, w) draws a bar graph of YY vs XX with bars
   of width W specified in data coordinates.
   BARS(xx, yy, w, y0) specifies the baseline of the plot;
   default for Y0 is 0. Y0 may also be a vector (which must
   then be the same size as XX and YY). This is useful for
   creating stacked bar graphs.'''

    if isnscalar(y0):
        y0=np.zeros(yy.shape) + y0
    
    for k in range(xx.size):
        patch(np.array([-.5, .5, .5, -.5])*w + xx[k],
               np.array([0, 0, 1, 1])*yy[k] + y0[k])

def brush(color=None, alpha=None, id=None):
    '''BRUSH - Set brush for QPlot
    All arguments are optional.
      COLOR may be a named color (i.e., one of krgbcmyw), or a 3-digit or
        a 6-digit string, or 'none' or '' for none.
      ALPHA must be a number between 0 and 1.
      ID specifies an ID.'''
    first = True
    out = ['brush']
    if id is not None:
        out.append(id)
    color = qi.interpretcolor(color)
    if color is not None:
        out.append(color)
    if alpha is not None:
        out.append('%g' % alpha)
    qi.write(str.join(' ', out) + '\n')

def pen(color=None, width=None, join=None, cap=None, pattern=None, \
        alpha=None, id=None):
    '''PEN - Selects a new pen for QPlot
    All arguments are optional.
      COLOR may be a single character matlab color, or a 3- or 6-digit RGB
      specification or an [r, g, b] triplet, or 'none'. 
      WIDTH is linewidth in points, or 0 for hairline.
      JOIN must be one of: 'miterjoin', 'beveljoin', 'roundjoin'.
      CAP must be one of: 'flatcap', 'squarecap', 'roundcap'.
      PATTERN must be one of: 'solid', 'dash', 'dot', 'none'.
      PATTERN may also be a tuple ('dash', vec) where VEC is a vector of 
        stroke and space lengths, or it may be a tuple ('dot', vec) where
        VEC is a vector of space lengths.
      ALPHA specifies transparency between 0 and 1.
      ID must be a single capital letter'''
    out = [ 'pen' ]
    if id is not None:
        out.append(id)
    color = qi.interpretcolor(color)
    if color is not None:
        out.append(color)
    if alpha is not None:
        out.append('%g' % -alpha)
    if width is not None:
        out.append('%g' % width)
    if join is not None:
        if join in pens.joins:
            out.append(join)
        else:
            qi.error('Join type not understood')
    if cap is not None:
        if cap in pens.caps:
            out.append(cap)
        else:
            qi.error('Cap type not understood')
    if pattern is not None:
        if type(pattern)==tuple and (pattern[0]=='dash' or pattern[0]=='dot'):
            out.append(pattern[0])
            out.append('[')
            for a in pattern[1]:
                out.append('%g' % a)
            out.append(']')
        elif pattern in pens.patterns:
            out.append(pattern)
        else:
            qi.error('Pattern type not understood')
    qi.write(' '.join(out))
pen.joins = qi.wordset('miterjoin beveljoin roundjoin')
pen.caps = qi.wordset('flatcap squarecap roundcap')
pen.patterns = qi.wordset('solid none dash dot')

def ytitlerot(pt=None):
    '''YTITLEROT - Specifies the rotation of y-axis titles.
   YTITLEROT(phi) specifies the rotation of y-axis titles, in degrees:
   phi=0 means upright,
   phi>0 means rotated 90 degrees to the left,
   phi<0 means rotated 90 degrees to the right.'''
    qi.ensure()
    if pt is None:
        pt = qi.curfig.ytitlerot
    else:
        if not isnscalar(pt):
            qi.error('ytitlerot must be a real scalar')
    
    qi.curfig.ytitlerot = np.sign(pt)*np.pi/2
    
def title(ttl):
    '''TITLE - Render a title on the current QPlot
   TITLE(text) renders the given text centered along the top of the
   current QPlot figure.
   For more control over placement, use TEXT and friends.'''
    at()
    pid = qi.curfig.panel
    if pid=='-':
        xywh = qi.curfig.extent
    else:
        xywh = qi.curfig.panelextent[pid]
    align('top', 'center')
    text(xywh(1) + xywh(3)/2, xywh(2) + 5, ttl)

def textdist(lbl=None, ttl=None):
    '''TEXTDIST - Specifies distance to text labels for XAXIS and YAXIS
    QTEXTDIST(lbldist, ttldist) specifies distance between ticks and
    tick labels and between tick labels and axis title, in points.
    QTEXTDIST(dist) uses DIST for both distances.
    Positive numbers are to the left and down; negative numbers are to the
    right and up.
    (lbl, ttl) = TEXTDIST returns current settings.'''

    qi.ensure()
    
    if lbl is None:
        lbl = qi.curfig.textdist[0]
        ttl = qi.curfig.textdist[1]
    elif ttl is None:
        ttl = lbl
    qi.curfig.textdist = (lbl, ttl)
    return (lbl, ttl)
    
def ticklen(pt=None):
    '''TICKLEN - Specifies length of ticks for XAXIS and YAXIS
   TICKLEN(len) specifies length of ticks (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = TICKLEN returns current setting.'''
    qi.ensure()
    if pt is None:
        pt = qi.curfig.ticklen
    else:
        if not isnscalar(pt):
            qi.error('ticklen must be a real scalar')
        qi.curfig.ticklen = pt
    return pt

def figure(fn=None, w=5, h=None):
    '''FIGURE - Open a QPlot figure
    FIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
    in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
    W defaults to 5 inches.
    fn = FIGURE('', w, h) opens a new QPlot figure of given size (in inches)
    with a temporary filename.'''
    if h is None:
        h = .75 * w
    MAXALLOWED = 36
    if w>MAXALLOWED or h>MAXALLOWED:
        qi.error('Unreasonable size passed to qfigure. Units are inches!')

    if fn in qi.figs:
        qi.curfig = qi.figs[fn]
        return fn

    fig = qi.Figure()
    if qi.isempty(fn):
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
    qi.figs[fn] = fig
    qi.curfig = fig
    qi.write('figsize %g %g\n' % (w,h))
    qi.unix('qpclient %s' % fn)
    fig.flush()

def xaxis(y0=None, lim=None, ticks=None, labels=None, title='', flip=False):
    '''XAXIS - Draw x-axis
    All arguments are optional.
      Y0 specifies intersect with y-axis.
      LIM specifies left and right edges as a tuple or list. If None,
        LIM is determined from TICKS. If [], no line is drawn.
      TICKS specifies positions of ticks along axis.
      LABELS specifies labels to put by ticks. If None, tick coordinates
        are used. If [], no labels are drawn.
      TITLE specifies title for axis.
      FLIP, if True, specifies that labels and ticks go in opposite direction.'''
    if y0 is None:
        yy = qi.sensibleticks(qi.curfig.datarange[2:4], 1)
        y0 = yy[0]
    if ticks is None:
        ticks = qi.sensibleticks(qi.curfig.datarange[0:2], inc=True)
    if lim is None:
        lim = [ticks[0], ticks[-1]]
    if labels is None:
        labels = qi.format(ticks) 
    ticklen = ticklen()
    axshift = axshift()
    [lbldist, ttldist] = textdist()
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
    
    qi.axis(orient='x', lim_d=lim, tick_d=ticks, tick_lbl=labels, ttl=title, \
            ticklen=ticklen, lbldist=lbldist, ttldist=ttldist, \
            coord_d=y0, coord_p=axshift)

#======================================================================
if __name__ == '__main__':
    print('qplot test')
    figure('hello', 4, 3)
    pen('r')
    plot([1,2,3,4], [1,3,2,4])
    
    brush('555')
    patch([1,2,1,1],[1,1,2,1])
