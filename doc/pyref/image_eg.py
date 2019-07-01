import pyqplot.all as qp

qp.figure('image', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
img = cat(3, xx/10, yy/10, .5+0*xx)

qp.image([0, 0, 1, 1], img)

