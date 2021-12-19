#!/usr/bin/python3

import sys
import os
import time
ifn = sys.argv[1]
ofn = sys.argv[2]
ofn, ext = os.path.splitext(ofn)

print('runpyeg', ifn, ofn)

f = os.popen('ensurexvfb')
txt = f.read()
os.environ['DISPLAY'] = txt.strip()
sys.path.insert(0, os.getcwd() + '/..')
with open(ifn) as f:
    txt = f.read()
    exec(txt)
    if qp.qi.f:
        if txt.find('shrink')<0:
            qp.shrink(2)
        qp.save(ofn + '.png', reso=100)
        qp.save(ofn + '.pdf')
        qp.close()
    else:
        print("No figure - unlinking files")
        if os.path.exists(ofn + '.png'):
            os.unlink(ofn + '.png')
        if os.path.exists(ofn + '.pdf'):
            os.unlink(ofn + '.pdf')
        os.system('touch "%s.png"' % ofn)
        os.system('touch "%s.pdf"' % ofn)
