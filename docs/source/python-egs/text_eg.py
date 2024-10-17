import qplot as qp
import numpy as np

qp.figure('text', 3, 3)

qp.font('Times', 15)
qp.align('base', 'left')
qp.at(0, .5)
qp.xlim(0, 1)
qp.ylim(0, 1)

qp.text('sin(/x/) = (e^/ix/ - e^-/ix/) / 2')
qp.text('l’Hôpital', dy=30)
qp.text('*F* = /m/ *a*', dy=60)
qp.text('/a/_x^2 + /y/_{/k/_1}^3/2', dy=90)
qp.text('2^{3^5} /b/_[2]^{\\,\\,{1}}', dy=120)
qp.text('e^-½\\,(/x/^2 + /y/^2)', dy=150)
qp.text('frown^{:(} or smile^{:)}', dy=180)

qp.shrink(10)
