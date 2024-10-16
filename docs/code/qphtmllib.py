import inspect
import re
import time

import qpdoclib as qpd


funcs = qpd.qplotfunctions()


def thisyear():
    return time.gmtime().tm_year


def doctype():
    return "<!DOCTYPE html>\n"


def head(ttl, depth=1):
    csspath = ("../" * depth) + "css"
    jspath = ("../" * depth) + "js"
    return f"""<head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <script src="{jspath}/docs.js"></script>
      <link rel="stylesheet" href="{csspath}/layout.css" type="text/css">
      <link rel="stylesheet" href="{csspath}/color.css" type="text/css">
      <title>QPlot: {ttl}</title>
    </head>
    """


def header():
    return f"""
    <div class="header">
    </div>
    """


def footer():
    year = thisyear()
    return f"""
    <div class="footer">
      QPlot Documentation — (C)
      <a href="http://www.danielwagenaar.net">Daniel A. Wagenaar</a>,
      2014–{year}
    </div>
"""


def sidebar(breadcrumbs):
    txt = """
    <div id="sidebar">
      <div class="logography">
        <div class="project">QPlot</div>
        <div class="ptagline">Beautifully typeset graphs for science</div>
      </div>
      <div class="breadcrumbs">
    """

    for k, (label, url) in enumerate(breadcrumbs.items()):
        if url is None:
            content = label
        else:
            content = f'<a href="{url}">{label}</a>'
        txt += f"""
        <div class="breadcrumb-{k+1}">
        <div class="bcleft"><span class="bcmark"></span></div>        
        <div class="bcinner">{content}</div>
        </div>
        """
    txt += """
      </div>
    </div>
    """
    return txt


def pydoc(doc, func, kww):
    r = re.compile(r"((?<!LUTS)\W+)")
    wrd = re.compile(r"(?:LUTS\.)?[a-zA-Z]+")
    nl = re.compile(r"\n")
    paren = re.compile(r"\(")
    parenc = re.compile(r"\)")
    bits = r.split(doc)
    out = ""
    gotfunc = False
    depth = 0
    inargs = False
    myargs = { kw for kw in kww }
    column = 0
    prevbits = [""] + bits[:-1]
    nextbits = bits[1:] + [""]
    for prv, bit, nxt in zip(prevbits, bits, nextbits):
        lobit = bit.lower()
        ishigh = bit == bit.upper()
        ishighplural = bit.endswith("s") and bit[:-1] == bit[:-1].upper()
        if wrd.match(bit):
            # This bit is word-like
            if (prv.endswith('"') or prv.endswith("'")) \
                   and nxt.startswith(prv[-1]):
                out += bit # don't mess with text in quotes
            elif prv.endswith("-") or nxt.startswith("-"):
                out += bit # hyphenated words are not func/var names
            elif ishigh and lobit==func:
                out += f'<span class="mefunc">{lobit}</span>'
                if column<=4:
                    gotfunc = True
            elif inargs and (gotfunc or lobit in myargs):
                out += f'<span class="arg">{lobit}</span>'
                if gotfunc:
                    myargs.add(lobit)
            elif ishigh and lobit in myargs:
                out += f'<span class="arg">{lobit}</span>'
            elif ishigh and lobit in funcs:
                out += f'<a class="tmlink" href="{lobit}.html">{lobit}</a>'
            elif ishighplural and lobit[:-1] in funcs:
                out += f'<a class="tmlink" href="{lobit[:-1]}.html">{lobit[:-1]}</a>s'
            elif ishigh and len(bit)>1:
                out += f'<span class="arg">{lobit}</span>'
                gotfunc = False
            else:
                out += bit
        else:
            # This bit is punctuation-like
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
            out += lst
            nobr = False
            for sbit in sub:
                if sbit == '':
                    out += '\n<p>'
                    nobr = True
                else:
                    if lst.endswith('.') or lst.endswith(':') \
                       or (sbit.startswith(' ' * 5) \
                           and not (sbit.startswith(' ' * 8) \
                                    and nxt[:1]==nxt[:1].lower())):
                        if not nobr:
                            out += '<br>\n'
                    else:
                        out += ' '
                    if not sbit.startswith(' ' * 4) and len(sbit.strip()):
                        print('Expected at least  4 spaces at start of line.')
                        print('Got: "%s"' % sbit)
                        raise Exception("Input format error")
                    if sbit.startswith(' '*8) and nxt[:1]==nxt[:1].lower():
                        sbit = sbit[8:]
                    else:
                        sbit = sbit[4:]
                    while sbit.startswith(' '):
                        out += '&nbsp;'
                        sbit = sbit[1:]
                    out += sbit
                    nobr = False
        column += len(bit)
    return out                   


def bodytext(body, func, kww):
    return f"""<div class="pyhelphead">Help text:</div>
    <div class="pyhelp">
    {pydoc(body, func, kww)}
    </div>
    """


def menubutton():
    return """<div class="menubutton" onclick="menuclick()">≡</div>"""


def titleblock(func, tagline):
    return f"""<div class="titleblock">
    {menubutton()}<div class="funcname"><span
    class="mefunc">{func}</span></div>
    <div class="tagline">{tagline}</div>
    </div>
"""


def sectitleblock(section):
    return f"""<div class="sectitleblock">
    {menubutton()}<div class="sectitle">{section}</div>
    </div>
    """


def idxtitleblock(section):
    return f"""<div class="idxtitleblock">
    {menubutton()}<div class="idxtitle">{section}</div>
    </div>
    """


def submoduletext(func, body):
    out = """<div class="pysighead">Contained functions:</div>
    <div class="pyhelp">
    <p>
    """
                   
    for name, fn in qp.__dict__[func].__dict__.items():
        if name.upper() in body:
            out += f'<a href="{func}.{name}.html"><b>{name}</b></a> — '
            doc = fn.__doc__.split("\n")[0].split(" - ")[-1]
            out += doc
            out += "<br>"

    out += """</div>"""
    return out                   


def sigline(func, obj):
    # This should be improved to print annotations in the future,
    # but for now, we don't use them, so it's OK.
    out = f"""<div class="pysighead">Call signature:</div>
    <div class="pysig">
    <span class="mefunc">{func}</span>("""
    first = True
    sig = inspect.signature(obj)
    pp = sig.parameters
    kww = []
    for k in pp.keys():
        if not first:
            out += ", "
        first = False
        kv = str(pp[k]).split('=', 1)
        out += f'<span class="arg">{kv[0]}</span>' 
        kww.append(kv[0])
        if len(kv)>1:
            out += f'={kv[1]}'
    out += """)</div>\n"""
    return out, kww

    
def egimage(f, func):
    return f"""<div class="egimage">
    <image class="egimg" src="{func}.png" width="300px">
    <div class="eglink">Download <a href="{func}.pdf">pdf</a></div>
    </div>
    """


def pyegline(line, func):
    """Construct a line from a python example

    LINE must be read from a _eg.py file
    FUNC must be the name of the function being documented
    """

    out = ""
    gr = re.compile(r"^( *)").search(line).group()
    for k in gr:
        out += "&nbsp; "

    r = re.compile(r"(qp(?:\.luts)?\.\w+)")
    bits = r.split(line[len(gr):])
    for k in range(len(bits)):
        bit = bits[k]
        if k % 2:
            if bit == "qp." + func:
                out += f'qp.<span class="mefunc">{func}</span>'
            else:
                out += f'qp.<a href="{bit[3:]}.html">{bit[3:]}</a>'
        else:
            out += bit
    return out

    
def egtext(func, example):
    out = """<div class="egcontainer">
    <div class="eghead">Example:</div>
    <div class="example">
    """
    
    for line in example.split("\n"):
        line = line.rstrip()
        if line == "":
            out +=  """<p class="empty"></p>"""
        else:
            out += f"""<p class="eg">{pyegline(line, func)}</p>"""

    out += f"""</div>
    <div class="eglink">
    Download <a href="{func}_eg.py">source</a>.
    </div>
</div>
    """
    return out
