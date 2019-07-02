import pyqplot as qp
import numpy as np

qp.figure('patch', 3, 3)
qp.brush g

qp.patch(cos(0:pi/3:2*pi), sin(0:pi/3:2*pi))

qp.brush r .5

qp.patch(sin(0:pi/3:2*pi),    cos(0:pi/3:2*pi))

