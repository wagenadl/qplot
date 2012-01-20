qfigure('qaxis_eg.qpt', 5, 3.5);

x = [-pi:.01:pi]*3;
xx = repmat(x,length(x),1);
yy = xx';
zz = cos(xx).*sin(yy+xx);

qlut(jet(1024));
qimsc(x,x,zz);



qat(3*pi,3*pi)
qcbar(72/6,72,72/4,0)
qcaxis([-1:.5:1],'Values');
qcaxis('l',[-.8:.4:.8],'Color');


qat(3*pi,-3*pi)
qcbar(72/6,-72,72/4,0)



qfudge
return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


xywh = [3*pi+4 -2*pi .5 4*pi];
qcbar(xywh);
qaxshift 3
qcaxis([-1:.5:1],'Values');

qnumfmt '%.2f'
qaxshift -.001
qcaxis([nan nan],[-.8:.4:.8],'Color');


xywh = [-2*pi -3*pi-4 4*pi .5];
qcbar(xywh,'h');
qaxshift 3
qcaxis([-1:.5:1],'Values');

qnumfmt '%.2f'
qaxshift -.001
qticklen -2
qcaxis([nan nan],[-.8:.4:.8],'Color');
qpen w 1
qcaxis([nan nan],[-.8:.4:.8],[])



qfudge(5);
