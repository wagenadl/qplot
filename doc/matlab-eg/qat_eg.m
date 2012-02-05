qfigure('qat.qpt', 3, 3)
qplot([0 1 2 3 4], [0 1 4 2 5]);
qalign top left

qat(1, 1);
qtext(3, 3, 'one');

qat(2, 4, -pi/4);
qtext(3, 3, 'two');
qat right bottom A

qat(3, 2, (4-3), (5-2));
qtext(3, 3, 'three');

qat A
qtext(3, 3, 'four');
