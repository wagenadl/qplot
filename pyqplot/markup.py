# -*- coding: utf-8 -*-
# Everything in the Annotations category and also QALIGN and QREFTEXT.
# Also the Legends category.

# align
# arrow
# at
# darrow
# legend
# legopt
# mlegend
# plegend
# reftext
# text
# title
# ctext
# textonpath

from . import utils
from . import qi
from . import paper
from . import fig
from . import style
import numpy as np

def align(*args):
    '''ALIGN - Set text alignment
    ALIGN('left|right|center') specifies horizontal text alignement.
    ALIGN('top|bottom|middle|base') specifies vertical text alignment.
    Horizontal and vertical alignment may be combined in one command.'''
    out = ['align']
    for a in args:
        if a in align.words:
            out.append(a)
        else:
            qi.error('Bad argument for align')
    qi.ensure()
    qi.f.write(out)
align.words = utils.wordset('left right center top bottom middle base')

def q__safetext(s):
    s = s.replace('"', '”')
    s = s.replace('\\', '\\\\')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    # Anything else?
    return s

def reftext(s):
    qi.ensure()
    qi.f.write('reftext "%s"\n' % q__safetext(s))
    
def text(s, dx=0, dy=0):
    '''TEXT - Render text 
    TEXT(text) renders text at the current anchor point.
    TEXT(text, dx, dy) renders text displaced by the given number of points.'''
    qi.ensure()
    qi.f.write('text %g %g "%s"\n' % (dx, dy, s))
    
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
           axis.
    For most use cases, DARROW is easier.'''
    if w is None:
        w = .6 * l
    paper.area(np.array([0, -l, dimple-l, -l]) - dl,
               np.array([0, w, 0, -w])/2+dw)

def darrow(x, y, phi=None, along=None, l=8, w=5, dist=0, dimple=0):
    '''DARROW - Draw an arrowhead
    DARROW(x, y) draws an arrow head pointing to (X,Y).
    Optional arguments are:
      PHI - Arrow points in the given direction specified in radians
           in paper space (0: pointing right, pi/2: pointing down, etc)
      ALONG - Arrow points in the given direction specified as a (DX,DY)
           vector in data space
      L - Length of the arrow in points (default: 8 pt)
      W - Full width of the arrow head in points (default: 5 pt)
      DIST - Arrow is to be retracted a given distance from the point (X, Y).
      DIMPLE - The back of the arrow head is indented by DIMPLE points.'''

    if phi is not None:
        at(x, y, phi=phi)
    elif along is not None:
        at(x, y, along=along)
    else:
        at(x, y)
    arrow(l, w, dl=dist, dimple=dimple)
    
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
    qi.f.atx = None
    qi.f.aty = None
    if x is None and y is None:
        qi.f.write('at -\n')
        return
    cmd = ['at']
    if type(x)==str:
        if x in at.xtype:
            cmd.append(x)
        else:
            qi.error('Bad specification for x')
    else:
        cmd.append('%g' % x)
        qi.f.atx = x
    if type(y)==str:
        if y in at.ytype:
            cmd.append(y)
        else:
            qi.error('Bad specification for y')
    else:
        cmd.append('%g' % y)
        qi.f.aty = y
    if phi is not None:
        cmd.append('%g' % phi)
    elif along is not None:
        cmd.append('%g %g' % (along[0], along[1]))
    if id is not None:
        cmd.append(id)
    qi.f.write(cmd)
at.xtype = utils.wordset('left right center abs absolute')
at.ytype = utils.wordset('top bottom middle abs absolute')

def title(ttl):
    '''TITLE - Render a title on the current QPlot
   TITLE(text) renders the given text centered along the top of the
   current QPlot figure.
   For more control over placement, use TEXT and friends.'''
    qi.ensure()
    at()
    pid = qi.f.panel
    if pid is None:
        xywh = qi.f.extent
    else:
        xywh = qi.f.panels[pid]
    align('top', 'center')
    text(ttl, dx=xywh[0] + xywh[2]/2, dy=xywh[1] + 5)
    
class LegOpt:
    x0 = 0
    y0 = 0
    skip = 15
    n = 0
    drop = 3
    height = 9
    width = 18
    indent = 9
    color = 'k'
    dx = 0
    dy = 0

def legopt(x0=None, y0=None, skip=None, height=None, width=None,
           indent=None, color=None, drop=None, dx=None, dy=None):
    '''QLEGOPT - Set options for LEGEND and friends
    LEGOPT specifies options for legend rendering.
    All arguments are optional:
      X0 - x position of left edge of legend, in data coordinates
      Y0 - y position of middle of top legend element, in data coordinates
      SKIP - baselineskip (in points) between elements
      HEIGHT - height (in points) of rendered patches
      WIDTH - width (in points) of rendered lines and patches
      INDENT - space between rendered samples and following text
      COLOR - color for following text
      DROP - vertical distance between middle of samples and text baseline
      DX, DY - additional horizontal and vertical displaced, in points
    All have sensible defaults, except X0 and Y0, which default to (0, 0).
    Legend elements are automatically rendered one below the other starting
    at Y0.'''
    qi.ensure()
    if qi.f.legopt is None:
        qi.f.legopt = LegOpt()
    if x0 is not None:
        qi.f.legopt.x0 = x0
    if y0 is not None:
        qi.f.legopt.y0 = y0
        qi.f.legopt.n = 0
    if skip is not None:
        qi.f.legopt.skip = skip
    if height is not None:
        qi.f.legopt.height = height
    if width is not None:
        qi.f.legopt.width = width
    if indent is not None:
        qi.f.legopt.indent = indent
    if color is not None:
        qi.f.legopt.color = color
    if drop is not None:
        qi.f.legopt.drop = drop
    if indent is not None:
        qi.f.legopt.indent = indent 
    if dx is not None:
        qi.f.legopt.dx = dx
    if dy is not None:
        qi.f.legopt.dy = dy

def legend(s):
    '''LEGEND - Render legend element for plotted line
    LEGEND(str) renders a sample of the most recently plotted line
    at the location set by LEGOPT and writes the given string
    next to it.
    See also MLEGEND and PLEGEND.'''
    legopt()
    opt = qi.f.legopt
    at(opt.x0, opt.y0)
    paper.line(np.array([0, 1])*opt.width + opt.dx,
               opt.n*opt.skip + np.array([0, 0]) + opt.dy)
    fig.startgroup()
    style.pen(opt.color)
    align('left', 'base')
    text(s, dx=opt.width + opt.indent + opt.dx,
         dy=opt.n*opt.skip + opt.drop + opt.dy)
    fig.endgroup()
    qi.f.legopt.n += 1

def mlegend(s=None):
    '''MLEGEND - Render legend element for marks
    MLEGEND(str) renders a sample of the most recently rendered 
    mark at the location set by LEGOPT and writes the given string
    next to it.
    MLEGEND() without a string renders the most recently used mark
    over a previously rendered (line) legend.
    See also LEGEND and PLEGEND.'''
    legopt()
    opt = qi.f.legopt
    at(opt.x0, opt.y0)
    if s is None:
        paper.pmark(.5*opt.width+opt.dx, (opt.n-1)*opt.skip+opt.dy)
    else:
        paper.pmark(.5*opt.width+opt.dx, opt.n*opt.skip+opt.dy)
        fig.startgroup()
        style.pen(opt.color)
        align('left', 'base')
        text(s, dx=opt.width + opt.indent + opt.dx,
             dy=opt.n*opt.skip + opt.drop + opt.dy)
        fig.endgroup()
        qi.f.legopt.n += 1

def plegend(s):
    '''PLEGEND - Render legend element for patch
    PLEGEND(str) renders a sample of the most recently rendered 
    patch at the location set by LEGOPT and writes the given string
    next to it.
    See also LEGEND and MLEGEND.'''
    
    
    legopt()
    opt = qi.f.legopt
    
    at(opt.x0, opt.y0)
    paper.area(np.array([0, 1, 1, 0])*opt.width + opt.dx,
               opt.n*opt.skip + np.array([-.5, -.5, .5, .5])*opt.height + opt.dy)
    fig.startgroup()
    style.pen(opt.color)
    align('left', 'base')
    text(s, dx=opt.width + opt.indent + opt.dx,
         dy=opt.n*opt.skip + opt.drop + opt.dy)
    fig.endgroup()
    qi.f.legopt.n += 1
        
def ctext(text, dx=0, dy=0):
    '''CTEXT - Render text after previous text
    CTEXT(text) renders text where previous text plotting left off.
    Optional arguments DX and DY modify placement by the given number
    of points.'''
    qi.ensure()
    qi.f.write('ctext %g %g "%s"\n' % (dx, dy, q__safetext(text)))

def textonpath(xx, yy, text, dx=0, dy=0):
    '''TEXTONPATH - Place text along a path
    TEXTONPATH(xx, yy, text) places the TEXT along a path (XX, YY)
    defined in data coordinates.
    Optional arguments DX and DY shift the text right by DX and down
    by DY pts in its local vertical direction.
    TEXTONPATH does not use coordinates set by AT, but it does respect
    alignment set by ALIGN.
    In the present version, TEXTONPATH only accepts plain Unicode; not
    any of the special characters sequences accepted by TEXT.'''

    N = len(xx)
    if len(yy) != N:
        qi.error('xx and yy must match')
    qi.ensure()
    qi.f.write('textonpath *%i *%i %g %g "%s"\n'
               % (N, N, dx, dx, q__safetext(text)))
    qi.f.writedbl(xx)
    qi.f.writedbl(yy)
    
