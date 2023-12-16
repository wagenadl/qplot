# Everything in Graphics styling and also QFONT, but not QLUT (see img)

# brush
# font
# marker
# pen
# hairline

from . import utils
from . import qi
import numpy as np

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
    qi.ensure()
    qi.f.write(out)

def pen(color=None, width=None, join=None, cap=None, pattern=None, \
        alpha=None, id=None):
    '''PEN - Selects a new pen for QPlot
    All arguments are optional.
      COLOR may be a single character matlab color, or a 3- or 6-digit RGB
      specification or an [r, g, b] triplet, or 'none'. Color may also be
      '-' to reset a pen completely.
      WIDTH is linewidth in points, or 0 for hairline.
      JOIN must be one of: 'miter', 'bevel', 'round'.
      CAP must be one of: 'flat', 'square', 'round'.
      PATTERN must be one of: 'solid', 'dash', 'dot', 'none'.
      PATTERN may also be a tuple ('dash', vec) where VEC is a vector of 
        stroke and space lengths, or it may be a tuple ('dot', vec) where
        VEC is a vector of space lengths.
      ALPHA specifies transparency between 0 and 1.
      ID must be a single capital letter.
    Note that the string 'none' is different from the Python constant None,
    the latter meaning "do not change."'''
    out = [ 'pen' ]
    if id is not None:
        out.append(id)
    if type(color)==str and color=='-':
        out.append('-')
        qi.f.linewidth = 0.5 # See Figure::defaultPen()
    else:
        color = qi.interpretcolor(color)
        if color is not None:
            out.append(color)
    if alpha is not None:
        out.append('%g' % -alpha)
    if width is not None:
        out.append('%g' % width)
        qi.f.linewidth = width
    if join is not None:
        if join in pen.joins:
            out.append(join + 'join')
        else:
            qi.error('Join type not understood')
    if cap is not None:
        if cap in pen.caps:
            out.append(cap + 'cap')
        else:
            qi.error('Cap type not understood')
    if pattern is not None:
        qi.f.pattern = pattern
        if type(pattern)==tuple and (pattern[0]=='dash' or pattern[0]=='dot'):
            out.append(pattern[0])
            out.append('[')
            pat = utils.aslist(pattern[1])
            for a in pat:
                out.append('%g' % a)
            out.append(']')
        elif pattern in pen.patterns:
            out.append(pattern)
        else:
            qi.error('Pattern type not understood')
    qi.ensure()
    qi.f.write(out)
pen.joins = utils.wordset('miter bevel round')
pen.caps = utils.wordset('flat square round')
pen.patterns = utils.wordset('solid none dash dot')
    
def font(family=None, size=None, bold=False, italic=False):
    '''FONT - Select font 
    FONT(...) selects a new font for QPlot.
    The default font is Helvetica at 10 points.
    All arguments are optional:
      FAMILY - Font family name (default: Helvetica)
      SIZE - Font size in points (default: 10)
      BOLD - Select bold face if true
      ITALIC - Select italic (or slanted) if true'''
    qi.ensure()
    if family is None:
        family = qi.f.fontfamily
    else:
        qi.f.fontfamily = family
    if size is None:
        size = qi.f.fontsize
    else:
        qi.f.fontsize = size
    out = ['font', family]
    if bold:
        out.append('bold')
    if italic:
        out.append('italic')
    out.append('%g' % size)
    qi.f.write(out)
    
def marker(shape=None, size=None, fill=None):
    '''MARKER - Select a new marker for MARK and PMARK
    MARKER(shape, size, fill) selects a marker.
    All arguments are optional.
    SHAPE must be one of + x - | o s d < > ^ v p h; see below.
    SIZE is specified in points.
    FILL is one of open|solid|brush|spine:
      OPEN - The mark is filled with white
      SOLID - The mark is filled with the current pen's color
      BRUSH - The mark is filled with the current brush's color
      SPINE - Draws lines from the center to the vertices of the chosen shape
        instead of drawing the shape.
    The mark is always outlined with the current pen (which may be 'none',
    of course).
    Marks are: o: circle/disk
               + x: horizontal+vertical or diagonal crosses
               - |: horizontal or vertical lines
               s d p h: square, diamond, pentagon, or hexagon
               < > ^ v: left / right / up / down pointing triangles
    The fill style has no effect on +|x|-|| marks; SPINE is like BRUSH 
    for circle.'''
    out = [ 'marker' ]
    if shape is not None:
        if shape in qi.markermap:
            out.append(qi.markermap[shape])
        else:
            qi.error('Marker shape not understood')
    if size is not None:
        out.append('%g' % size)
    if fill is not None:
        if fill in marker.fills:
            out.append(fill)
        else:
            qi.error('Marker fill not understood')
    qi.ensure()
    qi.f.write(out)
marker.fills = utils.wordset('open solid brush spine')

def hairline(width):
    '''HAIRLINE - Specify hairline width
    HAIRLINE(width) specifies the width of hairlines (lines with 
    nominal width 0) as rendered to screen or pdf.
    The default is 0.25 pt when rendering to pdf. When rendering to
    screen, the default is 0, which implies "one pixel wide".
    Unlike all other QPlot commands, this one is effective retroactively
    as well as proactively: It affects every single object in the current
    figure that is plotted with nominal width 0.'''
    qi.ensure()
    qi.f.write('hairline %g\n' % width)
    
