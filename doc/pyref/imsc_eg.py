import pyqplot.all as qp

qp.figure('imsc', 3, 3)

xx = repmat([1:10], 10, 1)
yy = xx'
zz = cos(xx)+sin(yy)
cc = jet(100); # In octave, this inappropriately opens a native window
qp.lut(cc);

qp.imsc(xx, yy, zz)

