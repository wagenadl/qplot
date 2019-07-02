import pyqplot as qp
import numpy as np

qp.figure('gimage', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
img = cat(3, xx/10, yy/10, .5+0*xx)

qp.gimage([nan nan 0 0], [.5 .5 2 2]*72, img)

