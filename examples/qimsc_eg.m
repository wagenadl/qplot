qfigure('qaxis_eg.qpt', 5, 3.5);

x = [-pi:.01:pi]*3;
xx = repmat(x,length(x),1);
yy = xx';
zz = cos(xx).*sin(yy+xx);

qlut(jet(1024));
qimsc(x,x,zz);

qtextdist -3
qcolorbar([3*pi+.5 -2*pi .5 4*pi], [], [-1 1], [-.8:.4:.8], 'Values');

qfudge(5);
