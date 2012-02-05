qfigure('qdarrow.qpt', 3, 3);

tt = [0:.1:4*pi];
xx = sin(tt/2);
yy = sin(tt);
qpen 666
qplot(xx, yy);

qbrush k
qpen k

for n=5:10:length(xx)
  qdarrow(xx(n), yy(n), [xx(n)-xx(n-1), yy(n)-yy(n-1)]);
end
