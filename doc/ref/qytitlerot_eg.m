qfigure('qytitlerot', 3, 3);

qytitlerot 1
qyaxis(0, [0:5], 'Normal')

qytitlerot 0
qyaxis(1, [0:5], 'Upright')

qytitlerot -1
qyaxis(2, [0:5], 'Reverse')

qyaxis(3, [0:5]);
qat left 5
qalign right middle
qreftext '5'
qtext(-5, 0, 'Manual')

qshrink
