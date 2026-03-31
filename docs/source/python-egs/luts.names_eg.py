import qplot as qp
import numpy as np

qp.figure('luts.names', 3.5, 3.5)
qp.font(size=8)
names = qp.luts.names()
N = len(names)
C = 5
R = int(np.ceil(N/C))
c = 0
r = 0
for n in range(N):
    qp.at(c, -r)
    qp.text(names[n].replace("_", "\\_"))
    r += 1
    if r>=R:
        r = 0
        c += 1
qp.shrink()
        

