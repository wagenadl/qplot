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


import sys
import os
import glob
import pyqplot as qp

egs = glob.glob('html/pyref/*.html')

funcs = [k for k,v in qp.__dict__.items() if callable(v)]

ok = True
for f in funcs:
    if f==f.lower() and f.find('__')<0:
        if not ('html/pyref/%s.html' % f) in egs:
            print('Not documented by example: %s' % f)
            ok = False

if not ok:
    sys.exit(1)
