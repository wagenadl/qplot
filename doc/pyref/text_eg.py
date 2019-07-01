import pyqplot.all as qp

qp.figure('text', 3, 3)

qp.font Helvetica 15
qp.align base left
qp.at 0 1
qp.ylim 0 1.5
qp.xlim -.5 1

qp.text 0 0 sin(/x/) = (e^/ix/ ~– e^–/ix/ ) / 2
qp.text 0 30 l’Hôpital
qp.text 0 60 *F* = /m/ *a*
qp.text 0 90 a^x~+~y ~ 2^3^5 b
# Current syntax doesn't allow for continuation of nested superscripts,
# but some cases have solutions:
qp.text 0 120 e^–½ (/x/ ²~+~/y/ ²)
# Note the unicode thin spaces in the last example.

qp.shrink
