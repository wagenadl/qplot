#!/usr/bin/python3

import glob
import os

def readoctave(ifn):
    codelines = []
    with open(ifn) as f:
        while f:
            line.replace('q', '')
            codelines.append(line)
    return codelines


def writepython(fd, codelines):
    for l in codelines:
        l = l[:-1] # Remove newline
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
            fd.write('    %s\n' % l.rstrip())
        
inroot = 'doc/ref'
outroot = 'doc/pyref'
for ifn in glob.glob(inroot + '/*.m'):
    pth, ofn = os.path.split(ifn)
    ofn, ext = os.path.splitext(ofn)
    with open(outroot + '/' + ofn + '.py', 'w') as f:
        writepython(f, readoctave(ifn))
    
