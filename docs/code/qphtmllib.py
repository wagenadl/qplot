import inspect
import re
import time


sections = [("Installation", "installation.html"),
            ("Gallery", "gallery/index.html"),
            ("Python functions", "pyref/index.html"),
            ("Octave functions", "octref/index.html"),
            ]

funcs = []
def setfuncs(fu):
    global funcs
    funcs = fu


def thisyear():
    return time.gmtime().tm_year


def doctype():
    return "<!DOCTYPE html>\n"

def headfonts():
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,100..900;1,100..900&family=Noto+Serif:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
"""

def head(ttl, depth=1):
    csspath = ("../" * depth) + "css"
    jspath = ("../" * depth) + "js"
    return f"""<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <script src="{jspath}/docs.js"></script>
    <link rel="stylesheet" href="{csspath}/layout.css" type="text/css">
    <link rel="stylesheet" href="{csspath}/color.css" type="text/css">
    {headfonts()}
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
    <div class="footerspace"></div>
    <div class="footer">
      QPlot Documentation — (C)
      <a href="http://www.danielwagenaar.net">Daniel A. Wagenaar</a>,
      2014–{year}
    </div>
"""

def breadcrumbs(crumbs, sibs, level=0):
    txt = ""
    if crumbs:
        label, url = crumbs[0]
    else:
        label, url = "", None
    if sibs:
        heresibs = sibs[0]
        childsibs = sibs[1:]
    else:
        heresibs = [(label, url)]
        childsibs = None
    childcrumbs = crumbs[1:]
    for lbl, ur1 in heresibs:
        if lbl==label:
            mark = """<span class="bcmark"></span>"""
            cls = "bchere"
        else:
            mark = ""
            cls = ""
        uselbl = lbl.split(":")[-1]
        txt += f"""<div class="breadcrumb-{level+1} {cls}">"""
        txt += f"""<div class="bcheader  {cls}">"""
        txt += f"""<div class="bcleft">{mark}</div>"""
        if ur1 is None:
            cont1 = uselbl
        else:
            cont1 = f'<a href="{ur1}">{uselbl}</a>'
        txt += f"""<div class="bcinner {cls}">{cont1}</div></div>"""
        if lbl==label:
            if childsibs or childcrumbs:
                txt += f"""<div class="bcchildren">"""
                txt += breadcrumbs(childcrumbs, childsibs, level + 1)
                txt += f"""</div>"""
        txt += "</div>"

    return txt


def sidebar(crumbs, sibs=None, dirlevel=1):
    up = "../" * dirlevel
    secs = [(k, up + v) for k, v in sections]
    if sibs is None:
        sibs = [secs]
    else:
        sibs.insert(0, secs)
    txt = f"""
    <div id="sidebar">
      <div class="logography"><div class="centered">
        <div class="project"><a href="{up}index.html">QPlot</a></div>
        <div class="ptagline">Beautifully typeset graphs for science</div>
      </div></div>
      <div class="breadcrumbs"><div class="centered">
    """
    txt += breadcrumbs(crumbs, sibs)
    txt += """
      </div></div>
    </div>
    """
    return txt


def _countspaces(text):
    k = 0
    K = len(text)
    while k < K and text[k] == ' ':
        k += 1
    return k


_re_upper = re.compile(r"^[A-Z][A-Z_]*$")

def _isupper(text):
    return _re_upper.match(text)


def _splittopargs(text):
    '''Our standard is that each line should start with four spaces.
    We also support LIST ITEMs and CONTINUATION LINEs.
    A line that starts with X > 4 spaces is a LIST ITEM if either:
      X <= 6
      X = same as previous lines space count
      X < 10 and previous line was empty or had 4 spaces.
    A line with > X spaces is a CONTINUATION LINE.
    A line with 4 spaces starts a new paragraph if:
       Previous line had a different space count or was empty
       Previous line ended with "."
           and this line starts with capital.
    The above features examples of both types of special lines
    '''
    lines = text.split("\n")
    lastends = False
    four = 4
    lastx = 4
    para = []
    pargs = []
    first = True
    for line in lines:
        x = _countspaces(line)
        line = line.strip()
        if line == "":
            pargs.append(para)
            para = []
            lastx = four # pretend
        elif x < four and not first:
            raise ValueError("Must have ≥ 4 spaces")
        elif x <= four:
            if first:
                four = x
            # regular text line
            if (lastends and _isupper(line[:1])) or lastx > four:
                # Start new paragraph
                pargs.append(para)
                para = [line]
            else:
                para.append(line)
            lastx = four
        elif x<=6 or x==lastx or (x<=10 and lastx==four):
            # list item
            pargs.append(para)
            para = ["  " + line]
            lastx = x
        else:
            # continuation line
            para.append(line)
        first = False
        lastends = line.endswith(".") or line.endswith(".)")
    pargs.append(para)
    pargs = [" ".join(para) for para in pargs if para]
    return pargs


class PyDoc:
    def __init__(self, func, args):
        self.func = func
        self.myargs = {arg for arg in args}
        #self.re_call = re.compile(f"{func.upper()}\\(([^)]*)\\)")
        self.re_split = re.compile(r"((?<!LUTS)\W+)")
        self.re_itemsplit = re.compile("(::+ )")
        self.re_itemsplit1 = re.compile("( - )")
        self.re_pareno = re.compile(r"\(")
        self.re_parenc = re.compile(r"\)")
        self.re_word = re.compile(r"(?:LUTS\.)?[a-zA-Z]+")
        self.re_specialarg = re.compile("«([a-z]+)»")
        self.out = ""
        self.mykeywords = set()

    def extractspecialargs(self, doc):
        bits = self.re_specialarg.split(doc)
        for k in range(1, len(bits), 2):
            self.myargs.add(bits[k])
            bits[k] = bits[k].upper()
        return "".join(bits)
        
    def parse(self, doc):
        doc = self.extractspecialargs(doc)
        for parg in _splittopargs(doc):
            if parg.startswith("  "):
                self.parse_listitem(parg[2:])
            else:
                self.parse_para(parg)
        return self.out


    def countparens(self, bit):
        nopen = len(self.re_pareno.findall(bit))
        nclose = len(self.re_parenc.findall(bit))
        return nopen - nclose

    def clearquote(self, bit):
        if bit[:1]=="«" and bit[-1:]=="»":
            return bit[1:-1]
        else:
            return bit


    def listitem_tripartite(self, key, sep, value):
        if sep == " - ":
            sep = " — "
            cls = "pykw"
        else:
            sep = ": "
            cls = "pylit"
        self.out += '<span class="pli-key">'
        if key[:1]=='"':
            self.out += '<span class="doceg">'           
            self.renderpara(self.clearquote(key), False)
            self.out += '</span>'
        else:
            obits = []
            for kw in key.split(" "):
                lobit = kw.lower()
                #if cls == "pykw":
                self.mykeywords.add(lobit)
                obits.append(f'<span class="{cls}">{lobit}</span>')
            self.out += " ".join(obits)
        self.out += "</span>"
        self.out += f'<span class="pli-sep">{sep}</span>'
        self.out += '<span pclass="pli-val">'
        self.renderpara(value)
        self.out += "</span>"

    def listitem_simple(self, item):
        self.out += '<span class="pli-key">'
        if False: #self.isexample:
            self.out += '<span class="doceg">'           
            self.renderpara(self.clearquote(item), False)
            self.out += '</span>'
        else:
            self.renderpara(item, False)
        self.out += '</span>'
        
    def parse_listitem(self, item):
        self.out += '<div class="pylistitem">'
        bits = re.split(self.re_itemsplit, item)
        if len(bits) == 1:
            bits = re.split(self.re_itemsplit1, item)
        if len(bits) >= 3 and self.countparens(bits[0])==0:
            self.listitem_tripartite(bits[0], bits[1], "".join(bits[2:]))
        else:
            self.listitem_simple(item)
        self.out += "</div>"

    def renderpara(self, parg, collectargs=True):
        bits = re.split(self.re_split, parg)
        prevbits = [""] + bits[:-1]
        nextbits = bits[1:] + [""]
        inargs = False
        for bit, prv, nxt in zip(bits, prevbits, nextbits):
            if (prv.endswith("-") and len(prv)>1) \
               or (nxt.startswith("-") and len(nxt)>1):
                self.out += bit # don't mess with hyphenated words
                continue
            if prv[-1:] in ['"', "'"] and nxt.startswith(prv[-1]):
                self.out += bit # don't mess with text in quotes
                continue
            
            lobit = bit.lower()
            ishigh = bit == bit.upper()
            ispluhigh = bit.endswith("s") and bit[:-1] == bit[:-1].upper()
            if (prv==self.func.upper() or inargs) and collectargs:
                nopen = len(self.re_pareno.findall(bit))
                nclose = len(self.re_parenc.findall(bit))
                if nopen > nclose:
                    inargs = True
                elif nopen < nclose:
                    inargs = False

            if ishigh and lobit==self.func:
                self.out += f'<span class="mefunc">{lobit}</span>'
                gotfunc = True
            elif ishigh and lobit in self.mykeywords:
                self.out += f'<span class="pykw">{lobit}</span>'
            elif ishigh and lobit in self.myargs:
                self.out += f'<span class="arg">{lobit}</span>'
            elif ispluhigh and lobit[:-1] in self.myargs:
                self.out += f'<span class="arg">{lobit}</span>'
            elif ishigh and lobit in funcs:
                self.out += f'<a class="tmlink" href="{lobit}.html">{lobit}</a>'
            elif ispluhigh and lobit[:-1] in funcs:
                self.out += f'<a class="tmlink" href="{lobit[:-1]}.html">{lobit[:-1]}</a>s'
            elif inargs and self.re_word.match(bit) and nxt != "." and prv != ".":
                self.out += f'<span class="arg">{lobit}</span>'
                self.myargs.add(lobit)
            elif self.re_word.match(bit) and prv == "" and nxt == " = ":
                self.out += f'<span class="arg">{lobit}</span>'
            else:
                self.out += bit
        
            
    def parse_para(self, parg):
        #moreargs = self.re_call.findall(parg)
        #for args in moreargs:
        #    args = args.split(",")
        #    for arg in args:
        #        self.myargs.add(arg.split("=")[0].strip())
        
        self.out += '<div class="pypara">'
        self.renderpara(parg)
        self.out += "</div>"

def pydoc(doc, func, kww):
    pyd = PyDoc(func, kww)
    return pyd.parse(doc)


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


def octpars(s):
    try:
        oidx = s.index('(')
        cidx = s.index(')')
        if cidx > oidx:
            bits = s[oidx+1:cidx-1].split(",")
            return { k.strip():k.strip() for k in bits }
    except:
        return {}


def sigline(func, obj):
    # This should be improved to print annotations in the future,
    # but for now, we don't use them, so it's OK.
    out = f"""<div class="pysighead">Call signature:</div>
    <div class="pysig">
    <span class="mefunc">{func}</span>("""
    first = True
    if type(obj)==list:
        pp = octpars(obj[0])
    else:
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

    
def egimage(func):
    return f"""<div class="egimageblock">
    <div class="egimage">
    <div class="egimagetopline"></div><image class="egimg" src="{func}.png" width="300px"><div class="egimagebottomline"></div>
    </div>
    <div class="pdflink">
    Download <a href="{func}.pdf">pdf</a>.
    </div>
    </div>
    """


def octegline(line, func):
    gr = re.compile(r"(\W)")
    bits = gr.split(line)
    out = ""
    quot = False
    for bit in bits:
        if "'" in bit:
            quot = not quot
        if bit==func and not quot:
            out += f'<span class="mefunc">{func}</span>'
        elif bit in funcs and not quot:
            out += f'<a href="{bit}.html">{bit}</a>'
        else:
            out += bit
    return out

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

    
def egtext(func, example, typ="py"):
    out = """
    <div class="egtextblock">
    <div class="example">
    """
    
    for line in example.split("\n"):
        line = line.rstrip()
        if line == "":
            out +=  """<p class="empty"></p>"""
        elif typ=="m":
            out += f"""<p class="eg">{octegline(line, func)}</p>"""
        else:
            out += f"""<p class="eg">{pyegline(line, func)}</p>"""

    out += f"""
    </div>
    <div class="pylinkline"></div>
    <div class="pylink">
    Download <a href="{func}_eg.{typ}">source</a>.
    </div>    
    </div>
    """
    return out




def example(func, example, typ="py"):
    out = '<div class="eghead">Example:</div>'
    out += '<div class="egtopline"></div>'
    out += '<div class="egouterblock">'
    out += egtext(func, example, typ)
    out += egimage(func)
    out += '</div>' # egouterblock
    out += '<div class="egbottomline"></div>'
    return out

