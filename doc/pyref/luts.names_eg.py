import qplot as qp
import numpy as np

qp.figure('luts.names', 3.5, 3)

names = qp.luts.names()
N = len(names)
C = 4
R = int(np.ceil(N/C))
c = 0
r = 0
for n in range(N):
    if r==0:
        qp.subplot(1,C,c)
    qp.at(0, r)
    qp.text(names[n].replace("_", "\\_"))
    r = r + 1
    if r>=R:
        r = 0
        c = c + 1
        qp.shrink()
qp.shrink()
        

