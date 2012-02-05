qfigure('qgarea.qpt', 3, 3);

qplot([-pi:.1:pi],sin(-pi:.1:pi));

qpen none
qbrush r .5

qgarea({'absdata', 0, 0}, ...
    {'absdata', 0, 0, 'relpaper', 0, 36}, ...
    {'absdata', 1, sin(1), 'relpaper', 0, 36}, ...
    {'absdata', 1, sin(1)});

    