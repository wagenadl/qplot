qfigure('qselect_one');
qplot(0:.1:2*pi, sin(0:.1:2*pi));

qfigure('qselect_two');
qplot(0:.1:2*pi, cos(0:.1:2*pi));

qselect('qselect_one')
qplot(0:.1:2*pi, -sin(0:.1:2*pi));