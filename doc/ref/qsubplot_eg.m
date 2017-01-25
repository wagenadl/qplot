qfigure('qsubplot', 3, 3)

qsubplot(0, 0, 1, .5);

qplot(0:.1:2*pi, cos(0:.1:2*pi))
qshrink 10

qsubplot(0, .5, 1, .5);

qplot(0:.1:2*pi, sin(0:.1:2*pi))
qshrink 10
