# Everything in Graphics styling and also QFONT

# brush
# pen
# marker

import utils
import qi
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
        qi.f.pattern = pattern
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
    qi.ensure()
    qi.f.write(out)
pen.joins = utils.wordset('miterjoin beveljoin roundjoin')
pen.caps = utils.wordset('flatcap squarecap roundcap')
pen.patterns = utils.wordset('solid none dash dot')
    
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
    if shape not is None:
        if shape in qi.markermap:
            out.append(qi.markermap[shape])
        else:
            qi.error('Marker shape not understood')
    if size not is None:
        out.append('%g' % size)
    if fill not is None:
        if fill in marker.fills:
            out.append(fill)
        else:
            qi.error('Marker fill not understood')
    qi.ensure()
    qi.write(out)
marker.fills = utils.wordset('open solid brush spine')
