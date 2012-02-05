qfigure('qmlegend', 3, 3);

qlegopt('x', 5, 'y', 5, 'dx', 10, 'width', 5);

qpen b
qmarker x
qmark(randn(50,1), randn(50,1));

qmlegend('1 x 1');

qpen r
qmarker +
qmark(randn(50,1)/2, randn(50,1)*2);

qmlegend('0.5 x 2');

qpen 080
qbrush none
qmarker o brush
qmark(randn(50,1)*2, randn(50,1)/2);

qmlegend('2 x 0.5');

qshrink(1, 1);
