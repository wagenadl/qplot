qfigure('eg_gline', 1.8, 2.);
xx=[-1.5*pi:1.5*pi];
yy=cos(xx);
qmarker o solid 3
qmark(xx, yy);
N=length(xx)-1;

qpen 777
for n=1:N
    qgline({'absdata',xx(n),yy(n), 'retract', 5}, ...
            {'absdata',xx(n+1),yy(n+1), 'retract', 5});
end

qshrink
qsave pdf
qsave png 120