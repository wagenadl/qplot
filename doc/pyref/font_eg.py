import pyqplot.all as qp

qp.figure('font', 3, 3)

qp.patch([0 1 1 0], [0 0 1 1])

qp.font Helvetica 10

qp.at .2 .2
qp.text 0 0 Helvetica Roman

qp.font Times bold 12

qp.at .8 .8
qp.text 0 0 Times Bold

qp.font BitstreamCharter italic 12
qp.at .2 .8
qp.text 0 0 Charter Italic

qp.font Times italic 12
qp.text 0 14 Times Itali
