import numpy as np
import qplot_internal as qi
import core
import plots
import utils

class CBarInfo:
    clim = [0, 1]
    orient = 'x'
    xywh_d = [0,0,1,1]
    rev = False

class AxisInfo:
    orient='x'
    lim_d=None
    tick_d=None
    tick_p=None
    tick_lbl=None
    ttl=''
    ticklen=3
    lbldist=3
    ttldist=3
    coord_d=None
    coord_p=0
    ttlrot=0
    cbar=None

def axshift(pt=None):
    '''AXSHIFT - Specifies shift of drawn axis for XAXIS and YAXIS
   AXSHIFT(len) specifies shift (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = AXSHIFT returns current setting.'''
    qi.ensure()
    if qi.isempty(pt):
        pt = qi.curfig.axshift
    elif utils.isnscalar(pt):
        qi.curfig.axshift = pt
    else:
        qi.error('AXSHIFT needs real number')
    return pt

def textdist(lbl=None, ttl=None):
    '''TEXTDIST - Specifies distance to text labels for XAXIS and YAXIS
    QTEXTDIST(lbldist, ttldist) specifies distance between ticks and
    tick labels and between tick labels and axis title, in points.
    QTEXTDIST(dist) uses DIST for both distances.
    Positive numbers are to the left and down; negative numbers are to the
    right and up.
    (lbl, ttl) = TEXTDIST returns current settings.'''

    qi.ensure()
    
    if lbl is None:
        lbl = qi.curfig.textdist[0]
        ttl = qi.curfig.textdist[1]
    elif ttl is None:
        ttl = lbl
    qi.curfig.textdist = (lbl, ttl)
    return (lbl, ttl)
    
def ticklen(pt=None):
    '''TICKLEN - Specifies length of ticks for XAXIS and YAXIS
   TICKLEN(len) specifies length of ticks (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = TICKLEN returns current setting.'''
    qi.ensure()
    if pt is None:
        pt = qi.curfig.ticklen
    else:
        if not isnscalar(pt):
            qi.error('ticklen must be a real scalar')
        qi.curfig.ticklen = pt
    return pt


def q__axis(orient='x', lim_d=None, tick_d=None, tick_p=None,
            tick_lbl=None, ttl='',
            ticklen=3, lbldist=3, ttldist=3,
            coord_d=None, coord_p=0,
            ttlrot=0,
            cbar=None):
    '''Q__AXIS - Internal backend for axis rendering
    Q__AXIS(...) draws an axis according to the parameters:
      orient: 'x' or 'y'
      lim_d (2x1) limits of the axis in data coordinates (in the direction
                              of ORIENT)
      lim_p (2x1) shift of those limits in paper coordinates
      tick_d (Nx1) data coordinates (in the direction of ORIENT) of ticks
      tick_p (Nx1) shift of those coords in paper coordinates
      tick_lbl {Nx1} labels to be placed at those ticks
      ttl (string) title
      ticklen (scalar) length of ticks, +ve is down/right
      lbldist (scalar) dist b/w labels and axis/ticks, +ve is down/right
      ttldist (scalar) dist b/w title and labels/axis/ticks, +ve is down/right
      coord_d (scalar) position of the axis in data coords (in the direction
                                         orthogonal to ORIENT)
      coord_p (scalar) shift of that position in paper coordinates
      ttlrot (scalar) rotation of title: 0=normal +ve=CCW -ve=CW
          cbar (struct) optional reference to colorbar'''

    qi.ensure()
    qi.curfig.lastax = { 'orient': orient,
                      'lim_d': lim_d,
                      'tick_d': tick_d,
                      'tick_p': tick_p,
                      'tick_lbl': tick_lbl,
                      'ttl': ttl,
                      'ticklen': ticklen,
                      'lbldist': lbldist,
                      'ttldist': ttldist,
                      'coord_d': coord_d,
                      'coord_p': coord_p,
                      'ttlrot': ttlrot,
                      'cbar': cbar
    }
    
    if orient=='x':
        ishori=1
        isvert=0
    elif orient=='y':
        ishori=0
        isvert=1
    else:
        qi.error("orient must be 'x' or 'y'")    
    if isempty(lim_d):
        lim_d = np.zeros(lim_p.shape) + np.nan
    elif isempty(lim_p):
        lim_p = np.zeros(lim_d.shape)
        
    if isempty(tick_d):
        tick_d = np.zeros(tick_p.shape) + nan
    elif isempty(tick_p):
        tick_p = np.zeros(tick_d.shape)
        
    core.startgroup()
    
    tickdx = tick_d
    tickdy = np.zeros(tickdx.shape)+coord_d
    tickpx = tick_p
    tickpy = np.zeros(tickpx.shape)+coord_p
    ticklx = 0
    tickly = ticklen
    lbllx = 0
    lblly = lbldist
    
    if np.sign(tickly)==np.sign(lblly):
        lblly=lblly+tickly
        
    # Axis line position (x and y may be flipped later!)
    limdx = lim_d
    limdy = coord_d+np.zeros((2))
    limpx = lim_p
    limpy = coord_p+np.zeros((2))
    
    if not isempty(lim_d) and not np.isnan(lim_d[0]):
        ttldx = np.mean(limdx)
    elif not isempty(tick_d) and not isnan(tick_d[0]):
        ttldx = np.mean([tickdx[0], tickdx[-1]])
    else:
        ttldx = np.nan
        ttldy = coord_d
        
    if not isempty(lim_p):
        ttlpx = np.mean(limpx)
    elif not isempty(tick_p):
        ttlpx = np.mean([tickpx[0], tickpx[-1]])
    else:
        ttlpx = 0
        ttlpy = coord_p
        
    # Draw an axis line if desired
    if not isempty(lim_d):
        if isvert:
            (limdx, limdy) = (limdy, limdx)
            (limpx, limpy) = (limpy, limpx)
            gline(absdatax=limdx, absdatay=limdy,
                  relpaperx=limpx, relpapery=limpy)
            
    # Draw ticks if desired
    if isvert:
        (tickdx, tickdy) = (tickdy, tickdx)
        (tickpx, tickpy) = (tickpy, tickpx)
        (ticklx, tickly) = (tickly, ticklx)
        (lbllx, lblly)   = (lblly, lbllx)
    if ticklen!=0:
        for k in range(len(tickdx)):
            plots.gline([plots.AbsData(tickdx(k), tickdy(k)),
    	                 plots.RelPaper(tickpx(k), tickpy(k))],
                        [plots.AbsData(tickdx(k), tickdy(k)),
    	                 plots.RelPaper(tickpx(k)+ticklx, tickpy(k)+tickly)])
            
    # Draw labels if desired
    if ~isempty(tick_lbl):
        core.startgroup
        [xa, ya] = qpa_align(ishori, lbllx, lblly)
        qalign(xa, ya)
        if ishori:
            reftxt=''
            for k=1:length(tick_lbl):
                if str2double(tick_lbl{k}) < 0:
    	            tick_lbl{k} = [ tick_lbl{k} ' ' ]
                    reftxt = [ reftxt tick_lbl{k} ]
                    annotate.reftext(reftxt)
                    
        for k=1:length(tick_lbl):
            annotate.at(tickdx(k), tickdy(k))
            annotate.text(tickpx(k)+lbllx, tickpy(k)+lblly, tick_lbl{k})
            
        annotate.reftext('')
        core.endgroup()
        
    # Draw title if desired
    if not isempty(ttl):
        ttllx = 0
        ttlly = ttldist
        if isvert:
            (ttlpx, ttlpy) = (ttlpy, ttlpx)
            (ttllx, ttlly) = (ttlly, ttllx)
            (ttldx, ttldy) = (ttldy, ttldx)
            
    
        if utils.isempty(tick_lbl) or np.sign(ttldist)!=np.sign(lbldist):
            # Ignore labels when placing title: not on same side
            if np.sign(ttldist)==np.sign(ticklen):
                ttllx = ttllx + ticklx
                ttlly = ttlly + tickly
                annotate.at(ttldx, ttldy, -np.pi/2*np.sign(ttlrot))
        else:
            if ishori:
                ttlpy=0
            else:
                ttlpx=0
                [xa, ya] = qpa_align(ishori, -ttldist)
            if ishori:
                qat(ttldx, ya, -pi/2*sign(ttlrot))
            else:
                qat(xa, ttldy, -pi/2*sign(ttlrot))
        if ttlrot==0:
            [xa, ya] = qpa_align(ishori, ttldist)
        else:
            [xa, ya] = qpa_align(isvert, ttldist*sign(ttlrot))
            qalign(xa, ya)
        if ttlrot:
            qtext(-sign(ttlrot)*(ttlpy+ttlly), ...
    	          sign(ttlrot)*(ttlpx+ttllx), ttl)
        else:
            qtext(ttlpx+ttllx, ttlpy+ttlly, ttl)
            qendgroup


def xaxis(y0=None, lim=None, ticks=None, labels=None, title='', flip=False):
    '''XAXIS - Draw x-axis
    All arguments are optional.
      Y0 specifies intersect with y-axis.
      LIM specifies left and right edges as a tuple or list. If None,
        LIM is determined from TICKS. If [], no line is drawn.
      TICKS specifies positions of ticks along axis.
      LABELS specifies labels to put by ticks. If None, tick coordinates
        are used. If [], no labels are drawn.
      TITLE specifies title for axis.
      FLIP, if True, specifies that labels and ticks go in opposite direction.'''
    if y0 is None:
        yy = qi.sensibleticks(qi.curfig.datarange[2:4], 1)
        y0 = yy[0]
    if ticks is None:
        ticks = qi.sensibleticks(qi.curfig.datarange[0:2], inc=True)
    if lim is None:
        lim = [ticks[0], ticks[-1]]
    if labels is None:
        labels = qi.format(ticks) 
    ticklen = ticklen()
    axshift = axshift()
    [lbldist, ttldist] = textdist()
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
    
    qi.axis(orient='x', lim_d=lim, tick_d=ticks, tick_lbl=labels, ttl=title, \
            ticklen=ticklen, lbldist=lbldist, ttldist=ttldist, \
            coord_d=y0, coord_p=axshift)
