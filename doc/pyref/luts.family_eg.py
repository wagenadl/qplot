import qplot as qp
import numpy as np

qp.figure('luts.family', 3, 3)

names = qp.luts.family("native")
N = len(names)
for n in range(N):
    cc = qp.luts.get(names[n], 1024)
    L,C = cc.shape
    qp.image(cc.reshape(1,L,C), rect=[0, n, 1, .5])
    qp.at(0, n+.3)
    qp.align('right', 'middle')
    qp.text(names[n], dx=-5)

