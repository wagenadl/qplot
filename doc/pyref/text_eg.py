import qplot as qp
import numpy as np

qp.figure('text', 3, 3)

qp.font('Helvetica', 15)
qp.align('base', 'left')
qp.at(0, 1)
qp.ylim(0, 1.5)
qp.xlim(-.5, 1)

qp.text('sin(/x/) = (e^/ix/ ~– e^–/ix/ ) / 2')
qp.text('l’Hôpital', dy=30)
qp.text('*F* = /m/ *a*', dy=60)
qp.text('a^x~+~y ~ 2^3^5 b', dy=90)
# Current syntax doesn't allow for continuation of nested superscripts,
# but some cases have solutions:
qp.text('e^–½ (/x/ ²~+~/y/ ²', dy=120)
# Note the unicode thin spaces in the last example.

