import qplot as qp
import numpy as np

qp.figure('luts.families', 4.5, 4.5)

fams = qp.luts.families()
y = 0
for fam in fams:
    names = qp.luts.family(fam)
    if len(names):
        name = names[0]
        cc = qp.luts.get(name)
        L,C = cc.shape
        qp.image(cc.reshape(1,L,C), rect=[0, y, 1, .5])
        qp.at(0, y+.25)
        qp.align('right', 'middle')
        qp.text(f"{name} ({fam})", dx=-5)
        y -= 1
