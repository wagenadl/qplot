qfigure('qnumfmt.qpt', 3, 3);

qxaxis(0, [0:.5:2]);

qnumfmt('%.1f')
qyaxis(0, [0:.5:2]);

qnumfmt('%.3f')
qyaxis(.75,[0.5:.125:1])

qnumfmt('')
qyaxis(1.5,[0.5:.125:1])