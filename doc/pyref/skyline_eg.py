import pyqplot as qp
import numpy as np

qp.figure('skyline', 3, 3)
xx=[0:.05:1].^2*2*pi
yy=sin(xx)
qp.brush 666

qp.skyline(xx, yy)
