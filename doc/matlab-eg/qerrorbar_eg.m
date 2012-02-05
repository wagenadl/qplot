qfigure('qerrorbar.qpt', 3, 3);

tt = [-pi:.5:pi]';

qmarker o solid
qmark(tt, sin(tt))

qerrorbar(tt, sin(tt), .2*cos(tt)+.3, 5);

qmarker o solid
qmark(tt, 2+sin(tt-1))

qerrorbar(tt, 2+sin(tt-1), [.3+zeros(size(tt)), .2*cos(tt)+.3]);
