qfigure('qcbar.qpt', 3, 3);

xx = repmat([1:10], 10, 1);
yy = xx';
zz = cos(xx).*sin(yy);
qimsc([0 0 1 1], zz, -1, 1);
qcbard([1.1 0 .1 1]);
qcaxis([-1:1:1], {'negv', '0', 'posv'});

qcbard([0 1.1 1 .1],'h');
qcaxis([-1:1:1], {'negv', '0', 'posv'});

qshrink
