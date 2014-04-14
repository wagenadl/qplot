qfigure('eg_legend.qpt', 5, 3);

qlegopt('x0', 2*pi, 'y0', 1, 'dx', 18);
xx = [0:.01:2*pi];

qpen b 1
qplot(xx, cos(xx));
qlegend('cosine');

qpen r 1
qplot(xx, sin(xx));
qlegend('sine');

qmarker o solid 4
qpen g 0
qmark(randn(10,1)+pi, randn(10,1)/3);
qmlegend('random');

qpen k 0
qbrush 666
qbars([.1:.2:1.9]*pi,.2*sin([.1:.2:1.9]*pi*2),.5)
qplegend('bars');
qpen none
qbrush b
qplegend('more');

qpen k 0
qaxshift 5
qxaxis(-1,[0 pi 2*pi],{'0','pi','2pi'});
qyaxis(0,[-1:1]);
qshrink