import numpy as np
import tempfile
import os
import re
import qplot_internal as q


def plot(xx, yy=None):
    '''PLOT - Draw a line series in data space
   PLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
   coordinates. See also LINE and GLINE.'''    if yy is None:
        yy = xx
        xx = range(len(yy))
    q.plot(xx, yy, 'plot')

def area(xx, yy):
    '''AREA - Draw a polygon in paper space
   AREA(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
   is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
   The polygon is filled with the current brush.
   XX and YY are given in postscript points. See also PATCH and GAREA.'''
    q.plot(xx, yy, 'area')

def patch(xx, yy):
    '''PATCH - Draw a polygonal patch in data space
   PATCH(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
   is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
   The polygon is filled with the current brush.
   XX and YY are given in data coordinates. See also AREA and GAREA.'''
    q.plot(xx, yy, 'patch')
    
def arrow(l=8, w=None, dl=0, dimple=0, dw=0):
    '''ARROW - Draw an arrowhead
  ARROW draws an arrow head pointing to the current anchor set by AT.
  ARROW(l, w) specifies length and (full) width of the arrow head
  These are specified in points, and default to L=8, W=5.
  ARROW(l, w, dl) specifies that the arrow is to be displaced from the
  anchor by a distance DL along the arrow's axis.
  ARROW(l, w, dl, dimple) specifies that the back of the arrow head is
  indented by DIMPLE points.
  ARROW(l, w, dl, dimple, dw) specifies that the arrow is to be displaced
  from the anchor by DW points in the orthogonal direction of the arrow's
  axis.'''
    if w is None:
        w = .6 * l
    area(np.array([0, -l, dimple-l, -l]) - dl,
          np.array([0, w, 0, -w])/2+dw)
    
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

def xlim(x0=None, x1=None):
    '''XLIM - Set x-axis limits
  XLIM(x0, x1) sets x-axis limits in the current panel.'''
    if x0 is None:
        q.error('Usage: xlim x0 x1')    
    if x1 is None:
        x1 = x0[1]
        x0 = x0[0]

    write('xlim %g %g\n' % (x0, x1))
    flush()

def ylim(y0=None, y1=None):
    '''YLIM - Set y-axis limits
  YLIM(y0, y1) sets y-axis limits in the current panel.'''
    if y0 is None:
        q.error('Usage: ylim y0 y1')    
    if y1 is None:
        y1 = y0[1]
        y0 = y0[0]

    write('ylim %g %g\n' % (y0, y1))
    flush()

def at(*args):
    '''AT - Specify location for future text
   AT(x, y) specifies that future text will be placed at data location (x,y)
   AT(x, y, phi) specifies that the text will be rotated by phi radians
   AT(x, y, dx, dy) specifies that the text will be rotated s.t. the baseline
   points in the data direction (dx,dy).
   AT(id, x, y) specifies coordinates in a specific subplots
   AT(id, x, y, phi) specifies coordinates in a specific subplots
   AT without arguments reverts to absolute placement relative to topleft.
   Either X or Y may also be nan (or '-') to have absolute placement in
   one dimension'''
    nargin = len(args)
    q.ensure()
    if nargin==0:
        write('at -\n')
    
    if nargin<1 or nargin>4:
        q.error('Cannot interpret arguments to AT')
    
    s = 'at'
    atcoord = np.zeros((nargin,)) + np.nan
    if type(args[0])==str and args[0]>='A' and args[0]<='Z':
        s += ' ' + args[0]
        if nargin>3:
            q.error('Cannot interpret AT arguments following ID')
        for k in range(1,nargin):
            a = args[k]
            if isnscalar(a):
                s += ' %g' % a
            else:
                q.error('Cannot interpret arguments following ID')
    else:
        if nargin<2:
            q.error('Cannot interpret arguments to AT')
        # at x y [dx dy]|[angle]|[ID]
        xtype = 'left right center abs absolute'.split()
        ytype = 'top bottom middle abs absolute'.split()
        for k in range(nargin):
            a = args[k]
            if nargin==3 and k==2 and type(a)==str and len(a)==1:
                s += ' ' + a
            elif isnscalar(a):
                s += ' %g' % a
                atcoord[k] = a
            elif k==0 and type(a)==str and a in xtype:
                s += ' ' + a
            elif k==1 and type(a)==str and a in type:
                s += ' ' + a
            elif k<2 and ((type(a)==str and a=='-')
                          or isnscalar(a) and np.isnan(a)):
                s += ' -'
            else:
                q.error('Cannot interpret arguments')
    write(s)
    q.figs[q.curfn].atcoord = atcoord

def axshift(pt=None):
    '''AXSHIFT - Specifies shift of drawn axis for XAXIS and YAXIS
   AXSHIFT(len) specifies shift (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = AXSHIFT returns current setting.'''
    fn = q.ensure()
    if q.isempty(pt):
        pt = q.figs[fn].axshift
    elif isnscalar(pt):
        q.figs[fn].axshift = pt
    else:
        q.error('AXSHIFT needs real number')
    return pt
    
def align(*args):
    '''ALIGN - Set alignment for following text
  ALIGN left|right|center|top|bottom|middle|base sets alignment for
  subsequent TEXT commands.'''
    allowed = 'left right center top bottom middle base'.split()
    usage = 'Usage: align ' + str.join('|', allowed) + ' ...'
    if q.isempty(args):
        q.error(usage)
    
    txt = 'align'
    for a in args:
        if a in allowed:
            txt += ' ' + a
        else:
            q.error(usage)

    write(txt + '\n')
    flush()

def bars(xx, yy, w, y0=0):
    '''BARS - Bar plot with bar width specified in data coordinates
   BARS(xx, yy, w) draws a bar graph of YY vs XX with bars
   of width W specified in data coordinates.
   BARS(xx, yy, w, y0) specifies the baseline of the plot;
   default for Y0 is 0. Y0 may also be a vector (which must
   then be the same size as XX and YY). This is useful for
   creating stacked bar graphs.'''

    if isnscalar(y0):
        y0=np.zeros(yy.shape) + y0
    
    for k in range(xx.size):
        patch(np.array([-.5, .5, .5, -.5])*w + xx[k],
               np.array([0, 0, 1, 1])*yy[k] + y0[k])

def brush(*args):
    '''BRUSH - Set brush for QPlot
   BRUSH id | color | 'none' | opacity  chooses or changes a brush for
   Plot. ID must be a single capital letter. COLOR may be a named color
   (i.e., one of krgbcmyw), or a 3-digit or a 6-digit string. 
   OPACITY must be a number between 0 and 1.'''
    first = True
    out = ['brush']
    for a in args:
        if type(a)==str:
            if len(a)==1 and a>='A' and a<='Z' and first:
                out.append(a) # This is ID, so good
            elif a=='none':
                out.append(a) # This is a known keyword, so good
            elif not q.isempty(q.mapcolor(a)):
                # This is a good color
                out.append(q.mapcolor(a))
            elif q.allnumeric(a):
                # This is a number
                if len(a)==3:
                    out.append('#%02x%02x%02x' % 
    	                       (int(255.999*int(a[0])/9),
    	                        int(255.999*int(a[1])/9), 
    	                        int(255.999*int(a[2])/9)))
                elif len(a)==6:
                    out.append('#%02x%02x%02x' % 
    	                       (int(255.999*int(a[0:2])/99), 
    	                        int(255.999*int(a[2:4])/99), 
    	                        int(255.999*int(a[4:6])/99)))
                else:
                    q.error('Cannot interpret argument for brush')
            else:
                q.error('Cannot interpret argument for brush')
        elif isnscalar(a):
            # This is opacity
            out.append('%g' % a)
        elif isnvector(a) and len(a)==3:
            out.append('##02x#02x#02x' %
    	               (int(255.999*a[0]),
    	                int(255.999*a[1]),
    	                int(255.999*a[2])))
        else:
            q.error('Cannot interpret argument for brush')
        first = False
    write(str.join(' ', out) + '\n')

def pen(*args):
    '''PEN - Selects a new pen for Plot
   PEN id | join | cap | pattern | color | width | -alpha | 'none'
   selects a new pen.
   ID must be a single capital letter
   JOIN must be one of: miterjoin beveljoin roundjoin
   CAP must be one of: flatcap squarecap roundcap
   PATTERN must be one of: solid dash dot none
      dash may optionally be followed by a vector of stroke and space lengths
      dot may optionally be followed by a vector of space lengths
   COLOR may be a single character matlab color, or a 3- or 6-digit RGB
   specification. 
   WIDTH is linewidth in points, or 0 for hairline.
   ALPHA specifies transparency between 0 and 1.'''
    out = [ 'pen' ]
    while args:
        a = args.pop(0);
        if type(a)==str:
            if len(a)==1 and a>='A' and a<='Z' and First:
                out.append(a)
            elif a in pen.joins or a in pen.caps or a in pen.style:
                out.append(a)
            elif a in pen.dashdot.split():
                out.append(a)
                vec = [ 3 ]
                if args and q.isnvector(a[0]):
                    vec = a.pop(0)
                out.append('[')
                for v in vec:
                    out.append('%g' % v)
                out.append(']')
            elif a in q.colormap:
                out.append(q.colormap[a])
            elif q.alldigits(a):
                # This is a number
                if len(a)==3:
                    out.append('#%02x%02%02x' % (int(255.999*int(a[0])/9),
                                                 int(255.999*int(a[1])/9),
                                                 int(255.999*int(a[2])/9)))
                elif len(a)==6:
    	            out.append('#%02x%02x%02x' % (int(255.999*int(a[0:2])/99),
                                                  int(255.999*int(a[2:4])/99),
                                                  int(255.999*int(a[4:6])/99)))
                else:
                    out.append(a) # This is pen width
            else:
                q.error([ 'Cannot interpret ' a ' as an argument for pen' ])
        elif q.isnscalar(a) && q.isreal(a):
            # This is a pen width
            out.append('%g' % a)
        elif q.isnvector(a) && q.isreal(a) && len(a)==3:
            # I AM WORKING HERE
            # This is a color
            cmd = [ cmd ' ' sprintf('##02x#02x#02x', ...
    	    floor(255.999*a))]
        else:
            q.error([ 'Cannot interpret ' disp(a) ' as an argument for pen' ])
        n=n+1
    
    fprintf(fd, '#s\n', cmd)
pen.joins = q.wordset('miterjoin beveljoin roundjoin')
pen.caps = q.wordset('flatcap squarecap roundcap')
pen.style = q.wordset('solid none')
pen.dashdot = q.wordset('dash dot')

def ytitlerot(pt=None):
    '''YTITLEROT - Specifies the rotation of y-axis titles.
   YTITLEROT(phi) specifies the rotation of y-axis titles, in degrees:
   phi=0 means upright,
   phi>0 means rotated 90 degrees to the left,
   phi<0 means rotated 90 degrees to the right.'''
    fn = q.ensure()
    if pt is None:
        pt = q.figs[fn].ytitlerot
    else:
        if not isnscalar(pt):
            q.error('ytitlerot must be a real scalar')
    
    q.figs[fn].ytitlerot = np.sign(pt)*np.pi/2
    
def title(ttl):
    '''TITLE - Render a title on the current QPlot
   TITLE(text) renders the given text centered along the top of the
   current QPlot figure.
   For more control over placement, use TEXT and friends.'''
    at()
    pid = q.figs[q.curfn].panel
    if pid=='-':
        xywh = q.figs[q.curfn].extent
    else:
        xywh = q.figs[q.curfn].panelextent[pid]
    
    align top center
    text(xywh(1) + xywh(3)/2, xywh(2) + 5, ttl)

def ticklen(pt=None):
    '''TICKLEN - Specifies length of ticks for XAXIS and YAXIS
   TICKLEN(len) specifies length of ticks (in points) for XAXIS and
   YAXIS. Positive means down or left, negative means up or right.
   pt = TICKLEN returns current setting.'''
    fn = q.ensure()
    if pt is None:
        pt = q.figs[fn].ticklen
    else:
        if not isnscalar(pt):
            q.error('ticklen must be a real scalar')
        q.figs[fn].ticklen = pt
    return pt
    
#======================================================================
if __name__ == '__main__':
    print('qplot test')
    figure('hello', 4, 3)
    plot([1,2,3,4], [1,3,2,4])
    
    brush('555')
    patch([1,2,1,1],[1,1,2,1])
