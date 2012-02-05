qfigure('qcbarh.qpt', 3, 3);

xx = repmat([1:10], 10, 1);
yy = xx';
zz = cos(xx).*sin(yy);
qimsc([0 0 1 1], zz, -1, 1);
qat 0 0
qcbarh(2.5*72, 10, 25, 5);

qcaxis([-1:1:1], {'negv', '0', 'posv'});

qshrink
