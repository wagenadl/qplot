#!/usr/bin/python3

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014-2023  Daniel Wagenaar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import re
import inspect
sys.path.append('..')
import qplot as qp

ofn = sys.argv[1]
dr, fn = os.path.split(sys.argv[1])
func, xt = os.path.splitext(fn)

funcs = {k for k,v in qp.__dict__.items() if callable(v)}
for k, v in qp.luts.__dict__.items():
    if callable(v):
        funcs.add("luts." + k)


def writeheader(f, func):
    f.write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" href="../css/doc.css" type="text/css">
<title>QPlot: %s</title>
</head>
<body class="mloct"><div class="main">
''' % func)

def writetrailer(f):
    f.write('''</div>
<div class="tail">
QPlot Documentation — (C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2014–2023
</div>
</body>
</html>
''')

def indextext(f):
    f.write('''<div class="toindex">
<span class="toidx"><a href="alpha.html">Alphabetical list</a></span>
<span class="toidx"><a href="catg.html">Categories</a></span>
</div>
''')


def extracttitle(func, doc):
    lines = doc.split('\n')
    title = lines[0]
    if title.startswith(func.upper()):
        title = title[len(func):]
        if title.startswith(' - '):
            title = title[3:]
    else:
        print('Unexpected title line for %s: %s' % (func, title))
        sys.exit(1)
    return title

def extractbody(doc):
    lines = doc.split('\n')
    lines.pop(0)
    return '\n'.join(lines)

def pyeg(doc, func):
    out = []
    gr = re.compile(r'^( *)').search(doc).group()
    for k in gr:
        out.append("&nbsp; ")
    doc = doc[len(gr):]

    r = re.compile(r'(qp(?:\.luts)?\.\w+)')
    bits = r.split(doc)
    for k in range(len(bits)):
        bit = bits[k]
        if k % 2:
            if bit=='qp.'+func:
                out.append('qp.<span class="mefunc">%s</span>' % func)
            else:
                out.append('qp.<a href="%s.html">%s</a>' % (bit[3:],bit[3:]))
        else:
            out.append(bit)
    return ''.join(out)

def pydoc(doc, func, kww):
    r = re.compile(r'((?<!LUTS)\W+)')
    wrd = re.compile(r'(?:LUTS\.)?[a-zA-Z]+')
    nl = re.compile(r'\n')
    paren = re.compile(r'\(')
    parenc = re.compile(r'\)')
    bits = r.split(doc)
    out = ['<p>']
    gotfunc = False
    depth = 0
    inargs = False
    myargs = { kw for kw in kww }
    column = 0
    prevbits = [''] + bits[:-1]
    nextbits = bits[1:] + ['']
    for prv, bit, nxt in zip(prevbits, bits, nextbits):
        if wrd.match(bit):
            if (prv.endswith('"') or prv.endswith("'")) and nxt.startswith(prv[-1]):
                out.append(bit) # don't do anything with text in quotes
            elif prv.endswith("-") or nxt.startswith("-"):
                out.append(bit) # hyphenated words are not function/variable names
            elif bit==bit.upper() and bit.lower()==func:
                out.append('<span class="mefunc">%s</span>' % bit.lower())
                if column<=4:
                    gotfunc = True
            elif inargs and (gotfunc or bit.lower() in myargs):
                #print(bit, inargs, gotfunc, bit.lower() in myargs)
                out.append('<span class="arg">%s</span>' % bit.lower())
                if gotfunc:
                    myargs.add(bit.lower())
            elif bit==bit.upper() and bit.lower() in myargs:
                #print(bit, bit.lower() in myargs)
                out.append('<span class="arg">%s</span>' % bit.lower())
            elif bit==bit.upper() and bit.lower() in funcs:
                out.append('<a class="tmlink" href="%s.html">%s</a>'
                           % (bit.lower(), bit.lower()))
            elif bit[:-1] == bit[:-1].upper() and bit.endswith("s") \
                 and bit[:-1].lower() in funcs:
                out.append('<a class="tmlink" href="%s.html">%s</a>s'
                           % (bit[:-1].lower(), bit[:-1].lower()))
            elif len(bit)>1 and bit==bit.upper():
                #print(bit)
                out.append('<span class="arg">%s</span>' % bit.lower())
                gotfunc = False
            else:
                out.append(bit)
        else:
            if bit.startswith('(') and prv.lower() in funcs:
                inargs = True
            depth += len(paren.findall(bit)) - len(parenc.findall(bit))
            if depth<=0:
                inargs = False
                gotfunc = False
            if "\n" in bit:
                inargs = False
                gotfunc = False
                depth = 0
            sub = nl.split(bit)
            lst = sub.pop(0)
            out.append(lst)
            nobr = False
            for sbit in sub:
                if sbit=='':
                    out.append('\n<p>')
                    nobr = True
                else:
                    if lst.endswith('.') or lst.endswith(':') \
                       or (sbit.startswith(' '*5) and not \
                           (sbit.startswith(' '*8) and nxt[:1]==nxt[:1].lower())):
                        if not nobr:
                            out.append('<br>\n')
                    else:
                        out.append(' ')
                    if not sbit.startswith(' '*4):
                        print('Expected at least  4 spaces at start of line.')
                        print('Got: "%s"' % sbit)
                        sys.exit(1)
                    if sbit.startswith(' '*8) and nxt[:1]==nxt[:1].lower():
                        sbit = sbit[8:]
                    else:
                        sbit = sbit[4:]
                    while sbit.startswith(' '):
                        out.append('&nbsp;')
                        sbit = sbit[1:]
                    out.append(sbit)
                    nobr = False
        column += len(bit)
    return ''.join(out) + '\n'

def titletext(f, func, tagline):
    f.write('''<div class="titlehead">
<span class="title mefunc">%s</span>
<span class="tagline">%s</span>
</div>
''' % (func, tagline))

def submoduletext(f, func, body):
    f.write('''<div class="pysighead">Contained functions:</div>
<div class="pyhelp">
<p>
''')
    for name, fn in qp.__dict__[func].__dict__.items():
        if name.upper() in body:
            f.write(f'''<a href="{func}.{name}.html"><b>{name}</b></a> — ''')
            print(name, fn)
            doc = fn.__doc__.split("\n")[0].split(" - ")[-1]
            f.write(doc)
            f.write("<br>")
    f.write('''</div>
''')

    
def sigline(f, func, obj):
    # This should be improved to print annotations in the future,
    # but for now, we don't use them, so it's OK.
    f.write('''<div class="pysighead">Call signature:</div>
<div class="pysig"><p><span class="mefunc">%s</span>(''' % func)
    first = True
    sig = inspect.signature(obj)
    pp = sig.parameters
    kww = []
    for k in pp.keys():
        if not first:
            f.write(', ')
        first = False
        kv = str(pp[k]).split('=', 1)
        f.write('<span class="arg">%s</span>' % kv[0])
        kww.append(kv[0])
        if len(kv)>1:
            f.write('=%s' % kv[1])
    f.write(''')</p></div>
''')
    return kww
    
def bodytext(f, body, func, kww):
    f.write('''<div class="pyhelphead">Help text:</div>
<div class="pyhelp">
''')
    f.write(pydoc(body, func, kww))
    f.write('''</div>
''')

def egimage(f, func):
    f.write('''<div class="egimage">
<image class="egimg" src="%s.png" width="300px">
<div class="eglink">Download <a href="%s.pdf">pdf</a></div>
</div>
''' % (func, func))

def egtext(f, func, example):
    f.write('''<div class="egcontainer">
<div class="eghead">Example:</div>
<div class="example">
''')
    
    for line in example:
        line = line.rstrip()
        if line=='':
            f.write('''<p class="empty"></p>
''')
        else:
            f.write('''<p class="eg">%s</p>
''' % pyeg(line, func))
    f.write('''</div>
<div class="eglink">
Download <a href="%s_eg.py">source</a>.
</div>
</div>
''' % func)

obj = qp
for fn in func.split("."):
    obj = obj.__dict__[fn]
doc = obj.__doc__
title = extracttitle(func, doc)
body = extractbody(doc)
with open('html/pyref/%s_eg.py' % func) as f:
    example = f.read().split('\n')

with open(ofn, 'w') as f:
    writeheader(f, func)
    indextext(f)
    titletext(f, func, title)
    if func=="luts":
        submoduletext(f, func, body)
    else:
        kww = sigline(f, func, obj)
        bodytext(f, body, func, kww)
    if os.path.exists('html/pyref/%s.png' % func):
        s = os.stat('html/pyref/%s.png' % func)
        if s.st_size>0:
            egimage(f, func)
    if example is not None:
        egtext(f, func, example)

    if func.startswith("luts."):
        f.write('''<p>The full collection of available colormaps is shown <a href="lutdemo.html">here</a>.''')
    writetrailer(f)

