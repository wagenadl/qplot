qfigure('qtextdist', 3, 3);

qtextdist 10
qxaxis(0, [0:5], 'Title');

qtextdist 3
qxaxis(1, [0:5], 'Title');

qtextdist -3 3
qxaxis(2, [0:5], 'Title');

qtextdist 3 -10
qxaxis(3, [0:5], 'Title');

qshrink
