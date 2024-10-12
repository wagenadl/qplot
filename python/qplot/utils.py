import numpy as np
import os
import re

def alldigits(x):
    '''ALLDIGITS - True if a string contains only digits'''
    if alldigits.regex.match(x):
        return True
    else:
        return False
alldigits.regex = re.compile('^\d+$')

def isempty(x):
    if x is None:
        return True
    elif type(x)==list:
        return len(x)==0
    elif type(x)==str:
        return len(x)==0
    elif type(x)==np.array:
        return len(x)==0
    else:
        return False

def isnscalar(x):
    '''ISNSCALAR - True if array is a real numeric scalar.
  ISNSCALAR(x) returns True if X is a scalar numeric array, False if not.'''
    try:
        ok = float(x)
        return True
    except TypeError:
        return False

def isnvector(x):
    '''ISNVECTOR - True if array is a numeric vector of real numbers.
   ISNVECTOR(x) returns True if X is an 1xN or Nx1 numeric array, 
   False if not.'''
    # THIS MUST BE IMPROVED
    try:
        if isnscalar(x):
            return True
        ok = x+0
        if np.prod(x.shape) == x.size:
            return True
        else:
            return False
    except TypeError:
        return False

def unix(s):
    os.system(s)

def nonanstretch(xx):
    N = len(xx)
    isn = np.isnan(xx)
    iup = []
    idn = []
    state = False
    for n in range(N):
        if state:
            if isn[n]:
                idn.append(n)
                state = False
        else:
             if ~isn[n]:
                 iup.append(n)
                 state = True
    if state:
        idn.append(N)
    return (iup, idn)
    
def aslist(x):
    '''ASLIST - Convert almost anything to a list.
    y = ASLIST(x) puts scalar numbers in a list. It converts numpy
    arrays to one-dimensional as well. ASLIST does not change tuples to
    lists. It also does not change numpy arrays to lists.
    The result will have LEN defined and is indexible.'''
    if type(x)==list:
        return x
    elif type(x)==tuple:
        return x
    elif type(x)==np.ndarray:
        return np.reshape(x, x.size)
    else:
        return [x]

def arange(start, end, step=1):
    # See axes.py for docs
    rng = np.arange(start, end + step/1e10, step)
    rng[np.abs(rng) < step/1e10] = 0
    return rng


    
def sensiblestep(mx):
    '''dx = SENSIBLESTEP(mx) returns a sensible step size not much smaller
    than MX:

      1 ≤ MX < 2  ⇒  DX = 1
      2 ≤ MX < 5  ⇒  DX = 2
      5 ≤ MX < 10 ⇒  DX = 5
    etc.'''

    if mx <= 0:
        return 0
    lg = np.log10(mx)
    ordr = np.floor(lg)
    sub = 10**(lg - ordr)
    if sub > 5:
        sub = 5
    elif sub > 2:
        sub = 2
    else:
        sub = 1
    return sub * 10**ordr

def sensibleticks(xxx, cnt=5, inc=False):
    '''SENSIBLETICKS - Coordinates of sensible ticks
    tx = SENSIBLETICKS(xxx) returns approximately 5 ticks that
    span the range of the data XXX. The number is approximate, because
    the step size is always 1, 2, or 5 times some power of 10.
    Optional argument CNT overrides the approximate number.
    Optional argument INC, if True, makes the ticks extend past the data.
    (The default is for the ticks to not go beyond the data limits.)'''
    
    xd = np.array(xxx)
    if len(xd) == 0:
        return np.array([])
    x0 = np.min(xd)
    x1 = np.max(xd)
    rng = x1 - x0
    if rng <= 0:
        return np.array(x0)
    tx=[]
    scl=1
    while len(tx) < cnt:
        dx = sensiblestep(rng / scl)
        if inc:
            x0a = np.floor(x0/dx) * dx
        else:
            x0a = np.ceil(x0/dx) * dx
        if inc:
            x1a = np.ceil(x1/dx) * dx
        else:
            x1a = np.floor(x1/dx) * dx
        tx = arange(x0a, x1a, dx)
        scl = scl * 1.5
    return tx

def sampleminmax(xx, ii):
    '''SAMPLEMINMAX - Find minima and maxima in bins of sampled data
    y_min, y_max = SAMPLEMINMAX(xx,ii) finds the minima and the maxima
    of the data XX in the intervals [II₀, II₁), [II₁, II₂), ...,
    [IIₙ₋₁, IIₙ).
    Usage note: This is useful for things like plotting an electrode
    trace at just the resolution of the screen, without losing spikes.'''
    N = len(ii) - 1
    y_min = np.zeros(N)
    y_max = np.zeros(N)
    
    for n in range(N):
        i0 = ii[n]
        i1 = ii[n + 1]
        y_min[n] = np.min(xx[i0:i1])
        y_max[n] = np.max(xx[i0:i1])
    return y_min, y_max
