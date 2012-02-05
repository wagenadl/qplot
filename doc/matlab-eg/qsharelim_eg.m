qfigure('qsharelim', 3, 3);

id=qsubplot(0, 0, 1, .5);
qplot(1:100, sqrt(1:100));
qxaxis(0,[0:50:100]);
qyaxis(0,[0:2:10]);
qshrink

qsubplot(0, .5, 1, .5);
qplot(51:150, 20+2*cos([51:150]/10));
qaxshift 5
qxaxis(18,[50:50:150]);
qyaxis(50,[18:2:22]);
qshrink

qsharelim(id);
