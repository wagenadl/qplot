# Everything in Graphics styling and also QFONT

# brush
# pen
# font

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
    
def font(family, size=10, bold=False, italic=False):
    '''FONT - Select font 
    FONT(family) selects a new font for QPlot.
    The default font is Helvetica at 10 points.
    Optional arguments:
      SIZE - Set size in points (default: 10)
      BOLD - Select bold face if true
      ITALIC - Select italic (or slanted) if true'''
    out = ['font' family]
    if bold:
        out.append('bold')
    if italic:
        out.append('italic')
    if size:
        out.append('%g' % size)
    qi.ensure()
    qi.f.write(out)
    
