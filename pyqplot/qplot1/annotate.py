import numpy as np
import qplot_internal as qi
import core

def arrow(l=8, w=None, dl=0, dimple=0, dw=0):
    '''ARROW - Draw an arrowhead
    ARROW draws an arrow head pointing to the current anchor set by AT.
    ARROW(l, w) specifies length and (full) width of the arrow head
    These are specified in points, and default to L=8, W=5.
    Optional arguments:
      DL - specifies that the arrow is to be displaced from the
           anchor by a distance DL along the arrow's axis.
      DIMPLE - specifies that the back of the arrow head is
           indented by DIMPLE points.
      DW - specifies that the arrow is to be displaced from the anchor 
           by DW points in the orthogonal direction of the arrow's
           axis.'''
    if w is None:
        w = .6 * l
    basics.area(np.array([0, -l, dimple-l, -l]) - dl,
                np.array([0, w, 0, -w])/2+dw)
    

def at(x=None, y=None, phi=None, along=None, id=None):
    '''AT - Specify location for future text
    AT(x, y) specifies that future text will be placed at data location (x,y)
    Optional arguments:
      PHI - specifies that the text will be rotated by phi radians.
      ALONG - must be a tuple (dx,dy), meaning that the text will be
            rotated s.t. the baseline points in the data direction (dx,dy).
      ID - coordinates are specified relative to a subplot
    X may also be one of 'left,' 'right,' 'center,' 'abs,' 'absolute.'
    Y may also be one of 'top,' 'bottom,' 'middle,' 'abs,' 'absolute.'
    If X and/or Y is omitted, placements reverts to absolute in those
    dimensions.
    '''
    qi.ensure()
    qi.curfig.atx = None
    qi.curfig.aty = None
    if x is None and y is None:
        qi.write('at -\n')
        return
    cmd = ['at']
    if id is not None:
        cmd.append(id)
    if type(x)==str:
        if x in at.xtype:
            cmd.append(x)
        else:
            qi.error('Bad specification for x')
    else:
        cmd.append('%g' % x)
        qi.curfig.atx = x
    if type(y)==str:
        if y in at.ytype:
            cmd.append(y)
        else:
            qi.error('Bad specification for y')
    else:
        cmd.append('%g' % y)
        qi.curfig.aty = y
    if phi is not None:
        cmd.append('%g' % phi)
    elif along is not None:
        cmd.append('%g %g' % (along[0], along[1]))
    qi.write(' '.join(cmd))
    
at.xtype = qi.wordset('left right center abs absolute')
at.ytype = qi.wordset('top bottom middle abs absolute')

    
def align(*args):
    '''ALIGN - Set alignment for following text
  ALIGN left|right|center|top|bottom|middle|base sets alignment for
  subsequent TEXT commands.'''
    allowed = 'left right center top bottom middle base'.split()
    usage = 'Usage: align ' + str.join('|', allowed) + ' ...'
    if qi.isempty(args):
        qi.error(usage)
    
    txt = 'align'
    for a in args:
        if a in allowed:
            txt += ' ' + a
        else:
            qi.error(usage)

    qi.write(txt + '\n')
    qi.flush()

def ytitlerot(pt=None):
    '''YTITLEROT - Specifies the rotation of y-axis titles.
   YTITLEROT(phi) specifies the rotation of y-axis titles, in degrees:
   phi=0 means upright,
   phi>0 means rotated 90 degrees to the left,
   phi<0 means rotated 90 degrees to the right.'''
    qi.ensure()
    if pt is None:
        pt = qi.curfig.ytitlerot
    else:
        if not isnscalar(pt):
            qi.error('ytitlerot must be a real scalar')
    
    qi.curfig.ytitlerot = np.sign(pt)*np.pi/2
    
def title(ttl):
    '''TITLE - Render a title on the current QPlot
   TITLE(text) renders the given text centered along the top of the
   current QPlot figure.
   For more control over placement, use TEXT and friends.'''
    at()
    pid = qi.curfig.panel
    if pid=='-':
        xywh = qi.curfig.extent
    else:
        xywh = qi.curfig.panelextent[pid]
    align('top', 'center')
    text(xywh(1) + xywh(3)/2, xywh(2) + 5, ttl)
    
