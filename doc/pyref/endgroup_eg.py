import qplot as qp
import numpy as np

qp.figure('endgroup', 3, 3)

qp.pen('b', 1)
qp.plot([0, 0, 1], [1, 0, 0])

# Grouping creates a bounding box
qp.group()
qp.pen('r')
qp.at(.3, .5)
qp.text('Hello world')
qp.at(.5, .5)
qp.text('More text', dy=15)
qp.at(.7, .5)
qp.text('And a third line', dy=30)
qp.endgroup()

# Leave bread crumbs at four corners
qp.at('left', 'top', id='A')
qp.at('right', 'top', id='B')
qp.at('left', 'bottom', id='C')
qp.at('right', 'bottom', id='D')

# Use them to draw lines
qp.gline([[qp.At('C'), qp.RelPaper(-5,5)], [qp.At('A'), qp.RelPaper(-5,-5)]])
qp.gline([[qp.At('B'), qp.RelPaper(5,-5)], [qp.At('D'), qp.RelPaper(5,5)]])
