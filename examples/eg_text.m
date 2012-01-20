qfigure('eg_text.qpt', 5, 3.5);

qpen 955
qplot([-1 1],[0 0]);
qplot([0 0],[-1 1]);

qfont Helvetica 10
qpen k

qat 0 .8
qalign base

qalign left
qtext 0 0 left
qalign center
qtext 0 12 center
qalign right
qtext 0 24 right

qat -.8 0
qalign center

qalign top
qtext 0 0 (top)
qalign middle
qtext 50 0 (middle)
qalign bottom
qtext 100 0 (bottom)
qalign base
qtext 150 0 (base)

qalign base left
qat 0.1 -.2
qtext 0 0 sin(/x/) = (e^/ix/ ~– e^–/ix/ ) / 2
qtext 0 15 l’Hôpital
qtext 0 30 *F* = /m/ *a*
qtext 0 45 a^x~+~y ~ b^3
