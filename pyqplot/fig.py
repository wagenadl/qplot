# Everything in the Figures category and also the Scale to fit category
# Also the Grouping category

# figure
# clf
# close
# closeall
# xlim
# ylim
# startgroup
# endgroup
# panel
# relpanel
# subplot
# not qprint
# select
# NEXT UP: save

import numpy as np
import qi
import style

def figure(fn=None, w=5, h=None):
    '''FIGURE - Open a QPlot figure
    FIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
    in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
    W defaults to 5 inches.
    fn = FIGURE('', w, h) opens a new QPlot figure of given size (in inches)
    with a temporary filename.'''
    if fn in qi.figs:
        qi.f = qi.figs[fn]
        return fn
    qi.f = qi.Figure(fn, w, h)
    qi.figs[fn] = qi.f
    return qi.f

def select(fn):
    if not fn.endswith('.qpt'):
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
    '''QCLOSE - Close a QPlot window
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
            for f in qi.figs:
                if f.fd not is None:
                    qi.f = f
                    return
    else:
        qi.error('No such figure')

def closeall():
    '''CLOSEALL - Close all QPlot windows'''
    fns = [ f.fn for f in qi.figs ]
    for fn in fns:
        close(fn)
            
def xlim(x0=None, x1=None):
    '''XLIM - Set x-axis limits
    XLIM(x0, x1) or XLIM([x0, x1]) sets x-axis limits in the current panel.'''
    if x0 is None:
        qi.error('Usage: xlim x0 x1')    
    if x1 is None:
        x1 = x0[1]
        x0 = x0[0]

    qi.f.write('xlim %g %g\n' % (x0, x1))

def ylim(y0=None, y1=None):
    '''YLIM - Set y-axis limits
    YLIM(y0, y1) or YLIM([y0, y1]) sets y-axis limits in the current panel.'''
    if y0 is None:
        qi.error('Usage: ylim y0 y1')    
    if y1 is None:
        y1 = y0[1]
        y0 = y0[0]
    qi.ensure()
    qi.f.write('ylim %g %g\n' % (y0, y1))

def startgroup():
    qi.ensure()
    qi.f.write('group')

def endgroup():
    qi.ensure()
    qi.f.write('endgroup')

def panel(id, rect=None):
    '''PANEL - Define a new subpanel or reenter a previous one
    PANEL(id, (x, y, w, h)) defines a new panel. (X, Y, W, H) are 
    specified in points. (X, Y) are measured from top left.
    PANEL(id) revisits a previously defined panel. ID must be a single
    capital or None to revert to the top level.
    See also SUBPLOT and RELPANEL.'''
    qi.ensure()
    qi.f.panel = id
    qi.f.datarange = None
        
    out = ['panel']
    if id is None:
        out.append('-')
    else:
        out.append(id)
    if rect is not None:
        if id is None:
            qi.error('Cannot specify panel extent for root panel.')
        for k in range(4):
            out.append('%g' % rect[k])
        if id is not None:
            qi.panels[id] = rect

    qi.f.write(' '.join(out))

def relpanel(id, rect):
    '''RELPANEL - Define  a new subpanel
    PANELSUB(id, (x, y, w, h)) defines a new panel. (X, Y, W, H) are 
    specified as a fraction of the figure width and height.
    ID must be a single capital.
    See also SUBPLOT and PANEL.'''
    qi.ensure()
    panel(id, (rect[0]*qi.f.extent[2],
               rect[1]*qi.f.extent[3],
               rect[2]*qi.f.extent[2],
               rect[3]*qi.f.extent[3]))

def subplot(row, cols, idx):
    '''SUBPLOT - Define a new subpanel in Matlab/Octave style
    SUBPLOT(rows, cols, idx) defines a new subpanel in Matlab/Octave style.
    id = SUBPLOT(...) returns the ID of the subpanel, for use with PANEL.'''
    h = 1./rows
    w = 1./cols
    x = w * (idx-1 % cols)
    y = h * ((idx-1) // cols)
    qi.ensure()
    for k in range(26):
        id = '%c' % (65 + k)
        if id not in qi.f.panels:
            # Gotcha
            style.pen(None)
            style.brush(None)
            relpanel(id, (x,y,w,h))
            style.pen('k')
            return
    qi.error('Too many panels')
    
