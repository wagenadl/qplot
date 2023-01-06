qfigure('qvcbar', 3, 3);

xx = repmat([1:10], 10, 1);
yy = xx';
zz = cos(xx).*sin(yy);
qimsc([0 0 1 1], zz, -1, 1);
qaxshift 5
qvcbar(1, 0, 1);
qaxshift 0
qcaxis([-1:1:1], {'negative', '0', 'positive'});

qshrink(1, 1);
