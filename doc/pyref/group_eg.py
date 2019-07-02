import pyqplot as qp
import numpy as np

qp.figure('group', 3, 3)

qp.pen b 1
qp.plot([0 0 1],[1 0 0])

qp.group
qp.pen r
qp.at .3 .5
qp.text 0 0 Hello world
qp.at .5 .5
qp.text 0 15 More text
qp.at .7 .5
qp.text 0 30 And a third line
qp.endgroup

qp.at left top A
qp.at right top B
qp.at left bottom C
qp.at right bottom D

qp.gline({'at','C','relpaper',-5,5}, {'at','A','relpaper',-5,-5})
qp.gline({'at','B','relpaper',5,-5}, {'at','D','relpaper',5,5})
