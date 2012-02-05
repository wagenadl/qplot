qfigure('qreftext', 3, 3);

qpen 666
qplot([0 1],[0 0]);
qplot([0 1],[.5 .5]);
qplot([0 1],[2 2]);
qplot([0 1],[1.5 1.5]);

qpen k
qfont Helvetica 15
qalign top

qat .25 2
qtext 0 0 Without
qat .5 2
qtext 0 0 a
qat .75 2
qtext 0 0 reference

qreftext('With a reference');

qat .25 1.5
qtext 0 0 With
qat .5 1.5
qtext 0 0 a
qat .75 1.5
qtext 0 0 reference

qreftext('');

qalign bottom

qat .25 0.5
qtext 0 0 Baseline
qat .75 .5
qtext 0 0 wobbly

qreftext('Baseline not wobbly');

qat .25 0
qtext 0 0 Baseline
qat .5 0
qtext 0 0 not
qat .75 0
qtext 0 0 wobbly


qshrink
