#!/usr/bin/python3

import os
import glob
import time

today = time.asctime(time.localtime(time.time()))

os.chdir('../src')
srcs = glob.glob('*.cpp')
hdrs = glob.glob('*.h')
srcs.sort()
hdrs.sort()
with open('CMakeLists.txt', 'w') as ofd:
    ofd.write(f"""# src/CMakeLists.txt - Part of qplot
# Automatically generated by tools/updatesources.py
# Last update: {today}
# Manual edits will be lost

""")

    ofd.write("set(SOURCES\n")
    for src in srcs:
        ofd.write(f'  "{src}"\n')
    ofd.write(")\n\n")

    ofd.write("set(HEADERS\n")
    for hdr in hdrs:
        ofd.write(f'  "{hdr}"\n')
    ofd.write(")\n")

    
    
