qfigure('qxaxis', 3, 3);

qxaxis(0, [0:5]);

qxaxis(1, [0:5], {'zero', 'one', 'two', 'three', 'four', 'five'});

qxaxis(2, [0:5], 'x-axis');

qxaxis(3, [0 5], [1:4]);

qxaxis(4, [0:5], {});

qxaxis('t', 5, [0:5], 'top orientation')

qshrink
