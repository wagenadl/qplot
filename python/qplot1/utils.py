import numpy as np
import os

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
    
