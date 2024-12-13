#!/usr/bin/python3

import sys
import os

os.chdir("build")

sys.path.append("../../python")
import qplot as qp

codepath = "../code"
sys.path.append(codepath)
import qphtmllib as qph


def create(fam):
    qp.luts.demo(fam)
    qp.save(f"html/luts/{fam}.png", 300)
    qp.close()

def createall():
    for fam in qp.luts.families():
        if len(qp.luts.family(fam)):
            create(fam)

def body(title):
    html = """
    <h2>Look-up tables for image rendering</h2>
    
    <p>The following colormaps are available for use with
    <a href="../pyref/luts.set.html">luts.set()</a> and <a
    href="../pyref/luts.get.html">luts.get()</a>.

    <p>In a few instances, multiple families offer like-named
    colormaps. In that case, you can prefix the name with the family,
    e.g., <span class="inlineeg">cm = qp.luts.get("misc.rainbow")</span>.

    <p>Most color maps are continuous, i.e., comprise an
    infinitesimally fine range of shades. Some are categorical, i.e.,
    define a strictly finite number of shades, such as the
    “qualitative” family from Matplotlib. There are also colormaps
    that are categorical by default but may be used as continuous maps
    by asking for a specific number of shadings, such as the “carto”
    family from Plotly.

    """
    
    for fam in qp.luts.families():
        luts = qp.luts.family(fam)
        N = len(luts)
        if N > 0:
            if N==1:
                cls = "lut-half"
            else:
                cls = "lut-full"
            html += f"""
            <h2 class="lutfamily">{fam}</h2>
            <div class="qpt"><img class="{cls}" src="{fam}.png"></div>
            """

    html += """
    <p>Only the “native” colormaps are strictly part of QPlot.
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
    <a href="https://colorcet.holoviz.org/"/>colorcet</a>.

    <p>Colormaps from other sources can also be used with QPlot.
    Excellent colormaps are provided, e.g., by the <a
    href="https://cmasher.readthedocs.io/index.html">CMasher</a>, <a
    href="https://github.com/callumrollo/cmcrameri">cmcrameri</a>, and
    <a href="https://github.com/yt-project/cmyt">cmyt</a>
    projects. See also <a href="../pyref/lut.html">lut()</a>.
    """
    return html


def document(title="Color maps"):
    html = qph.doctype()
    html += "<html>"
    html += qph.head(title, 1)
    html += "<body>"
    html += '<div class="contents">'
    crumbs = [(title, None)]
    html += qph.sidebar(crumbs, dirlevel=1)
    html += '<div id="central">'
    html += qph.header()
    html += qph.idxtitleblock(title)
    html += '<div class="rst"><div class="document">'
    html += body(title)
    html += '</div></div>\n' # document rst
    html += qph.footer()
    html += '</div>\n' # central
    html += '<div id="rightspace"></div>'
    html += '</div>\n' # contents
    return html

def createindex():
    with open("html/luts/index.html", 'w') as f:
        f.write(document())

        
def hidedisplay():
    with os.popen(f"{codepath}/ensurexvfb") as f:
        txt = f.read().strip()
        if txt:
            os.environ["DISPLAY"] = txt
        else:
            raise RuntimeError("Cannot create X11 display")

        
def main():
    hidedisplay()
    createindex()
    createall()


main()
