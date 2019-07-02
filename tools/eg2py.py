#!/usr/bin/python3

import glob
import os

def readoctave(ifn):
    codelines = []
    with open(ifn) as f:
        while f:
            line = f.readline()
            if line=='':
                break
            codelines.append(line)
    return codelines


def writepython(fd, codelines):
    fd.write('import pyqplot as qp\n')
    fd.write('import numpy as np\n\n')
    for l in codelines:
        l = l[:-1] # Remove newline
        l = l.replace('q', 'qp.')
        l = l.replace("'qp.", "'")
        l = l.replace('%', '#')
        l = l.replace('  ', '    ')
        if l.endswith(';'):
            l = l[:-1]
        strp = l.strip()
        bits = strp.split()
        bits.append('')
        kw = bits[0]
        if kw=='if' or kw=='for' or kw=='while':
            l += ':'
        if kw=='end':
            pass
        else:
            fd.write('%s\n' % l.rstrip())
        
inroot = 'doc/ref'
outroot = 'doc/pyref'
for ifn in glob.glob(inroot + '/*.m'):
    pth, ofn = os.path.split(ifn)
    ofn, ext = os.path.splitext(ofn)
    ofn = ofn[1:]
    ofn = outroot + '/' + ofn + '.py'
    print('Converting', ifn, 'to', ofn)
    with open(ofn, 'w') as f:
        writepython(f, readoctave(ifn))
    
