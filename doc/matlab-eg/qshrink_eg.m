qfigure('qshrink_eg.qpt', 3, 3);

qbrush 888
qpen none
qpanel('A', [.25 .25 2.5 1]*72);
qpen k solid
qplot(0:.1:2*pi,sin(0:.1:2*pi))
qxaxis(-1,[0 pi 2*pi],{'0','π','2π'})
qyaxis(0,-1:1);

qbrush 888
qpen none
qpanel('B', [.25 1.75 2.5 1]*72);
qpen k solid
qplot(0:.1:2*pi,sin(0:.1:2*pi))
qxaxis(-1,[0 pi 2*pi],{'0','π','2π'})
qyaxis(0,-1:1);

qshrink
