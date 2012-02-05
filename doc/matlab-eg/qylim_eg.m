qfigure('qylim', 3, 3)

qpen 777
qpanel('A', 10,10,3*72-20,1.5*72-20);
qpen k
qplot(0:.1:2*pi, sin(0:.1:2*pi));
qyaxis(0, [-1:1]);

qylim -2 1.5

qpen 777
qpanel('B', 10,10+1.5*72,3*72-20,1.5*72-20);
qpen k
qplot(0:.1:2*pi, sin(0:.1:2*pi));
qyaxis(0, [-1:1]);

qylim -.8 .8

