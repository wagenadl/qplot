qfigure('qcaligraph', 3, 3)

qplot([0 1], [0 0]);
qplot([0 0], [0 1]);
qplot([0 -1/3], [0 -2/3]);

qshrink(1,1);

phi = [-.9*pi:.1:.9*pi];
xx = sin(phi);
yy = -cos(phi);
ww = 1.5*(1-yy);
xx=xx/10;
yy=1+yy/30;

qcaligraph(xx, yy, ww);

qat(xx(end), yy(end), xx(end)-xx(end-1), yy(end)-yy(end-1));
qbrush k
qarrow(6,4,-2,1.5);
