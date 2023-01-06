qfigure('qylim', 3, 3)

qpen 777
qpanel('A', 20,20,3*72-30,1.5*72-40);
qpen k
qplot(0:.1:2*pi, sin(0:.1:2*pi));
qyaxis(0, [-1:1]);

qylim -2 1.5

qpen 777
qpanel('B', 20,20+1.5*72,3*72-30,1.5*72-40);
qpen k
qplot(0:.1:2*pi, sin(0:.1:2*pi));
qyaxis(0, [-1:1]);

qylim -.8 .8

qpanel -
