import pyqplot.all as qp

qp.figure('lut', 3, 3)

xx=repmat(2*pi*[0:100]/100,101,1)
yy=xx'
zz=cos(xx)+sin(yy)

qp.imsc([0 0 1 1], zz)
qp.at 1 0
qp.cbar(10,[],10,0,1)

qp.lut(jet)

qp.imsc([0 1.1 1 1], zz)
qp.at 1 1.1
qp.cbar(10,[],10,0,1)

qp.lut(hsv)

qp.imsc([1.5 0 1 1], zz)
qp.at 2.5 0
qp.cbar(10,[],10,0,1)

qp.lut(hot)

qp.imsc([1.5 1.1 1 1], zz)
qp.at 2.5 1.1
qp.cbar(10,[],10,0,1)


qp.shrink 1
