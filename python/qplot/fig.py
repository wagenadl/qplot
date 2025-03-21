# Everything in the Figures category and also the Scale to fit category
# Also the Grouping category

# clf
# close
# closeall
# current
# endgroup
# figure
# (not qprint)
# panel
# relpanel
# save
# select
# alignaxes
# commonscale
# shrink
# group
# subplot
# xlim
# ylim

import numpy as np
import numbers
from . import qi
from . import style
from . import utils
import os

def figure(fn=None, w=None, h=None, unit="in"):
    '''FIGURE - Open a QPlot figure
    FIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
    in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
    W defaults to 5 inches.

    fn = FIGURE('', w, h) opens a new QPlot figure of given size (in inches)
    with a temporary filename.

    Optional argument UNIT specifies alternative units. FIGURE
    understands inch, mm, cm, and pt.

    As a convenience, fn = FIGURE(w, h) also works

    '''
    
    if h is None and isinstance(fn, numbers.Number):
        h = w
        w = fn
        fn = None
    if w is None:
        w = 5
    if h is None:
        h = 0.75 * w

    if unit=="in" or unit=="inch":
        pass
    elif unit=="cm":
        w = w / 2.54
        h = h / 2.54
    elif unit=="mm":
        w = w / 25.4
        h = h / 25.4
    elif unit=="pt":
        w = w / 72
        h = h / 72
    else:
        raise ValueError("Unknown unit")
    
    if qi.figisopen(fn):
        qi.f = qi.refigure(fn, w, h)
    else:
        qi.f = qi.Figure(fn, w, h)
        qi.figs[qi.f.fn] = qi.f
    if utils.isempty(fn):
        return qi.f.fn
    # Default: return nothing

def select(fn):
    '''SELECT - Select a previously created QPlot figure for more work
    SELECT(fn), where FN is the name of a previously created QPlot figure,
    directs subsequent QPlot commands to that figure.'''
    if fn not in qi.figs and not fn.endswith('.qpt'):
        fn += '.qpt'
    if fn in qi.figs:
        qi.f = qi.figs[fn]
        qi.f.tofront()
    else:
        qi.error('No such figure')

def clf():
    '''CLF - Clear current QPlot figure
  CLF clears the current QPlot figure. '''
    if qi.f is None:
        ensure()
    else:
        qi.f.clf()

def close(fn=None):
    '''CLOSE - Close a QPlot window
    CLOSE closes the current window.
    CLOSE(filename) closes the named window.
    See also CLOSEALL.'''
    current = False
    if fn is None:
        if qi.f is not None:
            fn = qi.f.fn
            current = True
    if fn in qi.figs:
        if current:
            qi.f = None
        qi.figs[fn].close()
        del qi.figs[fn]
        if current:
            for (fn, f) in qi.figs.items():
                if f.fd is not None:
                    qi.f = f
                    return
    else:
        qi.error('No such figure')

def closeall():
    '''CLOSEALL - Close all QPlot windows'''
    fns = [ f for f in qi.figs ]
    for fn in fns:
        close(fn)
    qi.f = None
            
def xlim(x0=None, x1=None):
    '''XLIM - Set x-axis limits
    XLIM(x0, x1) or XLIM([x0, x1]) sets x-axis limits in the current panel.
    This means that data outside of that range are not included in
    calculations for shrink. It does not mean that such data are not
    plotted.'''
    if x0 is None:
        qi.error('Usage: xlim x0 x1')    
    if x1 is None:
        x1 = x0[1]
        x0 = x0[0]

    qi.f.write('xlim %g %g\n' % (x0, x1))

def ylim(y0=None, y1=None):
    '''YLIM - Set y-axis limits
    YLIM(y0, y1) or YLIM([y0, y1]) sets y-axis limits in the current panel.
    This means that data outside of that range are not included in
    calculations for shrink. It does not mean that such data are not
    plotted.'''
    if y0 is None:
        qi.error('Usage: ylim y0 y1')    
    if y1 is None:
        y1 = y0[1]
        y0 = y0[0]
    qi.ensure()
    qi.f.write('ylim %g %g\n' % (y0, y1))

def group():
    '''GROUP - Start a group for bounding box collection'''
    qi.ensure()
    qi.f.write('group\n')

def endgroup():
    '''ENDGROUP - End a group for bounding box collection'''
    qi.ensure()
    qi.f.write('endgroup\n')


def _autoid():
    for k in range(26):
        id = "%c" % (65 + k)
        if id not in qi.f.panels:
            return id
    for k in range(26):
        for l in range(26):
            id = "%cZ%c" % (65 + k, 65 + l)
            if id not in qi.f.panels:
                return id
    qi.error('Too many panels')
    
    

def panel(id=None, rect=None):
    '''PANEL - Define a new subpanel or reenter a previous one
    PANEL(id, (x, y, w, h)) defines a new panel. 
    Either absolute or relative coordinates may be used:
    Absolute means (X, Y, W, H) are specified in points (1/72th of an inch).
    Relative means (X, Y, W, H) are specified relative to figure size.
    Coordinates are understood to be relative if all are ≤ 1.
    In either case (X, Y) are measured from top left.
    PANEL(id) revisits a previously defined panel. 
    PANEL() reverts to the top level.
    If ID is None but a rectangle is specified, a new ID is automatically
    assigned and returned.
    See also SUBPLOT.'''
    qi.ensure()
    qi.f.panel = id
    qi.f.datarange = None
    retid = False
    
    out = ['panel']
    if id is None:
        if rect is None:
            id = '-'
        else:
            id = _autoid()
            retid = True
    out.append(id)
    if rect is not None:
        isrel = all([dim<1.001 for dim in rect])
        x,y,w,h = rect
        if isrel:
            W = qi.f.extent[2]
            H = qi.f.extent[3]
            x *= W
            y *= H
            w *= W
            h *= H
        out.append(f"{x} {y} {w} {h}")            
        if id != '-':
            qi.f.panels[id] = rect
    qi.f.write(out)
    if retid:
        return id

    
def relpanel(id, rect):
    '''RELPANEL - Define  a new subpanel
    Now an alias for PANEL, which see.'''
    panel(id, rect)
    

def subplot(rows, cols, r=None, c=None):
    '''SUBPLOT - Define a new subpanel in Matlab/Octave style
    SUBPLOT(rows, cols, idx) defines a new subpanel in Matlab/Octave style.
    Note that idx counts from 0, unlike in Matlab/Octave.
    SUBPLOT(rows, cols, r, c) specifies row and column.
    
    id = SUBPLOT(...) returns the ID of the subpanel, for use with PANEL.'''
    h = 1./rows
    w = 1./cols
    if c is None:
        idx = r
        if idx<0 or idx>=rows*cols:
            qi.error("Subplot index out of range")
        c = idx % cols
        r = idx // cols
    else:
        if c<0 or c>=cols:
            qi.error("Subplot column out of range")
        if r<0 or r>=rows:
            qi.error("Subplot row out of range")
    x = c*w
    y = r*h
    qi.ensure()
    if r > 26 or c > 26:
        r1 = r // 26
        r2 = r % 26
        c1 = c // 26
        c2 = c % 26
        id = "%c%c%c%" % (65 + r1, 65 + r2, 65 + c1, 65 + c2)
    else:
        id = "%c%c" % (65 + r, 65 + c)
    relpanel(id, (x,y,w,h))
    return id
    
def save(ofn=None, reso=300, qual=95):
    '''SAVE - Saves a qplot figure
    SAVE(ofn) saves the current qplot figure to the named file.
    SAVE(ext), where EXT is just a filename extension (without the dot),
    uses the name of the current figure.
    Optional argument RESO specifies bitmap resolution for png/jpeg output. 
    (The default is 300 dpi).
    Optional argument QUAL specifies quality for jpeg output. (The default
    is 95.)
    SAVE without arguments saves to pdf.'''
    if qi.f is None:
        qi.error('No window')
    
    if ofn is None:
        ofn='pdf'
    pth, ext = os.path.splitext(ofn)
    if ext=='' and pth.find('/')<0:
        # Just an extension given
        ext = pth
        pth, oldext = os.path.splitext(qi.f.fn)
        ofn = pth + '.' + ext
    qi.f.save(ofn, reso, qual)

def shrink(margin=1, ratio=None):
    '''SHRINK - Add margin to QPlot panel
    SHRINK() adds 1 point of margin to the current QPlot panel.
    SHRINK(margin) adds the given margin (in points).
    SHRINK(margin, ratio) forces a given aspect ratio on the data units.
    SHRINK(None, ratio) only enforces aspect ratio.'''
    qi.ensure()
    out = ['shrink']
    if margin is None:
        out.append('-')
    else:
        out.append('%g' % margin)
    if ratio is not None:
        out.append('%g' % ratio)
    qi.f.write(out)

def commonscale(axis, ids):
    '''COMMONSCALE - Share axis scale between QPlot panels
    COMMONSCALE('xy', ids) shares x and y-axis scales between the named panels.
    COMMONSCALE('x', ids) only shares x-axis scale.
    COMMONSCALE('y', ids) only shares y-axis scale.
    IDS must be a list of panel IDs.
    See also ALIGNAXES and REBALANCE.'''
    out = ['commonscale']
    if axis=='x' or axis=='y' or axis=='xy':
        out.append(axis)
    else:
        qi.error('Bad axis specification')
    out += ids
    qi.ensure()
    qi.f.write(out)


def alignaxes(axis, ids):
    '''ALIGNAXES - Share axis limits between QPlot panels, aligning the axes
    ALIGNAXES('x', ids) aligns x-axes between the named panels. Alignment is 
    only performed within groups of panels that form a vertical stack. Between 
    groups, or if the panels do not form stacks at all, the horizontal scale
    is still shared (as in COMMONSCALE), but there will be no alignment.
    ALIGNAXES('y', ids) aligns y-axes. Alignment occurs within groups of panels
    that form a horizontal row.
    ALIGNAXES('xy', ids) aligns both x- and y-axes between the named panels.
    Grouping is performed independently for x and y.
    IDS must be a list of single-letter panel IDs.
    See also COMMONSCALE and REBALANCE.'''
    out = ['alignaxes']
    if axis=='x' or axis=='y' or axis=='xy':
        out.append(axis)
    else:
        qi.error('Bad axis specification')
    out += ids
    qi.ensure()
    qi.f.write(out)


def rebalance(axis, ids, *args):
    '''REBALANCE - Rebalance space between QPlot panels to achieve common scale
    REBALANCE('x', ids), where IDS is a list of named panels, rebalances horizontal
    space between the panels. This works if IDS represent a single horizontal row 
    of panels or a grid of panels. After, the horizontal scale of all of the panels
    will be the same, and axes will be aligned within columns (as per ALIGNAXES).
    REBALANCE('x', ids, moreids, ...) rebalances across all the columns represented 
    by the panels named in IDS and MOREIDS, but does not assume that the horizontal
    scales are the same between the two groups of panels. There is no limit on the
    number of groups of panels that can be rebalanced concurrently.
    REBALANCE('y', ...) rebalances vertical space.
    REBALANCE('xy', ...) rebalances in both directions.
    See also COMMONSCALE and ALIGNAXES.'''

    out = ['rebalance']
    if axis=='x' or axis=='y' or axis=='xy':
        out.append(axis)
    else:
        qi.error('Bad axis specification')

    out += ids
    for arg in args:
        out.append('-')
        out += arg
    qi.ensure()
    qi.f.write(out)
    
    
def current():
    '''CURRENT - Filename of current figure
    fn = CURRENT() returns the filename of the current figure or None
    if none are open.'''
    if utils.isempty(qi.figs):
        return None
    qi.ensure()
    return qi.f.fn


def ion():
    '''ION - Enable interactive rendering
    Subsequently created figures will show on screen.
    See also IOFF.'''
    qi.Figure.interactive(True)

def ioff():
    '''IOFF - Disable interactive rendering
    Subsequently created figures will not show on screen, but
    are still available to SAVE.
    See also ION.'''
    qi.Figure.interactive(False)

def degrees():
    '''DEGREES - Specify future angles to AT and HATCH in degrees
    See also RADIANS.'''
    qi.Figure.use_degrees()

def radians():
    '''RADIANS - Specify future angles to AT and HATCH in radians
    Radians are the default.
    See also DEGREES.'''
    qi.Figure.use_radians()
    
