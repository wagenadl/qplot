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
    A line that starts with X>4 spaces is a LIST ITEM if either:
      X <= 6
      X = same as previous lines space count
      X<10 and previous line was empty or had 4 spaces.
    A line with >X spaces is a CONTINUATION LINE.
    A line with 4 spaces starts a new paragraph if:
       Previous line had a different space count or was empty
       Previous line ended with "."
           and this line starts with capital.
    The above features examples of both types of special lines
    '''
    lines = text.split("\n")
    lastends = False
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
            lastx = 4 # pretend
        elif x < 4 and not first:
            raise ValueError("Must have ≥ 4 spaces")
        elif x <= 4:
            # regular text line
            if (lastends and _isupper(line[:1])) or lastx > 4:
                # Start new paragraph
                pargs.append(para)
                para = [line]
            else:
                para.append(line)
            lastx = 4
        elif x<=6 or x==lastx or (x<=10 and lastx==4):
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
        self.re_itemsplit = re.compile("( - |: )")
        self.re_pareno = re.compile(r"\(")
        self.re_parenc = re.compile(r"\)")
        self.re_word = re.compile(r"(?:LUTS\.)?[a-zA-Z]+")
        self.out = ""
        self.mykeywords = set()

    def parse(self, doc):
        for parg in _splittopargs(doc):
            if parg.startswith("  "):
                self.parse_listitem(parg[2:])
            else:
                self.parse_para(parg)
        return self.out

    def parse_listitem(self, item):
        self.out += '<div class="pylistitem">'
        bits = re.split(self.re_itemsplit, item)
        if len(bits) >= 3:
            # Study first bit specially
            self.out += '<span class="pli-key">'
            if bits[0].startswith('"'):
                self.out += bits[0]
            else:
                obits = []
                for kw in bits[0].split(" "):
                    lobit = kw.lower()
                    self.mykeywords.add(lobit)
                    obits.append(f'<span class="pykw">{lobit}</span>')
                self.out += " ".join(obits)
            self.out += "</span>"
            self.out += f'<span class="pli-sep">{bits[1]}</span>'
            self.out += '<span pclass="pli-val">'
            self.renderpara("".join(bits[2:]))
            self.out += "</span>"
        else:
            self.out += '<span class="pli-key">'
            self.renderpara(item)
            self.out += '</span>'
        self.out += "</div>"

    def renderpara(self, parg):
        bits = re.split(self.re_split, parg)
        prevbits = [""] + bits[:-1]
        nextbits = bits[1:] + [""]
        inargs = False
        for bit, prv, nxt in zip(bits, prevbits, nextbits):
            if prv.endswith("-") or nxt.startswith("-"):
                self.out += bit # don't mess with hyphenated words
                continue
            if prv[-1:] in ['"', "'"] and nxt.startswith(prv[-1]):
                self.out += bit # don't mess with text in quotes
                continue
            
            lobit = bit.lower()
            ishigh = bit == bit.upper()
            ispluhigh = bit.endswith("s") and bit[:-1] == bit[:-1].upper()
            if prv==self.func.upper() or inargs:
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
            elif inargs and self.re_word.match(bit):
                self.out += f'<span class="arg">{lobit}</span>'
                self.myargs.add(lobit)
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
    
        
def pydoc1(doc, func, kww):
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
            elif ishigh and lobit==self.func:
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
            biglike = len(bit) > 10
            if biglike:
                print(f"*BIG* [{prv}] [{[ord(c) for c in bit]}] [{nxt}]")
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
            if biglike:
                print(len(sub))
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

    
def egimage(func):
    return f"""<div class="egimageblock">
    <div class="egimage">
    <image class="egimg" src="{func}.png" width="300px">
    </div></div>
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
    out = """
    <div class="egtextblock">
    <div class="example">
    """
    
    for line in example.split("\n"):
        line = line.rstrip()
        if line == "":
            out +=  """<p class="empty"></p>"""
        else:
            out += f"""<p class="eg">{pyegline(line, func)}</p>"""

    out += f"""
    </div>
    </div>
    """
    return out


def eglinks(func):
    out = f"""
    <div class="eglinks">
    <div class="pylink">
    Download <a href="{func}_eg.py">source</a>.
    </div>
    <div class="pdflink">
    Download <a href="{func}.pdf">pdf</a>.
    </div>
    </div>
    """
    return out


def example(func, example):
    out = '<div class="eghead">Example:</div>'
    out += '<div class="egtopline"></div>'
    out += '<div class="egouterblock">'
    out += egtext(func, example)
    out += egimage(func)
    out += '</div>' # egouterblock
    out += '<div class="egbottomline"></div>'
    out += eglinks(func)
    return out

