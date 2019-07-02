import pyqplot as qp
import numpy as np

qp.figure('select_one')
qp.plot(0:.1:2*pi, sin(0:.1:2*pi))

qp.figure('select_two')
qp.plot(0:.1:2*pi, cos(0:.1:2*pi))

qp.select('select_one')
qp.plot(0:.1:2*pi, -sin(0:.1:2*pi))
