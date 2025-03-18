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
align.words = set('left right center top bottom middle base'.split(' '))

def _safetext(s):
    s = s.replace('"', '”')
    s = s.replace('\\', '\\\\')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    # Anything else?
    return s

def reftext(s):
    '''REFTEXT - Set reference text
    REFTEXT(text) sets the reference text used for vertical alignment
    of subsequent TEXT commands.'''

    qi.ensure()
    qi.f.reftext = s
    qi.f.write('reftext "%s"\n' % _safetext(s))
    
def text(s, dx=0, dy=0):
    '''TEXT - Render text 
    TEXT(text) renders text at the current anchor point.
    TEXT(text, dx, dy) renders text displaced by the given number of
    points. Normally, positive DX is to the right and positive DY down,
    but the x- and y-axes rotate along with the angle set by the AT 
    command.
    Text between underscore (_) and next space is set as subscript.
    Text between hat (^) and next space is set as superscript. Matched
    parentheses, brackets, and quotes protect spaces. Additionally,
    tilde (~) can be used as a protected space inside sub- or superscripts.
    Words can be /italicized/ or *boldfaced* with slashes and
    asterisks. “Words” in this context means a sequence of letters
    and/or numbers. Slashes and asterisks that do not form pairs
    around a word are not interpreted specially. 
    As in TeX math, \\, inserts a thin space, and \\! inserts a thin
    negative space.
    
    Examples of valid strings:
    
      "Distance (μm)" - Unicode is fully supported.
      "Coefficient *A*_1^2" - Boldface, subscript, superscript.
      "Coefficient *A*_{1^2}" - Nested subscript. Braces are eaten.
      "Coefficient *A*_{{1}}" - Nested subscript. Extra braces are not eaten.
      "/x/^{2}/2" - Braces help interpret end of superscript.
      "e^-½(/x/^2 + /y/^2)" - The parentheses protect the outer superscript.
      "e^-½{(/x/^2 + /y/^2) / σ^2}" - Braces are needed to protect
         spaces not protected by parentheses.
      "frown^:\\( or smile^:\\)" - Backslashes prevent unwanted space 
        protection.
      "frown^{:(} or smile^{:)}" - Braces obviate the need for backslashes.


    See also AT and ALIGN.

    '''
    qi.ensure()
    s = s.replace('"', '”')
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
    paper.poly(np.array([0, -l, dimple-l, -l]) - dl,
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
    
def at(x=None, y=None, phi=None, deg=None, rad=None,
       along=None, notransform=False):
    '''AT - Specify location for future text
    AT(x, y) specifies that future text will be placed at data location (x,y)
    Optional arguments:
      DEG - text will be rotated counterclockwise by DEG degrees.
      RAD - text will be rotated counterclockwise by RAD radians.
      PHI - specifies that the text will be rotated clockwise by phi radians
            (deprecated).
      ALONG - must be a tuple (dx,dy), meaning that the text will be
            rotated s.t. the baseline points in the data direction (dx,dy).

    X may also be one of 'left,' 'right,' 'center,' 'abs,' 'absolute.'
    Y may also be one of 'top,' 'bottom,' 'middle,' 'abs,' 'absolute.'
    If X and/or Y is omitted, placements reverts to absolute in those
    dimensions.'''
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
        if not notransform:
            x = qi.f.xtransform(x)
        cmd.append('%g' % x)
        qi.f.atx = x
        
    if type(y)==str:
        if y in at.ytype:
            cmd.append(y)
        else:
            qi.error('Bad specification for y')
    else:
        if not notransform:
            y = qi.f.ytransform(y)
        cmd.append('%g' % y)
        qi.f.aty = y
    if phi is not None:
        cmd.append('%g' % qi.to_radians(phi))
    elif deg is not None:
        cmd.append('%g' % (-np.pi*deg/180))
    elif rad is not None:
        cmd.append('%g' % (-rad))
    elif along is not None:
        cmd.append('%g %g' % (along[0], along[1]))
    qi.f.write(cmd)
at.xtype = set('left right center abs absolute -'.split(' '))
at.ytype = set('top bottom middle abs absolute -'.split(' '))

def memo(id, x, y):
    '''MEMO - Store a location for later use
    MEMO(id, x, y) stores the location of the data point (x,y) for
    later use by RECALL.
    X and Y may be data coordinates, but more usefully they may be
    “left”, “center”, “right” for X, or “top”, “middle”, “bottom” for Y.'''
    qi.ensure()
    qi.f.write(f'at {x} {y} {id}\n')

def recall(ids, deg=None, rad=None, along=None):
    '''RECALL - Revisit a previously stored location
    RECALL(id) revisits the previously named location. 
    RECALL([ids]) revisits the center of several previously named locations.
    Optional arguments DEG, RAD, ALONG work as in AT.
    Locations are stored on a per-figure basis, not on a per-subplot basis.
    This is useful, e.g., to place text that spans across panels after 
    shrinking.
    '''
    cmd = ['at']
    if type(ids)==str:
        cmd.append(ids)
    else:
        for id in ids:
            cmd.append(id) # allow list or numpy array
    if deg is not None:
        cmd.append(f"{-deg*np.pi/180}")
    elif rad is not None:
        cmd.append(f"{-rad}")
    elif along is not None:
        cmd.append(f"{along[0]} {along[1]}")
    qi.f.write(cmd)
    
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
    pass

def legopt(x0=None, y0=None, skip=15, height=9, width=18,
           indent=9, color='k', drop=3, dx=0, dy=0):
    '''LEGOPT - Set options for LEGEND and friends
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
    qi.f.legopt.x0 = x0
    qi.f.legopt.y0 = y0
    qi.f.legopt.n = 0
    qi.f.legopt.skip = skip
    qi.f.legopt.height = height
    qi.f.legopt.width = width
    qi.f.legopt.indent = indent
    qi.f.legopt.color = color
    qi.f.legopt.drop = drop
    qi.f.legopt.indent = indent 
    qi.f.legopt.dx = dx
    qi.f.legopt.dy = dy

def legend(s):
    '''LEGEND - Render legend element for plotted line
    LEGEND(str) renders a sample of the most recently plotted line
    at the location set by LEGOPT and writes the given string
    next to it.
    See also MLEGEND and PLEGEND.'''
    opt = qi.f.legopt
    at(opt.x0, opt.y0)
    paper.line(np.array([0, 1])*opt.width + opt.dx,
               opt.n*opt.skip + np.array([0, 0]) + opt.dy)
    fig.group()
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
    opt = qi.f.legopt
    at(opt.x0, opt.y0)
    if s is None:
        paper.pmark(.5*opt.width+opt.dx, (opt.n-1)*opt.skip+opt.dy)
    else:
        paper.pmark(.5*opt.width+opt.dx, opt.n*opt.skip+opt.dy)
        fig.group()
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
    
    opt = qi.f.legopt
    
    at(opt.x0, opt.y0)
    paper.poly(np.array([0, 1, 1, 0])*opt.width + opt.dx,
               opt.n*opt.skip + np.array([-.5, -.5, .5, .5])*opt.height + opt.dy)
    fig.group()
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
    qi.f.write('ctext %g %g "%s"\n' % (dx, dy, _safetext(text)))

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
               % (N, N, dx, dx, _safetext(text)))
    qi.f.writedbl(xx)
    qi.f.writedbl(yy)
    
