qfigure('qpmark', 3, 3);

xx = [1 2 3];
yy = [3 .5 1.5];
qbrush 555
qbars(xx, yy, .5);

mrks='+-x';
for k=1:3
  qat(xx(k), yy(k));
  qmarker(mrks(k));
  qpmark(0,-10);
end
