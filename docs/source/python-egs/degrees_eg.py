import qplot as qp
import numpy as np

qp.figure('degrees', 3, 3)

qp.patch([-1, 1, 1, -1], [-1, -1, 1, 1])

qp.degrees()

for a in [0, 90, 180, 270]:
    qp.at(0, 0, phi=a)
    qp.align('left', 'middle')
    qp.text(f"{a}°", dx=10)

qp.shrink()
