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

def wordset(s):
    '''WORDSET splits a string up at spaces and returns a dict pointing
each word to 1.'''
    return { k: 1 for k in s.split() }

def unix(s):
    os.system(s)

def schmitt(xx):
    N = len(xx)
    iup = []
    idn = []
    state = False
    for n in range(N):
        if state:
            if not(xx[n]):
                idn.append(n)
                state = False
        else:
             if xx[n]:
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
    elif type(x)==np.array:
        return np.reshape(x, x.size)
    else:
        return [x]

def sensiblestep(mx):
    '''dx = SENSIBLESTEP(mx) returns a sensible step size not much smaller
    than MX:

      1<=MX<2  -> DX=1
      2<=MX<5  -> DX=2
      5<=MX<10 -> DX=5
    etc.'''
    
    lg=np.log10(mx)
    ord=np.floor(lg)
    sub = 10**(lg-ord)
    if sub>5:
        sub=5
    elif sub>2:
        sub=2
    else:
        sub=1
    return sub * 10**ord

def sensibleticks(xxx, cnt=5, inc=False):
    '''SENSIBLETICKS - Coordinates of sensible ticks
    tx = SENSIBLETICKS(xxx) returns approx. 5 ticks that span the range of  
    the data XXX.
    Optional argument CNT overrides the approx. number.
    Optional argument INC, if True, makes the ticks extend past the data. (The
    default is for the ticks to not go beyond the data limits.)'''
    xd = np.array(xxx)
    x0 = np.min(xd)
    x1 = np.max(xd)
    rng = x1 - x0
    tx=[]
    scl=1
    while len(tx)<cnt:
        dx = sensiblestep(rng/scl)
        if inc:
            x0a = np.floor(x0/dx)*dx
        else:
            x0a = np.ceil(x0/dx)*dx
        if inc:
            x1a = np.ceil(x1/dx)*dx
        else:
            x1a = np.floor(x1/dx)*dx
        print(x0a, x1a, dx)
        tx = np.arange(x0a, x1a+dx/2, dx)
        scl = scl*1.5
    return tx

def sampleminmax(xx, ii):
    '''SAMPLEMINMAX - Find minima and maxima in bins of sampled data
   y_min, y_max = SAMPLEMINMAX(xx,ii) finds the minima and the maxima
   of the data XX in the intervals [ii_0,ii_1), [ii_1,ii_2), ...,
   [ii_n-1,ii_n).
   Usage note: This is useful for plotting an electrode trace at just
   the resolution of the screen, without losing spikes.'''
    N=len(ii)-1
    y_min=np.zeros(N)
    y_max=np.zeros(N)
    
    for n in range(N):
        y_min[n] = np.min(xx[ii[n]:ii[n+1]])
        y_max[n] = np.max(xx[ii[n]:ii[n+1]])
    return y_min, y_max

def mm(f=1):
    '''MM - Convert postscript points to millimeters
    Use as in 5*mm() or as in mm(5).'''
    return 72 * f / 25.4
