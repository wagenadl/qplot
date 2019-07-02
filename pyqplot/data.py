# Everything in the Plotting category

# bars
# caligraph
# ecoplot
# errorbars
# errorpatch
# mark
# patch
# plot
# skyline

import numpy as np
from . import qi
from . import utils


def plot(xx, yy=None):
    '''PLOT - Draw a line series in data space
    PLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
    coordinates.
    PLOT(yy) plots the data against x = 1..N.
    See also LINE and GLINE.'''
    if yy is None:
        yy = xx
        xx = range(len(yy))
    qi.plot(xx, yy, cmd='plot')

def patch(xx, yy):
    '''PATCH - Draw a polygonal patch in data space
    PATCH(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
    The polygon is filled with the current brush.
    XX and YY are given in data coordinates. See also AREA and GAREA.'''
    qi.plot(xx, yy, cmd='patch')

def mark(xx, yy):
    '''MARK - Draw on the current graph with the current marker
    MARK(xx, yy) draws marks at the given location in data space. See also
    MARKER and PMARK.'''
    qi.ensure()
    if utils.isempty(xx):
        return
    xx = np.array(utils.aslist(xx))
    yy = np.array(utils.aslist(yy))
    ok = ~np.isnan(xx+yy)
    xx = xx[ok]
    yy = yy[ok]
    qi.f.write('mark *%i *%i\n' % (len(xx), len(yy)))
    qi.f.writedbl(xx)
    qi.f.writedbl(yy)
    qi.f.updaterange(xx, yy)

def bars(xx, yy, w, y0=0):
    '''BARS - Bar plot with bar width specified in data coordinates
    BARS(xx, yy, w) draws a bar graph of YY vs XX with bars
    of width W specified in data coordinates.
    BARS(xx, yy, w, y0) specifies the baseline of the plot;
    default for Y0 is 0. Y0 may also be a vector (which must
    then be the same size as XX and YY). This is useful for
    creating stacked bar graphs.'''
    if utils.isnscalar(y0):
        y0=np.zeros(yy.shape) + y0
        
    for k in range(xx.size):
        patch(np.array([-.5, .5, .5, -.5])*w + xx[k],
              np.array([0, 0, 1, 1])*yy[k] + y0[k])

def ecoplot(x0, dx, yy, N=100):
    '''QECOPLOT - Economically plot large datasets
    ECOPLOT(x0, dx, yy, N) plots the data (xx,yy) using SAMPLEMINMAX to
    reduce data length to the given number of points.
    The results are plotted as a PATCH.
    X-coordinates are implied to be [X0, X0+DX, X0+2*DX, ...], along YY.
    If N is omitted, it defaults to 100.
    Note: This is the kind of plot that MEABench calls "TrueBlue".'''
    
    K = len(yy)
    if N>K:
        N=K
    ii = np.linspace(0, K, N+1).astype(int)
    ym, yM = utils.sampleminmax(yy, ii)
    xx = (ii[0:-1].astype(float) + ii[1:].astype(float))/2
    
    patch(x0+dx*np.concatenate((xx, np.flip(xx,0))),
          np.concatenate((ym, np.flip(yM,0))))

def errorbar(xx, yy, dy, w=None, dir='both'):
    '''QERRORBAR - Draw error bars
    ERRORBAR(xx, yy, dy) plots error bars at (XX,YY+-DY).
    Normally, XX, YY, and DY have the same shape. However, it is permissible
    for DY to be shaped Nx2, in which case lower and upper error bounds
    are different. (DY should always be positive).
    QERRORBAR(xx, yy, dy, w) adorns the error bars with horizontal lines of
    given width (W in points).
    QERRORBAR(..., 'up') only plots upward; QERRORBAR(..., 'down') only plots
    downward.'''

    N = len(xx)
    if np.prod(dy.shape)==2*N:
        dy_dn = -dy[:,0]
        dy_up = dy[:,1]
    else:
        dy_up = dy
        dy_dn = -dy

    if dir=='up':
        dy_dn = 0*dy_dn
    elif dir=='down':
        dy_up = 0*dy_up
    elif dir!='both':
        qi.error('Bad direction name')

    for n in range(N):
        plot(xx[n]+np.zeros(2), yy[n] + np.array([dy_dn[n], dy_up[n]]))
    
    if w>0:
        if dir!='down':
            # Draw top ticks
            for n in range(N):
                qat(xx[n], yy[n] + dy_up[n])
                line(np.array([-1, 1])*w/2,np.array([0, 0]))
        if dir!='up':
            # Draw down ticks
            for n in range(N):
                qat(xx[n], yy[n] + dy_dn[n])
                line(np.array([-1, 1])*w/2,np.array([0, 0]))

def qerrorpatch(xx, yy, dy, dir='both'):
    '''ERRORPATCH - Draw error patch
    ERRORPATCH(xx, yy, dy) plots an error patch at (XX,YY+-DY).
    Normally, XX, YY, and DY have the same shape. However, it is permissible
    for DY to be shaped Nx2, in which case lower and upper error bounds
    are different.
    ERRORPATCH(..., 'up') only plots upward; QERRORPATCH(..., 'down') only 
    plots downward.'''

    N = len(xx)
    if np.prod(dy.shape)==2*N:
        dy_dn = -dy[:,0]
        dy_up = dy[:,1]
    else:
        dy_up = dy
        dy_dn = -dy

    if dir=='up':
        dy_dn = 0*dy_dn
    elif dir=='down':
        dy_up = 0*dy_up
    elif dir!='both':
        qi.error('Bad direction name')
    
    patch(np.concatenate((xx, np.flip(xx, 0))),
          np.concatenate((yy + dy_dn, np.flip(yy+dy_up, 0))))

def skyline(xx, yy, y0=0):
    '''SKYLINE - Skyline plot (bar plot)
    SKYLINE(xx, yy) draws a bar plot of YY vs XX with bars touching.
    SKYLINE(xx, yy, y0) specifies the baseline of the plot; default is 0.'''
    N = len(xx)
    if N==1:
        xxx = np.array([-.5, .5]) + xx
        yyy = np.array([yy, yy])
    else:
        dx = np.diff(xx)
        dx = np.concatenate((dx[[0]], dx, dx[[-1]]),0)
        xxx = np.reshape(xx,(N,1))
        dx = np.reshape(dx,(N+1,1))
        xxx = np.concatenate((xxx-dx[0:-1,[0]]/2, xxx+dx[1:,[0]]/2), 1)
        yyy = np.reshape(yy,(N,1))
        yyy = np.concatenate((yyy,yyy), 1)
        xxx = np.reshape(xxx,(2*N))
        yyy = np.reshape(yyy,(2*N))
    
    patch(np.concatenate((xxx[[0]], xxx ,xxx[[-1]]), 0),
          np.concatenate(([y0], yyy, [y0])))
    
def caligraph(xx, yy, ww):
    '''CALIGRAPH - Draw a variable-width line series in data space
    CALIGRAPH(xx, yy, ww) plots the data YY vs XX. XX and YY are given in 
    data coordinates. WW specifies the line width at each point, in postscript
    points.
    The line is rendered in the current pen's color; dash patterns and cap
    and join styles are not used.'''
    N = len(xx)
    if len(yy) != N or len(ww) != N:
        qi.error('xx, yy, ww must be equally long')
    
    [iup, idn] = utils.nonanstretch(xx+yy+ww)

    qi.ensure()
    for k in range(len(iup)):
        N = idn[k] - iup[k]
        qi.f.write('caligraph *%i *%i *%i\n', N, N, N)
        qi.f.writedbl(xx[iup[k]:idn[k]], 'double')
        qi.f.writedbl(yy[iup[k]:idn[k]], 'double')
        qi.f.writedbl(ww[iup[k]:idn[k]], 'double')
    
