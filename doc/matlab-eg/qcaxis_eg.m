qfigure('qcaxis.qpt', 3, 3);

xx = repmat([1:10], 10, 1);
yy = xx';
zz = cos(xx).*sin(yy);
qimsc([0 0 1 1], zz, -1, 1);
qat 1 0
qcbar(10, [], 10, 0, 1);

qcaxis([-1:1:1], {'negv', '0', 'posv'});
qcaxis('l', [-1:.2:1],{});

qat 0 0
qcbarh([], 10, 0, 10, 1);
qcaxis([-1:1:1]);
qcaxis('t', [-1:.5:1],{});


qshrink
