qfigure('qlut', 3, 3);

xx=repmat(2*pi*[0:100]/100,101,1);
yy=xx';
zz=cos(xx)+sin(yy);

qimsc([0 0 1 1], zz);
qat 1 0
qcbar(10,[],10,0,1);

qlut(jet)

qimsc([0 1.1 1 1], zz);
qat 1 1.1
qcbar(10,[],10,0,1);

qlut(hsv)

qimsc([1.5 0 1 1], zz);
qat 2.5 0
qcbar(10,[],10,0,1);

qlut(hot)

qimsc([1.5 1.1 1 1], zz);
qat 2.5 1.1
qcbar(10,[],10,0,1);


qshrink 1
