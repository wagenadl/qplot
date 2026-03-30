#!/usr/bin/python3

import glob
import re

re_from = re.compile(r"^(\s*)from (.*) import (.*)\s*$")
re_bare = re.compile(r"^(\s*)import (.*)\s*$")

mods = glob.glob("python/*.py")

uni = set()
for m in mods:
    uni.add(m.split("/")[-1][:-3])


def transformline(line):
    mtch = re_from.match(line)
    if mtch:
        spc = mtch.group(1)
        src = mtch.group(2)
        obj = mtch.group(3)
        if src in uni:
            if src == "range":
                src = "range_"
            return f"{spc}from .{src} import {obj}\n"
        else:
            return line
    mtch = re_bare.match(line)
    if mtch:
        spc = mtch.group(1)
        src = mtch.group(2)
        if src in uni:
            if src == "range":
                src = "range_"
            return f"{spc}from . import {src}\n"
        else:
            return line
    return line
    
    
def transformfile(fn):
    with open(fn, 'r') as fd:
        lines = fd.readlines()
    out = []
    for line in lines:
        if "import" in line:
            out.append(transformline(line))
        else:
            out.append(line)
    with open(fn, 'w') as fd:
        for line in out:
            fd.write(line)

def main():
    for m in mods:
        transformfile(m)

        
if __name__ == "__main__":
    main()
