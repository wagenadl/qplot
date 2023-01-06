#!/usr/bin/python3

import numpy as np
import qplot as qp

qp.figure('eg_bars', 3, 2.5)

yy = np.array([[1.3, 1.5], [0.6, 0.7], [1.25, 1.4]])

qp.legopt(x0=2.6, y0=1.5)

qp.brush('955')
qp.pen('none')
qp.bars(np.arange(3) - .2, yy[:,0], .3)
qp.plegend('Trial A')

qp.brush('559')
qp.bars(np.arange(3) + .2, yy[:,1], .3)
qp.plegend('Trial B')

qp.pen('k', 0)
qp.xcaxis('', np.arange(3), ['Baseline', 'Expt.', 'Wash'])
qp.yaxis('Activity', qp.arange(0, 1.5, .5), x=-.5)

ym = np.max(yy, 1)
dy = [ np.nan, 5, 30]
txt = ['', '**', 'n.s.']
for k in [1, 2]:
    qp.shiftedline(0+.35*np.array([-1, 1]), ym[0], 0, -dy[k])
    qp.shiftedline(k+.35*np.array([-1, 1]), ym[k], 0, -dy[k])
    qp.shiftedline(np.array([0, 0, k, k]), ym[[0,0,0,k]],
                   0, -dy[k] - np.array([0, 10, 10, 0]))
    qp.at(np.mean([0, k]), np.max(ym[[0,k]]))
    qp.align('center', 'bottom')
    qp.text(txt[k], dy=-dy[k]-12)
    
qp.shrink()

qp.save('pdf')

