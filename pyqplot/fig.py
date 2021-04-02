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
# sharelim
# shrink
# group
# subplot
# xlim
# ylim

import numpy as np
from . import qi
from . import style
from . import utils
import os

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
    qi.figs[qi.f.fn] = qi.f
    return qi.f

def select(fn):
    '''SELECT - Select a previously created QPlot figure for more work
    SELECT(fn), where FN is the name of a previously created QPlot figure,
    directs subsequent QPlot commands to that figure.'''
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

def group():
    '''GROUP - Start a group for bounding box collection'''
    qi.ensure()
    qi.f.write('group\n')

def endgroup():
    '''ENDGROUP - End a group for bounding box collection'''
    qi.ensure()
    qi.f.write('endgroup\n')

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
            qi.f.panels[id] = rect

    qi.f.write(out)

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

def subplot(rows, cols, idx):
    '''SUBPLOT - Define a new subpanel in Matlab/Octave style
    SUBPLOT(rows, cols, idx) defines a new subpanel in Matlab/Octave style.
    id = SUBPLOT(...) returns the ID of the subpanel, for use with PANEL.
    Note that idx counts from 0, unlike in Matlab/Octave'''
    h = 1./rows
    w = 1./cols
    x = w * (idx % cols)
    y = h * (idx // cols)
    qi.ensure()
    for k in range(26):
        id = '%c' % (65 + k)
        if id not in qi.f.panels:
            # Gotcha
            style.pen('none')
            style.brush('none')
            relpanel(id, (x,y,w,h))
            style.pen('k')
            return
    qi.error('Too many panels')
    
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
        error('No window')
    
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

def sharelim(axes='all', ids=[]):
    '''SHARELIM - Share axis limits between QPlot panels
    SHARELIM(ids) shares x and y-axis limits with the other named panels.
    SHARELIM('x', ids) only shares x-axis limits.
    SHARELIM('y', ids) only shares y-axis limits.
    IDS must be a list of single-letter panel IDs or a string.'''
    if type(ids)==str:
        ids = [id for id in ids]
    out = ['sharelim']
    if axes=='x':
        out.append('x')
    elif axes=='y':
        out.append('y')
    elif axes!='all':
        qi.error('Bad axes specification')
    out += ids
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
