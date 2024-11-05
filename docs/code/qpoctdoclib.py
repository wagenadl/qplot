import re
import glob

octpath = "../octave/qplot"

def qplotfunctions():
    funcs = glob.glob(f"{octpath}/*.m")
    funcs = [func.split("/")[-1][:-2] for func in funcs]
    return funcs

_funcs = qplotfunctions()


def qpfunction(funcname):
    with open(f"{octpath}/{funcname}.m") as fd:
        obj = fd.read()
    return obj.split("\n")


def docstring(funcname):
    obj = qpfunction(funcname)
    doc = []
    for line in obj:
        if line.startswith("%"):
            doc.append(line)
        if doc and not line.startswith("%"):
            break
    return doc
    

def tagline(funcname):
    doc = docstring(funcname)
    if not doc:
        raise ValueError("No docstring")
    title = doc[0][1:].strip()
    if not title.startswith(funcname.upper()):
        raise ValueError(f"Unexpected tagline for {funcname}")
    title = title[len(funcname):]
    if title.startswith(" - "):
        title = title[3:]
    bits = title.split(" ")
    res = []
    for bit in bits:
        if len(bit) >= 2 and bit == bit.upper():
            lobit = bit.lower()
            bit = f'<a href="{lobit}.html">{lobit}</a>'
        elif len(bit) >= 2 and bit.endswith("s") \
             and bit[:-1] == bit[:-1].upper():
            lobit = bit.lower()
            bit = f"""<a href="{lobit[:-1]}.html">{lobit}</a>"""
        res.append(bit)
    return " ".join(res)


def docbody(funcname):
    doc = docstring(funcname)
    if len(doc)<2:
        return ""
    return "\n".join([x[1:].strip() for x in doc[1:]])

    

def loadexample(funcname, root):
    try:
        with open(f"{root}/{funcname}_eg.m") as f:
            return f.read()
    except FileNotFoundError:
        print("Not documented by example:", funcname)
        return None
    

def organization():
    funcs = []
    section = None
    org = {}

    def addsec():
        nonlocal funcs, section, org
        if section is not None:
            org[section] = funcs
            section = None
            funcs = []
    
    with open("source/octave-org.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if line.endswith(":"):
                addsec()
                section = line[:-1]
            elif line != "":
                funcs.append(line)
        addsec()
    return org
