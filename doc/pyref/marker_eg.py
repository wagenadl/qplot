import qplot as qp
import numpy as np

qp.figure('marker', 3, 3)

sty = [ 'open', 'solid', 'brush' ]
shp = '+x-|osd<>^vph'

qp.pen('k')
qp.brush('r')

for x in range(len(shp)):
    for y in range(len(sty)):
        qp.marker(shp[x], fill=sty[y])
        qp.mark(x, y)

