qfigure('qyaxis', 3, 3);

qyaxis(0, [0:5]);

qyaxis(1, [0:5], {'zero', 'one', 'two', 'three', 'four', 'five'});

qyaxis(2, [0:5], []);

qyaxis('r', 3, [0:5], 'right orientation')

qyaxis('R', 4, [0 5], [1:4], 'flipped title')

qshrink
