# Everything in the Tick axes and Tick axis styling categories.
# Also the Color bars category.

# ytitlerot

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


    
