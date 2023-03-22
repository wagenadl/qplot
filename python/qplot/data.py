# Everything in the Plotting category

# bars
# caligraph
# ecoplot
# errorbar
# errorpatch
# mark
# patch
# plot
# skyline

import numpy as np
from . import qi
from . import utils
from . import paper
from . import markup

def xtransform(foo=None):
    '''XTRANSFORM - Specify a transformation to be applied to all x-data
    XTRANSFORM(foo), where FOO is a callable that accepts numpy arrays,
    specifies a transformation to apply to all x-data. 
    XTRANSFORM(None) reverts to linear plotting.

    The transformation applies to coordinates passed into commands like
    PLOT, PATCH, AT, XAXIS, LEGOPT, IMAGE, etc. It also applies to the 
    ABSDATA subcommand for GLINE and friends. However, it does not apply
    to the RELDATA or ROTDATA subcommands.

    See also YTRANSFORM.'''
    qi.ensure()
    qi.f._xtransform = foo

def ytransform(foo=None):
    '''YTRANSFORM - Specify a transformation to be applied to all y-data
    YTRANSFORM(foo), where FOO is a callable that accepts numpy arrays,
    specifies a transformation to apply to all y-data.
    YTRANSFORM(None) reverts to linear plotting.

    See XTRANSFORM for more details.'''
    qi.ensure()
    qi.f._ytransform = foo
    
def clipy(xx, yy, ymin=None, ymax=None):
    '''CLIPY - Clip data at given y-values for plotting
    xx, yy = CLIPY(xx, yy, ymin, ymax) finds runs in the data where
    YMIN <= YY <= YMAX and returns those runs, placing np.nan in between 
    runs. At the beginning and end of each run, a point (X, YMIN) or (X, YMAX)
    is inserted that marks the linearly interpolated location where the run 
    passes through the threshold.
    This is useful for plotting, because qplot does not implement XLIM and 
    YLIM with a proper clip rectangle.'''
    if ymin is not None:
        xx, yy = clipy(xx, np.negative(yy), ymax=-ymin)
        yy = -yy
    if ymax is None:
        return xx, yy
    runs = []
    inrun = False
    run = []
    for n, y in enumerate(yy):
        if inrun:
            if y<=ymax:
                run.append(n)
            else:
                if len(run):
                    runs.append(run)
                    run = []
                    inrun = False
        else:
            if y<=ymax:
                run.append(n)
                inrun = True
    if len(run):
        runs.append(run)

    xxx = []
    yyy = []
    for run in runs:
        rxx = xx[run]
        ryy = yy[run]
        if run[0]>0:
            # Prepend something
            x = np.interp(ymax, [yy[run[0]], yy[run[0]-1]],
                          [xx[run[0]], xx[run[0]-1]])
            rxx = np.concatenate(([x], rxx))
            ryy = np.concatenate(([ymax], ryy))
        if run[-1]<len(xx)-1:
            # Append something
            x = np.interp(ymax, [yy[run[-1]], yy[run[-1]+1]],
                          [xx[run[-1]], xx[run[-1]+1]])
            rxx = np.append(rxx, x)
            ryy = np.append(ryy, ymax)
        xxx.append(rxx)
        yyy.append(ryy)

    if len(xxx)==0:
        return np.array([]), np.array([])
    xx = xxx[0]
    yy = yyy[0]
    for k in range(1,len(xxx)):
        xx = np.append(xx, np.nan)
        yy = np.append(yy, np.nan)
        xx = np.concatenate((xx, xxx[k]))
        yy = np.concatenate((yy, yyy[k]))
    return xx, yy
        
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
    is automatically closed (i.e., it is not necessary for xx[-1] to equal
    xx[0]).
    The polygon is filled with the current brush.
    XX and YY are given in data coordinates. See also AREA and GAREA.'''
    qi.plot(xx, yy, cmd='patch')

def rectangle(x, y, w, h):
    '''RECTANGLE - Draw a rectangle in data space
    RECTANGLE(x, y, w, h) draws a rectangle in paper space with given
    coordinates. The rectangle is drawn with the current pen and filled
    with the current brush. See also PATCH.'''
    patch([x, x+w, x+w, x], [y, y, y+h, y+h])

def hatch(xx, yy, pattern="|", angle=0, spacing=10, offset=0):
    '''HATCH - Hatch a polygonal patch in data space
    HATCH(xx, yy, pattern) hatches a polygon with vertices at (XX,YY) using
    the given pattern. PATTERN is a single character from the following:
      | / - \  : lines at the angle suggested angle
      + x      : combination of either orthogonal or diagonal lines
      : *      : marks in an orthogonal or hexagonal pattern.
    Lines are rendered with the current PEN.
    Marks are rendereded as by MARK, i.e., with the current MARKER (and PEN
    and BRUSH).
    Instead of a pattern, a numeric ANGLE may be specified, clockwise from
    vertical (in radians, but see DEGREES).
    Optional argument SPACING specifies space between lines, in points.
    By default, the line pattern is aligned with the center of the polygon.
    OFFSET shifts this center by the given number of points.
    NaN values in XX or YY may be used to separate multiple polygons to be
    drawn with common line pattern alignment.
    See also PHATCH.

    '''
    qi.hatch(xx, yy, pattern, angle, spacing, offset)
    
    
def _mark(xx, yy, rx=None, ry=None, vert=None):
    '''MARK - Draw on the current graph with the current marker
    MARK(xx, yy) draws marks at the given location in data space. See also
    MARKER and PMARK.'''
    qi.ensure()
    if utils.isempty(xx):
        return
    xx = np.array(utils.aslist(xx))
    yy = np.array(utils.aslist(yy))
    ok = ~np.isnan(xx+yy)
    xx = qi.f.xtransform(xx[ok])
    yy = qi.f.ytransform(yy[ok])
    if rx is not None:
        if ry is None:
            ry = rx;
        extra = f" {rx} {ry}"
        if vert is not None:
            extra += f" {vert}"
    else:
        extra = ''
    
    qi.f.write(f'mark *{len(xx)} *{len(yy)}{extra}\n')
    qi.f.writedbl(xx)
    qi.f.writedbl(yy)
    qi.f.updaterange(xx, yy)

def mark(xx, yy):
    '''MARK - Draw on the current graph with the current marker
    MARK(xx, yy) draws marks at the given location in data space. 
    See also MARKER and PMARK, and XMARK and YMARK.'''
    _mark(xx, yy)


def xmark(xx, yy, rx, ry=None):
    '''XMARK - Like mark, but with horizontal collision avoidance
    XMARK(xx, yy, rx, ry) tries to draw marks at (XX, YY), but displaces marks
    horizontally in steps of RX points to avoid collision within an ellipse
    with radii RX and RY. (Leaving out RY uses a circle with radius RX.)'''
    _mark(xx, yy, rx, ry, 0)

    
def ymark(xx, yy, rx, ry=None):
    '''YMARK - Like mark, but with vertical collision avoidance
    YMARK(xx, yy, rx, ry) tries to draw marks at (XX, YY), but displaces marks
    vertically in steps of RX points to avoid collision within an ellipse
    with radii RX and RY. (Leaving out RY uses a circle with radius RX.)'''
    _mark(xx, yy, rx, ry, 1)

    
def bars(xx, yy, w=None, y0=0):
    '''BARS - Bar plot in data coordinates
    BARS(xx, yy, w) draws a bar graph of YY vs XX with bars
    of width W specified in data coordinates.
    BARS(xx, yy, w, y0) specifies a nonzero baseline of the plot.
    Y0 may also be a vector, which must be the same length as XX and YY. 
    This is useful for creating stacked bar graphs. Note that YY is never
    relative to Y0.
    If W is not given, it defaults to mean(diff(xx)).
    If the length of the XX vector is one greater than the length
    of the YY vector, the XX vector is taken to represent the edges
    of the bins.
    See also HBARS and SKYLINE.'''
    xx = np.array(xx).flatten()
    yy = np.array(yy).flatten()
    if utils.isnscalar(y0):
        y0=np.zeros(yy.shape) + y0

    if xx.size == yy.size:
        if w is None:
            w = np.mean(np.diff(xx))
        for k in range(yy.size):
            patch(np.array([-.5, .5, .5, -.5])*w + xx[k],
                  np.array([0, 0, 1, 1])*yy[k] + y0[k])
    elif xx.size == yy.size + 1:
        if w is None:
            for k in range(yy.size):
                patch(np.array([xx[k], xx[k+1], xx[k+1], xx[k]]),
                      np.array([0, 0, 1, 1])*yy[k] + y0[k])
        else:
            for k in range(yy.size):
                patch(np.array([-.5, .5, .5, -.5])*w + (xx[k]+xx[k+1])/2,
                      np.array([0, 0, 1, 1])*yy[k] + y0[k])
    else:
        raise ValueError('Inconsistent array sizes')


def hbars(yy, xx, h=None, x0=0):
    '''HBARS - Horizontal bar plot in data coordinates
    HBARS(yy, xx, h) draws a horizontal bar graph of data XX at YY with bars
    of width H (in the vertical direction), specified in data coordinates.
    HBARS(yy, xx, h, x0) specifies a nonzero baseline of the plot.
    X0 may also be a vector, which must be the same length as XX 
    and YY. This is useful for creating stacked bar graphs. Note that XX is
    never relative to X0.
    If H is not given, it defaults to mean(diff(yy)).
    If the length of the YY vector is one greater than the length
    of the XX vector, the YY vector is taken to represent the edges
    of the bins.'''
    xx = np.array(xx).flatten()
    yy = np.array(yy).flatten()
    if utils.isnscalar(x0):
        x0 = np.zeros(xx.shape) + x0

    if xx.size == yy.size:
        if h is None:
            h = np.mean(np.diff(yy))
        for k in range(xx.size):
            patch(np.array([0, 0, 1, 1]) * xx[k] + x0[k],
            np.array([-.5, .5, .5, -.5]) * h + yy[k])
    elif xx.size == yy.size - 1:
        if h is None:
            for k in range(xx.size):
                patch(np.array([0, 0, 1, 1]) * xx[k] + x0[k],
                np.array([yy[k], yy[k + 1], yy[k + 1], yy[k]]))
        else:
            for k in range(xx.size):
                patch(np.array([0, 0, 1, 1]) * xx[k] + x0[k],
                    np.array([-.5, .5, .5, -.5]) * h + (yy[k] + yy[k + 1]) / 2)

    else:
        raise ValueError('Inconsistent array sizes')
    

def ecoplot(x0, dx, yy, N=100):
    '''ECOPLOT - Economically plot large datasets
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
    '''ERRORBAR - Draw error bars
    ERRORBAR(xx, yy, dy) plots error bars at (XX, YY ± DY).
    Normally, XX, YY, and DY have the same shape. However, it is permissible
    for DY to be shaped Nx2, or for DY to be a 2-tuple, in which case
    lower and upper error bounds are different. (DY should always be positive).
    ERRORBAR(xx, yy, dy, w) adorns the error bars with horizontal lines of
    given width (W in points).
    ERRORBAR(..., 'up') only plots upward; ERRORBAR(..., 'down') only plots
    downward.
    See also ERRORPATCH and HERRORBAR'''

    N = len(xx)
    if type(dy)==tuple:
        dy_dn = -dy[0]
        dy_up = dy[1]
    elif np.prod(dy.shape)==2*N:
        dy_dn = -dy[:,0]
        dy_up = dy[:,1]
    else:
        dy_dn = -dy
        dy_up = dy

    if dir=='up':
        dy_dn = 0*dy_dn
    elif dir=='down':
        dy_up = 0*dy_up
    elif dir!='both':
        qi.error('Bad direction name')

    for n in range(N):
        plot(xx[n]+np.zeros(2), yy[n] + np.array([dy_dn[n], dy_up[n]]))
    
    if w is not None:
        if dir!='down':
            # Draw top ticks
            for n in range(N):
                markup.at(xx[n], yy[n] + dy_up[n])
                paper.line(np.array([-1, 1])*w/2, np.array([0, 0]))
        if dir!='up':
            # Draw down ticks
            for n in range(N):
                markup.at(xx[n], yy[n] + dy_dn[n])
                paper.line(np.array([-1, 1])*w/2, np.array([0, 0]))

                
def herrorbar(yy, xx, dx, w=None, dir='both'):
    '''HERRORBAR - Draw horizontal error bars
    HERRORBAR(yy, xx, dx) plots horizontal error bars at (XX ± DX, YY).
    Normally, YY, XX, and DX have the same shape. However, it is permissible
    for DX to be shaped Nx2, or for DX to be a 2-tuple, in which case
    lower and upper error bounds are different. (DX should always be positive).
    HERRORBAR(yy, xx, dx, w) adorns the error bars with vertical lines of
    given extent (W in points).
    HERRORBAR(..., 'left') only plots to the left; HERRORBAR(..., 'right')
    only plots to the right.'''

    N = len(xx)
    if type(dx)==tuple:
        dy_dn = -dx[0]
        dy_up = dx[1]
    elif np.prod(dx.shape)==2*N:
        dy_dn = -dx[:,0]
        dy_up = dx[:,1]
    else:
        dy_dn = -dx
        dy_up = dx

    if dir=='right':
        dy_dn = 0*dy_dn
    elif dir=='left':
        dy_up = 0*dy_up
    elif dir!='both':
        qi.error('Bad direction name')

    for n in range(N):
        plot(xx[n] + np.array([dy_dn[n], dy_up[n]]), yy[n]+np.zeros(2))
    
    if w is not None:
        if dir!='left':
            # Draw right ticks
            for n in range(N):
                markup.at(xx[n] + dy_up[n], yy[n])
                paper.line(np.array([0, 0]), np.array([-1, 1])*w/2)
        if dir!='left':
            # Draw down ticks
            for n in range(N):
                markup.at(xx[n] + dy_dn[n], yy[n])
                paper.line(np.array([0, 0]), np.array([-1, 1])*w/2)

                
def errorpatch(xx, yy, dy=None, dir='both'):
    '''ERRORPATCH - Draw error patch
    ERRORPATCH(xx, yy, dy) plots an error patch at (XX, YY ± DY).
    Normally, XX, YY, and DY all are N-vectors. 
    ERRORPATCH(..., 'up') only plots upward; ERRORPATCH(..., 'down') only 
    plots downward.
    To specify downward and upward errors separately,  DY may be shaped Nx2.
    DY must be positive, even for the downward error.
    
    ERRORPATCH(xx, yy), where YY is shaped Nx2, directly specifies the bounds
    as (XX, YY[:,0]) and (XX, YY[:,1]), much like matplotlib's fill_between.
    '''

    N = len(xx)
    if dy is None:
        yy_dn = yy[:,0]
        yy_up = yy[:,1]
    else:
        if len(dy.shape)==2:
            yy_dn = yy - dy[:,0]
            yy_up = yy + dy[:,1]
        else:
            yy_dn = yy - dy
            yy_up = yy + dy
        if dir=='up':
            yy_dn = yy
        elif dir=='down':
            yy_up = yy
        elif dir!='both':
            qi.error('Bad direction name')
    
    patch(np.concatenate((xx, np.flip(xx, 0))),
          np.concatenate((yy_dn, np.flip(yy_up, 0))))

def skyline(xx, yy, y0=0):
    '''SKYLINE - Skyline plot (bar plot)
    SKYLINE(xx, yy) draws a bar plot of YY vs XX with bars touching.
    SKYLINE(xx, yy, y0) specifies the baseline of the plot; default is 0.
    (Note that YY is not relative to Y0.)'''
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
        qi.f.write('caligraph *%i *%i *%i\n' %  (N, N, N))
        qi.f.writedbl(xx[iup[k]:idn[k]])
        qi.f.writedbl(yy[iup[k]:idn[k]])
        qi.f.writedbl(ww[iup[k]:idn[k]])
