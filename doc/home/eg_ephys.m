x = vscope_load('data/003.xml', 'a');

idx = [3.3e4:3.8e4];

yy = x.analog.dat(idx, 1);
xx = x.analog.dat(idx, 2);
tt = [1:length(yy)]/1e4;

yy(xx>.5) = yy(xx>.5) - 50;

qfigure('eg_ephys', 3, 2.5);

qpen k 0
qbrush k
qecoplot(tt, yy, 1000);

qpen k 1.5
qaxshift 20
qxaxis(yy(end),tt(end)-[.05 0],[],'50 ms');

qplot(tt(end)+[0 0], yy(end)+10+[0 20]);
qat(tt(end), yy(end)+10+10);
qalign middle right
qtext -5 0 '20 mV'

qpen 555 0
qplot(tt, min(yy)-10+5*xx);

qpen 1.5
qplot(tt(end)+[0 0], min(yy)-[0 5]);
qat(tt(end), min(yy)-2.5);
qalign middle right
qtext -5 0 '1 nA'

qshrink
qsave pdf
qsave png 120
