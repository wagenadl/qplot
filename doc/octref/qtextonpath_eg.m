qfigure('qtextonpath', 3, 3);

xx = [0:.01:10];
yy = cos(xx);
qpen 1
qplot(xx, yy);
qylim -10 10
qfont Helvetica 14

qalign center base
qtextonpath(xx, yy, -3, 'This text follows the curve');

qshrink
