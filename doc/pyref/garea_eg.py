import pyqplot.all as qp

qp.figure('garea', 3, 3)

qp.plot([-pi:.1:pi],sin(-pi:.1:pi))

qp.pen none
qp.brush r .5

qp.garea({'absdata', 0, 0}, ...
        {'absdata', 0, 0, 'relpaper', 0, 36}, ...
        {'absdata', 1, sin(1), 'relpaper', 0, 36}, ...
        {'absdata', 1, sin(1)})


