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

import glob
import sys
sys.path.append('..')
import qplot as qp

def header(f, title):
    f.write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" href="../css/doc.css" type="text/css">
<link rel="stylesheet" href="../css/alpha.css" type="text/css">
<title>%s</title>
</head>
''' % title)

def trailer(f):
    f.write('''</div>
<div class="tail">
(C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2014–2019.  This web page is licensed under the <a href="http://www.gnu.org/copyleft/fdl.html">GNU Free Documentation License</a>.
</div>
</body>
</html>
''')

def bodystart(f):
    f.write('''<body>
<div class="main">
<div class="index">
<span class="toidx"><a href="catg.html">Categories</a></span>
</div>
<h1 class="tight">QPlot: Alphabetical list of functions</h1>
''')

def printlist(f, funcs):
    f.write('''<div class="list">
''')
    lastletter = ''
    funcs = [f for f in funcs if f==f.lower() and '_' not in f]
    for func in sorted(funcs, key=lambda s: s.casefold()):
        letter = func[0].upper()
        if letter != lastletter:
            if lastletter!='':
                f.write('</table>\n')
            f.write('''
<table class="funcs">
<tr><td class="letter"><span class="letterspan">%s</span></td>
<td class="regular"><a class="mlink" href="%s.html">%s</a></td></tr>
''' % (letter, func, func))
            lastletter = letter
        else:
            f.write('''<tr><td></td>
<td><a class="mlink" href="%s.html">%s</a></td></tr>
''' % (func, func))
    f.write('''</table>
</div>
''')

funcs = [k for k,v in qp.__dict__.items() if callable(v) and k!="jetlut"]
for k, v in qp.luts.__dict__.items():
    if callable(v):
        funcs.append("luts." + k)
funcs.sort()

with open(sys.argv[2], 'w') as f:
    header(f, "QPlot: Alphabetical list of functions")
    bodystart(f)
    printlist(f, funcs)
    trailer(f)
