import qplot as qp
import numpy as np
import inspect
import re


def qplotfunctions():
    funcs = [k for k, v in qp.__dict__.items()
             if callable(v) and not k.startswith("_")]
    for k, v in qp.luts.__dict__.items():
        if callable(v) and not k.startswith("_"):
            funcs.append("luts." + k)
    return [k for k in funcs if k==k.lower()]


_funcs = qplotfunctions()


def qpfunction(funcname):
    obj = qp
    for fn in funcname.split("."):
        obj = obj.__dict__[fn]
    return obj


def docstring(funcname):
    obj = qpfunction(funcname)
    try:
        return obj.__doc__
    except AttributeError:
        return ""
    

def tagline(funcname):
    doc = docstring(funcname)
    if not doc.startswith(funcname.upper()):
        raise ValueError(f"Unexpected tagline for {funcname}: {doc}")
    title = doc.split("\n")[0]
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
    try:
        idx = doc.index("\n")
        return doc[idx+1:]
    except ValueError:
        return ""
    

def loadexample(funcname, root):
    try:
        with open(f"{root}/{funcname}_eg.py") as f:
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
    
    with open("source/python-org.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if line.endswith(":"):
                addsec()
                section = line[:-1]
            elif line != "":
                funcs.append(line)
        addsec()
    return org
