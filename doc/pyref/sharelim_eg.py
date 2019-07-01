import pyqplot.all as qp

qp.figure('sharelim', 3, 3)

id=qp.subplot(0, 0, 1, .5)
qp.plot(1:100, sqp.rt(1:100))
qp.xaxis(0,[0:50:100])
qp.yaxis(0,[0:2:10])
qp.shrink

qp.subplot(0, .5, 1, .5)
qp.plot(51:150, 20+2*cos([51:150]/10))
qp.axshift 5
qp.xaxis(18,[50:50:150])
qp.yaxis(50,[18:2:22])
qp.shrink

qp.sharelim(id)
