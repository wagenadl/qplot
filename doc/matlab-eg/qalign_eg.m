qfigure('qalign', 3, 3)

qpen 777
qplot([-1 1], [0 0]);
qplot([-1 1], [.5 .5]);
qplot([-1 1], [-.5 -.5]);

qplot([0 0], [-1 1]);
qplot([.5 .5], [-1 1]);
qplot([-.5 -.5], [-1 1]);

qpen k

qat 0 0
qalign center middle
qtext 0 0 Center/Middle

qat 0.5 0
qalign left base
qtext 0 0 Left/Base

qat -.5 0
qalign right
qtext 0 0 Right/Base

qat 0 .5
qalign bottom center
qtext 0 0 Bottom

qat 0 -.5
qalign top center
qtext 0 0 Top
