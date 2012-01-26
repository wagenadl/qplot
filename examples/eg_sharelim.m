qfigure('eg_sharelim.qpt', 7, 3)

id=qsubplot(0.2,0,.7,.5);
qplot([1 2 3],[1 3 2])
qxaxis(1,[1:3])
qyaxis(1,[1:3])
qshrink

qsubplot(0,.5,1,.5)
qplot([0 1 2],[3 3 2])
qxaxis(2,[0:2])
qyaxis(0,[2:3])
qshrink

qsharelim('x', id);
qsharelim('y', id);

qfigure('eg_sharelim2.qpt', 7, 3)

id=qsubplot(0,0.2,.5,.7);
qplot([1 2 3],[1 3 2])
qxaxis(1,[1:3])
qyaxis(1,[1:3])
qshrink

qsubplot(.5,0,.5,1);
qplot([0 1 2],[3 3 2])
qxaxis(2,[0:2])
qyaxis(0,[2:3])
qshrink

qsharelim('x', id);
qsharelim('y', id);

