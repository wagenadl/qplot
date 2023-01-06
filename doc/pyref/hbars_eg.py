import qplot as qp
import numpy as np

qp.figure('hbars', 3, 3)
qp.brush('777')

yy = np.arange(0, 7)
qp.hbars(yy, np.sin(yy/2), 0.5)
qp.yaxis('', yy, ["One", "Two", "Three", "Four", "Five", "Six", "Seven"], lim=[-.4, 6.4])
