qfigure('qmticks.qpt', 3, 3);

qplot(0:.1:2*pi, sin(0:.1:2*pi));
qaxshift 10
qticklen 5
qxaxis(-1, [0 pi 2*pi], {'0', 'π', '2π'});
qticklen 3

qmticks([0:pi/4:2*pi]);

qshrink
