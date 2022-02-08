import sys
sys.path.append('../../..')
import numpy as np
import qplot as qp

qp.figure('tut-03');


x = np.arange(-10, 10, 0.1)

qp.pen('r', 2)
qp.plot(x, np.sin(x))
qp.pen('b', 2, pattern='dot')
qp.plot(x, np.cos(x))

qp.shrink()
qp.save('pytut-03-01.png', 96)

qp.figure('tut-03')

x = np.arange(-10, 10, 0.5)
qp.pen('r', 2)
qp.brush('955')
qp.skyline(x, np.sin(x));

qp.shrink()
qp.save('pytut-03-02.png', 96)

qp.figure('tut-03')

x = np.arange(-10, 10, 0.5)
qp.pen('none')
qp.brush('559')
qp.bars(x, np.sin(x), 0.33)

qp.shrink()
qp.save('pytut-03-03.png', 96)
