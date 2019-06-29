import numpy as np
import qplot_internal as qi
import fig

def figure(fn=None, w=5, h=None):
    '''FIGURE - Open a QPlot figure
    FIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
    in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
    W defaults to 5 inches.
    fn = FIGURE('', w, h) opens a new QPlot figure of given size (in inches)
    with a temporary filename.'''
    if fn in qi.figs:
        qi.curfig = qi.figs[fn]
        return fn
    f = fig.Figure(fn, w, h)
    qi.figs[fn] = f
    qi.curfig = f
    
def xlim(x0=None, x1=None):
    '''XLIM - Set x-axis limits
    XLIM(x0, x1) or XLIM([x0, x1]) sets x-axis limits in the current panel.'''
    if x0 is None:
        qi.error('Usage: xlim x0 x1')    
    if x1 is None:
        x1 = x0[1]
        x0 = x0[0]

    qi.write('xlim %g %g\n' % (x0, x1))

def ylim(y0=None, y1=None):
    '''YLIM - Set y-axis limits
    YLIM(y0, y1) or YLIM([y0, y1]) sets y-axis limits in the current panel.'''
    if y0 is None:
        qi.error('Usage: ylim y0 y1')    
    if y1 is None:
        y1 = y0[1]
        y0 = y0[0]

    qi.write('ylim %g %g\n' % (y0, y1))

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

def startgroup():
    qi.ensure()
    qi.write('group')

def endgroup():
    qi.ensure()
    qi.write('endgroup')
