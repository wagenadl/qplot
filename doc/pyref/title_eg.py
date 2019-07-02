import pyqplot as qp
import numpy as np

qp.figure('title', 3, 3)

qp.plot(0:.1:2*pi, sin(0:.1:2*pi))

qp.title 'Sine wave'

qp.shrink
