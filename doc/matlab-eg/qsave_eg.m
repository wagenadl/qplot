qfigure('qsave.qpt', 3, 3);

qplot(0:.1:2*pi,sin(0:.1:2*pi));

qsave('qsave.pdf');
qsave('qsave.ps');
qsave('qsave.png');
qsave('qsave.jpg');
qsave('qsave.svg');
