qfigure('qtext', 3, 3);

qfont Helvetica 15
qalign base left
qat 0 1
qylim 0 1.5
qxlim -.5 1

qtext 0 0 sin(/x/) = (e^/ix/ ~– e^–/ix/ ) / 2
qtext 0 30 l’Hôpital
qtext 0 60 *F* = /m/ *a*
qtext 0 90 a^x~+~y ~ 2^3^5 b
% Current syntax doesn't allow for continuation of nested superscripts, 
% but some cases have solutions:
qtext 0 120 e^–½ (/x/ ²~+~/y/ ²)
% Note the unicode thin spaces in the last example.

qshrink
