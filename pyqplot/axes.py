# Everything in the Tick axes and Tick axis styling categories.
# Also the Color bars category.

# axshift
# textdist
# ticklen
# xaxis
# yaxis
# ytitlerot
# caxis
# overline
# xcaxis
# numformat
# overlinedist
# overlinemin

from . import qi
from . import style
from . import paper
from . import markup
from . import fig

def ytitlerot(pt=None):
    '''YTITLEROT - Specifies the rotation of y-axis titles.
    YTITLEROT(phi) specifies the rotation of y-axis titles, in degrees:
    phi=0 means upright,
    phi>0 means rotated 90 degrees to the left,
    phi<0 means rotated 90 degrees to the right.
    phi = YTITLEROT() returns current value.'''
    qi.ensure()
    if pt is None:
        pt = qi.f.ytitlerot
    else:
        qi.f.ytitlerot = np.sign(pt)*np.pi/2
    return pt


def axshift(pt=None):
    '''AXSHIFT - Specifies shift of drawn axis for XAXIS and YAXIS
   AXSHIFT(len) specifies shift (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = AXSHIFT returns current setting.'''
    qi.ensure()
    if pt is None:
        pt = qi.f.axshift
    elif utils.isnscalar(pt):
        qi.f.axshift = pt
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
        lbl = qi.f.textdist[0]
        ttl = qi.f.textdist[1]
    elif ttl is None:
        ttl = lbl
    qi.f.textdist = (lbl, ttl)
    return (lbl, ttl)
    
def ticklen(pt=None):
    '''TICKLEN - Specifies length of ticks for XAXIS and YAXIS
   TICKLEN(len) specifies length of ticks (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = TICKLEN returns current setting.'''
    qi.ensure()
    if pt is None:
        pt = qi.f.ticklen
    else:
        if not isnscalar(pt):
            qi.error('ticklen must be a real scalar')
        qi.f.ticklen = pt
    return pt

def qpa__align(hori, dx, dy=None):
    if dy is None:
        dy = dx
    xa = 'center';
    ya = 'middle';
    if hori:
        if dy>0:
            ya = 'top';
        else:
            ya = 'bottom';
    else:
        if dx>0:
            xa = 'left';
        else:
            xa = 'right';
    return (xa, ya)

def q__axis(orient='x', lim_d=None,
            tick_d=None, tick_p=None,
            tick_lbl=None, ttl='',
            ticklen=3, lbldist=3, ttldist=3,
            coord_d=None, coord_p=0,
            ttlrot=0,
            cbar=None):
    '''Q__AXIS - Internal backend for axis rendering
    Q__AXIS(...) draws an axis according to the parameters:
      orient: 'x' or 'y'
      lim_d (2) limits of the axis in data coordinates (in the direction
                of ORIENT)
      tick_d (N) data coordinates (in the direction of ORIENT) of ticks
      tick_p (N) shift of those coords in paper coordinates
      tick_lbl (N strings) labels to be placed at those ticks
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
    qi.f.lastax = { 'orient': orient,
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
                    'cbar': cbar }
    
    if orient=='x':
        ishori=1
        isvert=0
    elif orient=='y':
        ishori=0
        isvert=1
    else:
        qi.error("orient must be 'x' or 'y'")    

    if type(tick_d)==function:
        tick_d = np.array([ tick_d(lbl) for lbl in tick_lbl])
    if tick_d is None:
        tick_d = np.zeros(tick_p.shape) + np.nan
    elif tick_p is None:
        tick_p = np.zeros(tick_d.shape)
        
    fig.startgroup()
    
    tickdx = tick_d
    tickdy = np.zeros(tickdx.shape) + coord_d
    tickpx = tick_p
    tickpy = np.zeros(tickpx.shape) + coord_p
    ticklx = 0
    tickly = ticklen
    lbllx = 0
    lblly = lbldist
    
    if np.sign(tickly)==np.sign(lblly):
        lblly = lblly + tickly
        
    # Axis line position (x and y may be flipped later!)
    limdx = lim_d
    limdy = coord_d + np.zeros((2))
    limpx = np.zeros((2))
    limpy = coord_p + np.zeros((2))
    
    if lim_d is not None:
        ttldx = np.mean(limdx)
    elif tick_d is not None:
        ttldx = np.mean([tickdx[0], tickdx[-1]])
    else:
        ttldx = np.nan
        ttldy = coord_d
        
    if tick_p is not None:
        ttlpx = np.mean([tickpx[0], tickpx[-1]])
    else:
        ttlpx = 0
        ttlpy = coord_p
        
    # Draw an axis line if desired
    if lim_d is not None:
        if isvert:
            (limdx, limdy) = (limdy, limdx)
            (limpx, limpy) = (limpy, limpx)
        paper.gline2([paper.AbsData(limdx, limdy),
                      paper.RelPaper(limpx, limpy)])
            
    # Draw ticks if desired
    if isvert:
        (tickdx, tickdy) = (tickdy, tickdx)
        (tickpx, tickpy) = (tickpy, tickpx)
        (ticklx, tickly) = (tickly, ticklx)
        (lbllx, lblly)   = (lblly, lbllx)
    if ticklen!=0:
        for k in range(len(tickdx)):
            paper.gline([paper.AbsData(tickdx(k), tickdy(k)),
    	                 paper.RelPaper(tickpx(k), tickpy(k))],
                        [paper.AbsData(tickdx(k), tickdy(k)),
    	                 paper.RelPaper(tickpx(k)+ticklx, tickpy(k)+tickly)])
            
    # Draw labels if desired
    if type(tick_lbl)==function:
        tick_lbl = [ tick_lbl(x) for x in tick_d ]
    if not utils.isEmpty(tick_lbl):
        fig.startgroup()
        [xa, ya] = qpa__align(ishori, lbllx, lblly)
        markup.align(xa, ya)
        if ishori:
            reftxt=''
            for lbl in tick_lbl:
                if type(lbl)!=str:
                    lbl = qi.f.numfmt % lbl
                reftxt += lbl
                try:
                    v = float(lbl)
                    if v<0:
                        reftxt += ' '
                except:
                    pass
            markup.reftext(reftxt)
                    
        for k in range(len(tick_lbl)):
            markup.at(tickdx[k], tickdy[k])
            lbl = tick_lbl[k]
            if type(lbl)!=str:
                lbl = qi.f.numfmt % lbl
            markup.text(lbl, dx=tickpx[k] + lbllx, dy=tickpy[k] + lblly)
            
        markup.reftext('')
        fig.endgroup()
        
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
            markup.at(ttldx, ttldy, phi=-np.pi/2*np.sign(ttlrot))
        else:
            if ishori:
                ttlpy = 0
            else:
                ttlpx = 0
                [xa, ya] = qpa__align(ishori, -ttldist)
            if ishori:
                markup.at(ttldx, ya, phi=-pi/2*sign(ttlrot))
            else:
                markup.at(xa, ttldy, phi=-pi/2*sign(ttlrot))
        if ttlrot==0:
            xa, ya = qpa__align(ishori, ttldist)
        else:
            xa, ya = qpa__align(isvert, ttldist*sign(ttlrot))
            align(xa, ya)
        if ttlrot:
            text(ttl,
                 dx=-np.sign(ttlrot)*(ttlpy+ttlly), 
    	         dy=np.sign(ttlrot)*(ttlpx+ttllx))
        else:
            text(txt, dx=ttlpx + ttllx, dy=ttlpy + ttlly)
    fig.endgroup()

def xaxis(y0=None, ticks=None, labels=None, title='', lim=None, flip=False):
    '''XAXIS - Draw x-axis
    All arguments are optional.
      Y0 specifies intersect with y-axis. If None, defaults to a reasonable
        position below the data.
      TICKS specifies positions of ticks along axis. If None, ticks are 
        inferred using SENSIBLETICKS. If [], no ticks are drawn.
      LABELS specifies labels to put by ticks. If None, tick coordinates
        are used. If [], no labels are drawn.
      TITLE specifies title for axis.
      LIM specifies left and right edges as a tuple or list. If None,
        LIM is determined from TICKS. If [], no line is drawn.
      FLIP, if True, inverts the sign of the settings from TICKLEN, TEXTDIST,
        and AXSHIFT.
    Either TICKS or LABELS (but not both) may be a function, in which case
    the labels are calculated from the tick positions (or vice versa). For
    example:

      XAXIS(0, lambda x: x/100, np.arange(0,101,25), 'Value (%)')

    Without any arguments or with just a title as an argument, XAXIS tries
    to determine sensible defaults based on previous calls to PLOT and
    friends. Your mileage may vary.'''
    qi.ensure()
    if y0 is None:
        yy = qi.sensibleticks(qi.f.datarange[2:4], 1)
        y0 = yy[0]
    if ticks is None:
        ticks = qi.sensibleticks(qi.f.datarange[0:2], inc=True)
    if lim is None:
        lim = [ticks[0], ticks[-1]]
    if labels is None:
        labels = qi.format(ticks) 
    ticklen = qi.f.ticklen
    axshift = qi.f.axshift
    [lbldist, ttldist] = textdist()
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
    
    q__axis(orient='x', lim_d=lim, tick_d=ticks, tick_lbl=labels, ttl=title, 
            ticklen=ticklen, lbldist=lbldist, ttldist=ttldist, 
            coord_d=y0, coord_p=axshift)

def yaxis(x0=None, lim=None, ticks=None, labels=None, title='', flip=False):
    '''YAXIS - Draw y-axis
    All arguments are optional.
      X0 specifies intersect with x-axis. If None, defaults to a reasonable
        position to the left of the data.
      LIM specifies bottom and top edges as a tuple or list. If None,
        LIM is determined from TICKS. If [], no line is drawn.
      TICKS specifies positions of ticks along axis. If None, ticks are 
        inferred using SENSIBLETICKS. If [], no ticks are drawn.
      LABELS specifies labels to put by ticks. If None, tick coordinates
        are used. If [], no labels are drawn.
      TITLE specifies title for axis.
      FLIP, if nonzero, inverts the sign of the settings from TICKLEN, TEXTDIST,
        and AXSHIFT. If FLIP=2, the title is flipped as well.
    Either TICKS or LABELS (but not both) may be a function, in which case
    the labels are calculated from the tick positions (or vice versa). For
    example:

      YAXIS(0, lambda y: y/100, np.arange(0,101,25), 'Value (%)')

    Without any arguments or with just a title as an argument, YAXIS tries
    to determine sensible defaults based on previous calls to PLOT and
    friends. Your mileage may vary.'''
    qi.ensure()
    if x0 is None:
        xx = qi.sensibleticks(qi.f.datarange[0:2], 1)
        x0 = xx[0]
    if ticks is None:
        ticks = qi.sensibleticks(qi.f.datarange[2:4], inc=True)
    if lim is None:
        lim = [ticks[0], ticks[-1]]
    if labels is None:
        labels = qi.format(ticks) 
    ticklen = ticklen()
    axshift = axshift()
    [lbldist, ttldist] = textdist()
    lblrot = ytitlerot()
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
        if flip==2:
            lblrot = -lblrot
    
    qi.axis(orient='y', lim_d=lim, tick_d=ticks, tick_lbl=labels, ttl=title, 
            ticklen=ticklen, lbldist=lbldist, ttldist=ttldist, 
            coord_d=x0, coord_p=axshift, ttlrot=lblrot)

def minorticks(xx, ticklen=None):
    '''MINORTICKS - Add more ticks to an existing axis
    MINORTICK(xx, ticklen) adds minor ticks at XX. Must be called after a 
    call to XAXIS or YAXIS. Typically, you'd set TICKLEN to a smaller value
    than what was used for the major ticks. Defaults to 2/3 of the figure's
    TICKLEN setting.'''
    
    qi.ensure()
    if qi.f.lastax is None:
        qi.error('No previous axis')
    
    kv = qdata.figs[fn].lastax
    if ticklen is None:
        ticklen = qi.f.ticklen * 2./3
    #if strcmp(kv.orient,'y'):
    #    kv.ticklen = -kv.ticklen # What is this about??
    if kv['cbar'] is not None:
        kv['cbar'].ctodat(kv['tick_d'])
    q__axis(orient=kv['orient'], tick_d=xx, tick_lbl=[], ticklen=ticklen,
            coord_d=kv['coord_d'], coord_p=kv['coord_p'])

def caxis(ticks=None, labels=None, title=None, lim=None, flip=False):
    '''CAXIS - Plot colorbar axis
    CAXIS plots a colorbar axis alongside the most recent CBAR or HCBAR.
    All arguments are optional.
      TICKS specifies the locations of the ticks in terms of the data
        represented in the IMSC for which the colorbar was drawn.
      LABELS specifies labels to be written by those ticks. If None, 
        labels are derived from TICKS. If [], no labels are written.
      TITLE specifies a title for the axis.
      LIM specifies the ends of the axis, again in terms of the data
        represented in the IMSC.
      FLIP specifies that the axis is rendered to the left or above the
        bar rather than to the right or below.

    CAXIS interprets settings from TICKLEN, TEXTDIST, and AXSHIFT
    differently from XAXIS and YAXIS: positive values are away from
    the colorbar.  Note that MINORTICKS currently doesn't understand
    about this convention, so MINORTICKS may produce unexpected
    results when used with CAXIS.'''

    qi.ensure()
    cb = qi.f.cbar
    if cb is None:
        qi.error('CAXIS needs a previous CBAR or HCBAR')
    if lim is None:
        lim = cb.lim
    if ticks is None:
        ticks = utils.sensibleticks(clim)
    if labels is None:
        labels = ticks

    ticklen = qi.f.ticklen
    (lbldist, ttldist) = textdist()

    if cb.orient=='y':
        ttlrot = ytitlerot()
        coord_d = cb.drect[0]
        coord_p = cb.prect[0]
        if flip:
            ticklen = -ticklen
            ttlrot = -ttlrot
            coord_p -= axshift()
        else:
            coord_p += cb.prect[2] + axshift()
    elif cb.orient=='x':
        ttlrot = 0
        coord_d = cb.drect[1]
        coord_p = cb.prect[1]
        if flip:
            ticklen = -ticklen
            coord_p -= axshift()
        else:
            coord_p += cb.prect[3] + axshift()
    else:
        qi.error('Orientation not understood')

    qi.axis(orient=cb.orient, lim_d=lim, tick_d=ticks, tick_lbl=labels,
            ttl=title, 
            ticklen=ticklen, lbldist=lbldist, ttldist=ttldist, 
            coord_d=coord_d, coord_p=coordp, ttlrot=ttlrot)
        
def numformat(fmt=None):
    '''NUMFORMAT - Specifies the format of numbers as tick labels
    NUMFORMAT(fmt) specifies the format of numeric axis tick labels.
    FMT may be anything that python's "%" operator understands,
    for instance: "%.1f". The default is "%g".
    fmt = NUMFORMAT() returns current setting.'''
    qi.ensure()
    if fmt is not None:
        qi.f.numfmt = fmt
    return qi.f.numfmt

def overlinedist(x=None):
    '''OVERLINEDIST - Specifies distance between OVERLINEs and data
    OVERLINEDIST(dist) specifies the distance between OVERLINEs and 
    the data, in points.
    dist = OVERLINEDIST() returns current settings.'''
    qi.ensure()
    if x is not None:
        qi.f.overlinedist = np.abs(x)
    return qi.f.overlinedist
    
def overlinemin(x=None):
    '''OVERLINEMIN - Specifies minimum vertical length of OVERLINEs
    OVERLINEMIN(h) specifies the minimum vertical length of OVERLINEs,
    in points.
    h = OVERLINEMIN() returns current settings.'''
    qi.ensure()
    if x is not None:
        qi.f.overlinemin = x
    return qi.f.overlinemin

def overline(xx, yy, txt=None, datadist=None, textdist=None, minlen=None):
    '''OVERLINE - Draw a line above data with a text above it
    OVERLINE(xx, y, text), where XX is a 2-vector and Y a scalar, draws
    a horizontal line just above (XX(1), Y) to (XX(2), Y) and places the
    given TEXT over it.
    OVERLINE(xx, yy, text), where both XX and YY are 2-vectors, draws the
    line just above the larger YY value and extends a vertical line down 
    to the smaller YY value.
    The whole thing is displaced by a distance OVERLINEDIST from the data,
    and the text placement uses the absolute value of TEXTDIST.
    If OVERLINEMIN is non-zero, a vertical line is drawn on both ends.
    OVERLINE(xx, y) or QOVERLINE(xx, yy) is permitted: no text is drawn.
    Optional arguments DATADIST, TEXTDIST, and MINLEN override global
    settings.'''
    qi.ensure()
    if datadist is None:
        datadist = qi.f.overlinedist
    if textdist is None:
        textdist = qi.f.textdist[0]
    if minlen is None:
        minlen = qi.f.overlinemin
    yy = np.array(utils.aslist(yy))
    ymax = np.max(yy)
    if len(yy)==2:
        paper.shiftedline(np.array([xx[0], xx[0], xx[1], xx[1]]),
                          np.array([yy[0], ymax, ymax, yy[1]]),
                          np.array([0,0,0,0]),
                          -np.array([datadist,
                                    datadist + minlen,
                                    datadist + minlen,
                                    datadist]))
    elif minlen>0:
        paper.shiftedline(np.array([xx[0], xx[0], xx[1], xx[1]]),
                          np.array([ymax, ymax, ymax, ymax]),
                          np.array([0,0,0,0]),
                          -np.array([datadist,
                                    datadist + minlen,
                                    datadist + minlen,
                                    datadist]))
    else:
        paper.shiftedline(np.array([xx[0], xx[1]]),
                          np.array([ymax, ymax]),
                          np.array([0,0]),
                          -np.array([datadist + minlen,
                                    datadist + minlen]))
    
    if txt is not None:
        markup.at((xx[0]+xx[1])/2, ymax)
        td = np.abs(textdist)
        markup.align('center', 'bottom')
        markup.text(txt, dy=-(datadist + minlen + td))

def xcaxis(y0=None, xx=None, labels=None, title='', lim=None, flip=False):
    '''XCAXIS - Plot x-axis with labels between ticks
    XCAXIS(y0, xx, labels) places labels XL at locations XX, but places
    ticks between labels rather than at the labels. First and last ticks
    are extrapolated.
    Optional argument TITLE specifies title to the axis.
    Optional argument LIM specifies those end ticks explicitly as a 2-ple.
    XCAXIS obeys settings from TICKLEN, TEXTDIST, and AXSHIFT.'''
    qi.ensure()
    if y0 is None:
        yy = qi.sensibleticks(qi.f.datarange[2:4], 1)
        y0 = yy[0]
    ticklen = qi.f.ticklen
    axshift = qi.f.axshift
    [lbldist, ttldist] = textdist()
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
    
    btwnx = (xx[0:-1] + xx[1:])/2
    if lim is None:
        avg = np.mean(np.diff(btwnx))
        lim = (btwnx[0]-avg, btwnx[-1]+avg)
    tickx = np.concatenate(([lim[0]], btwnx, [lim[1]]))

    # Place labels, do not draw bar
    q__axis(orient='x', tick_d=xx, tick_lbl=labels, ttl=title,
            ticklen=0, lbldisl=lbldist+ticklen, ttldist=ttldist,
            coord_d=y0, coord_p=axshift)
    # Place ticks, draw bar
    q__axis(orient='x', tick_d=tickx, tick_lbl='',
            ticklen=ticklen,
            coord_d=y0, coord_p=axshift)
    