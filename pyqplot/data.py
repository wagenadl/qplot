# Everything in the Plotting category

# plot
# patch

import numpy as np
import qi
import utils


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
