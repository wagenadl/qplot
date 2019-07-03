#!/usr/bin/python3

import sys
import os

ifn = sys.argv[1]
ofn = sys.argv[2]

print('runpyeg', ifn, ofn)

f = os.popen('ensurexvfb')
txt = f.read()
#os.environ['DISPLAY'] = txt.strip()
sys.path.insert(0, os.getcwd() + '/..')
with open(ifn) as f:
    txt = f.read()
    exec(txt)
    try:
        txt.index('shrink')
    except:
        qp.shrink(2)
    qp.save(ofn)
    qp.close()
