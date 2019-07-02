import pyqplot as qp
import numpy as np

qp.figure('marker', 3, 3)

sty = { 'open', 'solid', 'brush' }
shp = '+x-|osd<>^vph'

qp.pen k
qp.brush r

for x=1:length(shp):
    for y=1:length(sty):

        qp.marker(shp(x), sty{y})

        qp.mark(x, y)

qp.shrink
