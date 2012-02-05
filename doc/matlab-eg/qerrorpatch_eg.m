qfigure('qerrorpatch.qpt', 3, 3);

tt = [-pi:.1:pi]';

qbrush 555
qpen none

qerrorpatch(tt, sin(tt), .2*cos(tt)+.3, 5);

qpen k 1
qplot(tt, sin(tt))
