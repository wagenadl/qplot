qfigure('eg_imsc.qpt', 5, 3.5);

x = [-pi:.01:pi]*3;
xx = repmat(x,length(x),1);
yy = xx';
zz = cos(xx).*sin(yy+xx);

qlut(jet(1024));
qimsc(x,x,zz);

qaxshift 2

qat(3*pi,3*pi)
qcbar(72/6,72,72/2,0)
qcaxis([-1:.5:1],'Values');
qcaxis('l',[-.8:.4:.8],'Color');


qat(3*pi,-3*pi)
qcbar(72/6,-72,.75*72,0,'d')
qytitlerot -1
qcaxis([-1:.5:1],'Values');
qytitlerot 0
qcaxis('l',[-.8:.4:.4],'Color');

qat(-3*pi,3*pi)
qcbarh(72,72/6,0,-.75*72);
qcaxis([-1:.5:1],'Values');
qcaxis('t',[-.8:.8:.8],'Color');

qat(3*pi,3*pi)
qcbarh(-72,72/6,0,-.75*72,'l');
qcaxis([-1:.5:1],'Values');
qcaxis('t',[-.8:.8:.8],'Color');

qat(-pi,3*pi)
qticklen 0
qaxshift 0
qcbarh(0,72/6,0,-.75*72,2*pi)
qcaxis([],[-1:.5:1],'Values');

qpen w 1
qaxshift(-72/6/4)
qticklen(-72/6/2)
qcaxis([],[-.5:.5:.5],[])
%
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
