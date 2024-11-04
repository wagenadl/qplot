qfigure('qoverline', 3, 3);

xx = [1 2];
yy = [3 4];
dy = [.5 .75];
qbars(xx, yy, .5);
qerrorbar(xx, yy, dy);

qoverline(xx, max(yy+dy), '*');

xx = [3.5 4.5];
qbars(xx, yy, .5);
qerrorbar(xx, yy, dy);

qoverline(xx, yy+dy, '+');

qshrink
