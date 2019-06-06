#!/usr/bin/python3

import glob

def readoctave(ifn):
    funcline = ''
    headcomments = []
    codelines = []
    with open(ifn) as f:
        while f:
            line = f.readline()
            if line=='':
                break
            elif line.find('function') >= 0:
                funcline = line
                break

        while f:
            line = f.readline()
            if line=='':
                break
            elif line.startswith('%'):
                headcomments.append(line)
            else:
                codelines.append(line)
                break

        while f:
            line = f.readline()
            if line=='':
                break
            elif line.startswith('% QPlot'):
                # Skip copyright
                while True:
                    line = f.readline()
                    if line=='':
                        break
                    elif line.startswith('%'):
                        pass
                    else:
                        codelines.append(line)
                        break
            else:
                codelines.append(line)
    return (funcline, headcomments, codelines)


def writepython(funcline, headcomments, codelines):
    print('# ------------------------------------------------------')
    print('# ', funcline, end='')
    idx = funcline.find('=')
    if idx<0:
        idx = funcline.find(' ')
    funcline = funcline[idx+1:].strip()
    hasvararg = funcline.find('varargin')>=0
    funcline = funcline.replace('varargin', '*args')
    if funcline.endswith(')'):
        pass
    else:
        funcline += '()'
    print('def %s:' % funcline)
    print("    '''")
    for line in headcomments:
        print(line[2:-1])
    print("'''")
    usesnargin = False
    for l in codelines:
        if l.find('nargin')>=0:
            nargin = funcline.count(',')
            if hasvararg:
                print('    nargin = %i + len(args)' % nargin)
            elif nargin==0 and funcline.find('()')>=0:
                pass
            else:
                print('    nargin = %i' % (nargin+1))
            break
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
            print('    %s' % l.replace('%', '#').rstrip())
        
inroot = '../octave/qplot-0.2'
mainm = glob.glob(inroot + '/*.m')
mainm.sort()
privatem =  glob.glob(inroot + '/private/*.m')
privatem.sort()
allm = privatem + mainm

for ifn in allm:
    print()
    (funcline, headcomments, codelines) = readoctave(ifn)
    writepython(funcline, headcomments, codelines)
    
