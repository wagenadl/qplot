qfigure('qendgroup_eg.qpt', 3, 3);

qpen b 1
qplot([0 0 1],[1 0 0]);

qgroup
qpen r
qat .3 .5
qtext 0 0 Hello world
qat .5 .5
qtext 0 15 More text
qat .7 .5
qtext 0 30 And a third line
qendgroup

qat left top A
qat right top B
qat left bottom C
qat right bottom D

qgline({'at','C','relpaper',-5,5}, {'at','A','relpaper',-5,-5});
qgline({'at','B','relpaper',5,-5}, {'at','D','relpaper',5,5});