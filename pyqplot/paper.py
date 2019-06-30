# Everything in the Paper coordinate plotting

# line
# area

import qi

# A GLC is a tuple (cmd, arg) or (cmd, arg, arg2).
# A PTSPEC is a list of GLCS.
def q__gline(cmd='gline', ptspecs=[]):
    out = [cmd]
    for pt in ptspecs:
        out.append('(')
        for glc in pt:
            out.append(glc[0])
            if type(glc[1])==str:
                out.append(glc[1])
            else:
                out.append('%g' % glc[1])
            if len(glc)>=3:
                out.append('%g' % glc[2])
        out.append(')')
    qi.write(out)

# A VGLC is a GLC where each arg may be a vector
def q__gline2(cmd='gline', vglcs=[]):
    N = None
    for vgl in vglcs:
        a1 = aslist(vgl[1])
        n = len(a1)
        if N is None:
            N = n
        elif n>1 and n!=N:
            error('Mismatching point count')
    if N is None:
        return
    pts = []
    for n in range(N):
        pts.append([])
    for vgl in vglcs:
        a1 = aslist(vgl[1])
        n = len(a1)
        if len(vgl)>=3:
            a2 = aslist(vgl[2])
        else:
            a2 = None
        if n==1:
            a1 = a1[0]
            if a2 is None:
                for n in range(N):
                    pts[n].append((vgl[0], a1))
            else:
                a2 = a2[0]
                for n in range(N):
                    pts[n].append((vgl[0], a1, a2))
        else:
            if a2 is None:
                for n in range(N):
                    pts[n].append((vgl[0], a1[n]))
            else:
                for n in range(N):
                    pts[n].append((vgl[0], a1[n], a2[n]))
    q__gline(cmd, pts)

def line(xx, yy):
    '''LINE - Draw a line series in paper space
    LINE(xx, yy) draws a line series between the points (XX,YY).
    XX and YY are given in postscript points. See also PLOT and GLINE.'''
    qi.plot(xx, yy, cmd='line')

def area(xx, yy):
    '''AREA - Draw a polygon in paper space
    AREA(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
    The polygon is filled with the current brush.
    XX and YY are given in postscript points. See also PATCH and GAREA.'''
    qi.plot(xx, yy, cmd='area')
