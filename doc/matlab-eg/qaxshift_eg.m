qfigure('axshift', 3, 3);
qplot([-pi:.1:pi], sin([-pi:.1:pi]));

qaxshift 10

qxaxis(-1, [-pi 0 pi], {'π', '0', 'π'});
qyaxis(-pi,[-1:1]);
qshrink
