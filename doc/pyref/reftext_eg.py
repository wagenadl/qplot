import pyqplot as qp
import numpy as np

qp.figure('reftext', 3, 3)

qp.pen 666
qp.plot([0 1],[0 0])
qp.plot([0 1],[.5 .5])
qp.plot([0 1],[2 2])
qp.plot([0 1],[1.5 1.5])

qp.pen k
qp.font Helvetica 15
qp.align top

qp.at .25 2
qp.text 0 0 Without
qp.at .5 2
qp.text 0 0 a
qp.at .75 2
qp.text 0 0 reference

qp.reftext('With a reference')

qp.at .25 1.5
qp.text 0 0 With
qp.at .5 1.5
qp.text 0 0 a
qp.at .75 1.5
qp.text 0 0 reference

qp.reftext('')

qp.align bottom

qp.at .25 0.5
qp.text 0 0 Baseline
qp.at .75 .5
qp.text 0 0 wobbly

qp.reftext('Baseline not wobbly')

qp.at .25 0
qp.text 0 0 Baseline
qp.at .5 0
qp.text 0 0 not
qp.at .75 0
qp.text 0 0 wobbly


qp.shrink
