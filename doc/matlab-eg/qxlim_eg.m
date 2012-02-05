qfigure('qxlim', 3, 3)

qpen 777
qpanel('A', 10,10,3*72-20,1.5*72-20);
qpen k
qplot(0:.1:2*pi, sin(0:.1:2*pi));
qxaxis(-1, [0 pi 2*pi], {'0','π','2π'});

qxlim -5 10

qpen 777
qpanel('B', 10,10+1.5*72,3*72-20,1.5*72-20);
qpen k
qplot(0:.1:2*pi, sin(0:.1:2*pi));
qxaxis(-1, [0 pi 2*pi], {'0','π','2π'});
qxlim 1 6

