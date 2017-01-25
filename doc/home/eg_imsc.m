qfigure('eg_imsc', 2.7, 2.);

xx = [0:.1:20];
xx = repmat(xx, length(xx), 1);
yy = xx';

zz = cos(xx/2)+sin(yy/2);

cc = jet(100);

qlut(cc);

qimsc(xx, yy, zz, -2, 2);

qat 20 0
qcbar(10, [], 10, 0, 20);
qticklen 5
qcaxis([-1:1:1]*2, 'Density');
qticklen -2
qmticks([-1.5:.5:1.5]);

qshrink 1 1

qsave pdf
qsave png 120