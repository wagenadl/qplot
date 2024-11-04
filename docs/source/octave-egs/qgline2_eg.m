qfigure('qgline2', 3, 3);

xx=[-1.5*pi:1.5*pi];
yy=cos(xx);
qmarker o solid
qmark(xx, yy);

qgline2('absdata',xx,yy, 'retract', 10);

