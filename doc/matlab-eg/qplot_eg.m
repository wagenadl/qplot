qfigure('qplot.qpt', 3, 3);

xx = [0:.1:2*pi];

qplot(xx, sin(xx));

yy = cos(xx);
yy(abs(yy)<.1) = nan;

qplot(xx, yy);
