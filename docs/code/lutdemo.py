#!/usr/bin/python3

import sys
import os
sys.path.append('..')
import qplot as qp


def header(f, title):
    f.write('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="../css/doc.css" type="text/css">
    <title>QPlot: %s</title>
  </head>
<body class="mloct"><div class="main">
    ''' % title)

    
def trailer(f): 
    f.write('''</div>
<div class="tail">
(C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2014–2019. This web page is licensed under the <a href="http://www.gnu.org/copyleft/fdl.html">GNU Free Documentation License</a>.
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


def titletext(f, func, tagline):
    f.write('''<div class="titlehead">
<span class="title">%s</span>
<span class="tagline">%s</span>
</div>
''' % (func, tagline))

func = "luts"
 
ofn = sys.argv[1]
with open(ofn, 'w') as f:
    header(f, func)
    indextext(f)
    titletext(f, "luts", "Look-up tables for image rendering")

    for fam in qp.luts.families():
        if len(qp.luts.family(fam)):
            f.write(f'''<h3>{fam}</h3>\n''')
            qp.luts.demo(fam)
            qp.save(f"html/pyref/lutdemo-{fam}.png", 120)
            qp.close()
            f.write(f'''<div class="qpt"><img src="lutdemo-{fam}.png"></div>''')

    f.write('''<p>Only the “native” colormaps are strictly part of QPlot.
The “sequential,” “diverging,” “cyclic,” “qualitative,” and “misc”
colormaps are from <a href="https://matplotlib.org/">Matplotlib</a>.
The “plotly,” “carto,” “cmocean,” and “colorbrewer” colormaps are from
<a href="https://plotly.com/">plotly</a>. 
The “cet” colormaps are from 
<a href="https://colorcet.holoviz.org/"/>colorcet</a>.
Non-native colormaps are only
available if the respective libraries are installed on your computer.
For copyright information on non-native colormaps, please refer to
<a href="https://matplotlib.org/">matplotlib.org</a>,
<a href="https://plotly.com/">plotly.com</a>, and
<a href="https://colorcet.holoviz.org/"/>colorcet</a>.\n''')

    f.write('''<p>In a few instances, multiple families offer like-named colormaps. In that case, you can prefix the name with the family in GET and SET, e.g., “cm = qp.get("cet.rainbow")”.''')

    f.write('''<p>Colormaps from other sources can also be used with QPlot.
Excellent colormaps are provided, e.g., by the 
<a href="https://cmasher.readthedocs.io/index.html">CMasher</a>,
<a href="https://github.com/callumrollo/cmcrameri">cmcrameri</a>, and
<a href="https://github.com/yt-project/cmyt">cmyt</a>
projects. See also <a href="lut.html">lut()</a>.\n''')

    trailer(f)
