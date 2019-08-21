#!/usr/bin/python3

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014-2019  Daniel Wagenaar
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
sys.path.append('..')
import pyqplot as qp

def header(f, title):
    f.write('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="../css/doc.css" type="text/css">
    <link rel="stylesheet" href="../css/catg.css" type="text/css">
    <title>%s</title>
  </head>
    ''' % title)

def trailer(f): 
    f.write('''</div>
<div class="tail">
(C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2014–2019. This web page is licensed under the <a href="http://www.gnu.org/copyleft/fdl.html">GNU Free Documentation License</a>.
</div>
</body>
</html>
''')

def bodystart(f):
    f.write('''<body>
<div class="main">
<div class="index">
<span class="toidx"><a href="alpha.html">Alphabetical list</a></span>
</div>
<h1 class="tight">QPlot: Categorized list of functions</h1>
''')

def writecatg(f, lines):
    first = True
    funcs = []
    f.write('<div class="list">\n')
    for line in lines:
        if line.find(':')>=0:
            if not first:
                f.write('</table>\n')
            f.write('''<table class=funcs>
<tr><td class="letter"><span class="letterspan">%s</span></td></tr>
''' % line)
        elif line != '':
            f.write('''<tr><td class="regular">
<a class="mlink" href="%s.html">%s</a>
</td></tr>
''' % ( line, line))
            funcs.append(line)
    f.write('</table></div>\n')
    return funcs
    
funcs = [k for k,v in qp.__dict__.items() if callable(v)]

ifn = sys.argv[1]
ofn = sys.argv[2]

with open(ifn) as f:
    txt = f.read()

with open(ofn, 'w') as f:
    header(f, "QPlot: Categorized list of functions")
    bodystart(f)
    docd = writecatg(f, [line.strip() for line in txt.split('\n')])
    trailer(f)

ok = True
for f in funcs:
    if f.find('__')<0 and f==f.lower() and not f in docd:
        print('Not in category page: %s' % f)
        ok = False
for f in docd:
    if not f in funcs:
        print('Nonexistent: %s' %f)
        ok = False

if not ok:
    os.unlink(ofn)
    
