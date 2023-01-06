qfigure('qpanel', 3, 3);
xx=[0:.01:3*pi];

qplot(xx, sin(xx));
qshrink 1

qpen dash
qbrush 777

qpanel('B', [2.1 2.3 .9 .7]*72);

qpen solid
qplot(xx, cos(xx));
qshrink 5
