# Everything in the Paper coordinate plotting and Mixed coordinate plotting
# QGIMAGE is in img

# area
# line
# mm
# pmark
# garea
# garea2
# gline
# gline2
# shiftedline

from . import qi
from . import utils
import numpy as np
# A GLC is a tuple (cmd, arg) or (cmd, arg, arg2).
# A PTSPEC is a list of GLCS.
def _gline(cmd='gline', ptspecs=[]):
    out = [cmd]
    if type(ptspecs) != list:
        raise Exception(f"{cmd} takes a list of ptspecs, not {type(ptspecs)}")
        
    for pt in ptspecs:
        if type(pt) != list:
            raise Exception(f"{cmd} takes a list of ptspecs, which are lists of commands not {type(pt)}")
        out.append('(')
        for glc in pt:
            if type(glc) != tuple or len(glc)<2 or len(glc)>3:
                raise Exception(f"Commands in ptspec must be made with the AbsData etc. constructors")
            out.append(glc[0])
            if type(glc[1])==str:
                out.append(glc[1])
            else:
                out.append('%g' % glc[1])
            if len(glc)>=3:
                out.append('%g' % glc[2])
        out.append(')')
    qi.ensure()
    qi.f.write(out)

# A VGLC is a GLC where each arg may be a vector
def _gline2(cmd='gline', vglcs=[]):
    N = None
    for vgl in vglcs:
        a1 = utils.aslist(vgl[1])
        n = len(a1)
        if N is None or n>N:
            N = n
        elif n>1 and n!=N:
            error('Mismatching point count')
    if N is None:
        return
    pts = []
    for n in range(N):
        pts.append([])
    for vgl in vglcs:
        a1 = utils.aslist(vgl[1])
        L = len(a1)
        K = len(vgl)
        if K>=3:
            a2 = utils.aslist(vgl[2])
            L1 = len(a2)
            if L1==1:
                a2 = 0*a1 + a2
            elif L==1:
                a1 = 0*a2 + a1
                L = L1
        if L==1:
            a1 = a1[0]
            if K==2:
                for n in range(N):
                    pts[n].append((vgl[0], a1))
            else:
                a2 = a2[0]
                for n in range(N):
                    pts[n].append((vgl[0], a1, a2))
        else:
            if K==2:
                for n in range(N):
                    pts[n].append((vgl[0], a1[n]))
            else:
                for n in range(N):
                    pts[n].append((vgl[0], a1[n], a2[n]))
    _gline(cmd, pts)

def line(xx, yy):
    '''LINE - Draw a line series in paper space
    LINE(xx, yy) draws a line series between the points (XX,YY).
    XX and YY are given in postscript points. 

    See also PLOT and GLINE.'''
    qi.plot(xx, yy, cmd='line')

def area(xx, yy):
    '''AREA - Draw a polygon in paper space
    AREA(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
    is automatically closed (i.e., it is not necessary for xx[-1] to equal
    xx[0]).
    The polygon is filled with the current brush.
    XX and YY are given in postscript points. 

    See also PATCH and GAREA.'''
    qi.plot(xx, yy, cmd='area')


def phatch(xx, yy, pattern="|", angle=0, spacing=10, offset=0):
    '''PHATCH - Hatch a polygonal patch in paper space
    PATCH(xx, yy, angle) hatches a polygon with vertices at (XX,YY) using
    the given pattern. PATTERN is a single character from the following:
      | / - \  : lines at the angle suggested angle
      + x      : combination of either orthogonal or diagonal lines
      : *      : marks in an orthogonal or hexagonal pattern.
    Lines are rendered with the current PEN.
    Marks are rendereded as by MARK, i.e., with the current MARKER (and PEN
    and BRUSH).
    Instead of a pattern, a numeric ANGLE may be specified, clockwise from
    vertical (in radians, but see DEGREES).
    Optional argument SPACING specifies space between lines, in points.
    By default, the line pattern is aligned with the center of the polygon.
    OFFSET shifts this center by the given number of points.
    NaN values in XX or YY may be used to separate multiple polygons to be
    drawn with common line pattern alignment.
    See also HATCH.'''
    qi.hatch(xx, yy, pattern, angle, spacing, offset, cmd="phatch")
        

def pmark(xx, yy):
    '''PMARK - Draw on the current graph with the current marker
    PMARK(xx, yy) draws marks at the given location in paper space. 

    See also MARKER and MARK.'''

    xx = utils.aslist(xx)
    yy = utils.aslist(yy)
    if len(xx) != len(yy):
        error('xx and yy must be equally long')
    qi.ensure()
    qi.f.write('pmark *%i *%i\n' % (len(xx), len(yy)))
    qi.f.writedbl(xx)
    qi.f.writedbl(yy)

def AbsData(x, y):
    qi.ensure()
    x = qi.f.xtransform(x)
    y = qi.f.ytransform(y)
    
    return ('absdata', x, y)

def RelData(x, y):
    return ('reldata', x, y)

def AbsPaper(x, y):
    return ('abspaper', x, y)

def RelPaper(x, y):
    return ('relpaper', x, y)

def RotData(xi, eta):
    return ('rotdata', xi, eta)

def RotPaper(phi):
    return ('rotpaper', phi)

def Retract(l1, l2=None):
    if l2 is None:
        l2 = l1
    return ('retract', l1, l2)

def At(id):
    return ('at', id)

def AtX(id):
    return ('atx', id)

def AtY(id):
    return ('aty', id)

def gline(ptspecs):
    '''GLINE - Generalized line drawing
    GLINE([ptspec1, ptspec2, ...]).
    A PTSPEC is a list containing commands from the following list:

     AbsData(x, y)    - Absolute data coordinates. (This respects the
                        transformation set by XTRANSFORM and YTRANSFORM.)
     RelData(dx, dy)  - Relative data coordinates. (This does not respect
                        those transformations.)
     AbsPaper(x, y)   - Absolute paper coordinates (in pt)
     RelPaper(dx, dy) - Relative data coordinates (in pt)
     RotData(xi, eta) - Rotate by atan2(eta, xi) in data space.
                        (This affects subsequent relative positioning.) 
     RotPaper(phi)    - Rotate by phi radians. (This affects subsequent 
                        relative positioning.) 
     Retract(l)       - Retract preceding and following segments by L pt.
     Retract(l1, l2)  - Retract preceding and following segments by L1 and 
                        L2 pt respectively.
     At(id)           - Absolute paper coordinates of location set by AT.
     AtX(id)          - Absolute paper x-coordinate of location set by AT.
     AtY(id)          - Absolute paper y-coordinate of location set by AT.

    For instance,

      gline([[AbsData(0, 1), RelPaper(5,0)],
             [AbsData(2, 3), RelPaper(0, 7)]])

    draws a line from 5 pt to the right of the point (0, 1) in the graph to
    7 pt below the point (2, 3) in the graph. (Note that paper y-coordinates
    increase toward the bottom of the graph while data y-coordinates increase
    toward the top.)
    
    Note: The rather cumbersome syntax of GLINE makes LINE and PLOT more
    attractive for general usage. The same applies to GAREA versus AREA 
    and PATCH. 
    
    See also SHIFTEDLINE and GLINE2.'''
    _gline('gline', ptspecs)

def gline2(vglcs):
    '''GLINE2 - Generalized line drawing
    QGLINE([cmd1, cmd2, ...]) specifies a line in mixed data and paper 
    coordinates. Commands are as in GLINE, but in this case their arguments
    are vectors. GLINE2 does not support the AT, ATX, and ATY commands.

    For instance,

       gline2([AbsData([0, 2], [1, 3]), RelPaper([5, 0], [0, 7])])

    Draws a line from 5 pt to the right of the point (0, 1) in the graph
    to 7 pt below the point (2, 3) in the graph. (Note that paper 
    y-coordinates increase toward the bottom of the graph while data
    y-coordinates increase toward the top.)'''
    _gline2('gline', vglcs)

def garea(ptspecs):
    '''GAREA - Generalized area drawing
    GAREA is to PATCH and AREA as GLINE is to PLOT and LINE.
    
    See GLINE for supported commands.'''

    _gline('garea', ptspecs)

def garea2(vglcs):
    '''GAREA2 - Generalized area drawing
    GAREA2 is to PATCH and AREA as GLINE2 is to PLOT and LINE.
    
    See GLINE2 for supported commands.'''
    _gline2('garea', vglcs)
    
def mm(x=1):
    '''MM - Convert millimeters to postscript points
    MM(x) converts a length specified in millimeters to postscript points.
    MM() returns the number of postscript points in a millimeter.'''
    return 72 * x / 25.4

def shiftedline(xx, yy, dx, dy):
    '''SHIFTEDLINE - Renders a line displaced from data points
    SHIFTEDLINE(xx, yy, dx, dy) is like PLOT(xx, yy) except that the 
    plot is displaced by (DX, DY) points on the graph.
    XX, YY, DX, DY may be vectors or scalars. Any scalars are automatically
    converted to vectors of the appropriate length. All vectors must be
    the same length.
    See also GLINE and GLINE2.'''
    gline2([AbsData(xx, yy), RelPaper(dx, dy)])
