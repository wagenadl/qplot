qfigure('qgline.qpt', 3, 3);

xx=[-1.5*pi:1.5*pi];
yy=cos(xx);
qmarker o solid
qmark(xx, yy);

N=length(xx)-1;
for n=1:N
  qgline({'absdata',xx(n),yy(n), 'retract', 10}, ...
      {'absdata',xx(n+1),yy(n+1), 'retract', 10});
end
