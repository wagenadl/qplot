import pyqplot as qp
import numpy as np

qp.figure('font', 3, 3)

qp.patch([0, 1, 1, 0], [0, 0, 1, 1])

qp.font('Helvetica', 10)

qp.at(.2, .2)
qp.text('Helvetica Roman')

qp.font('Times', 12, bold=True)

qp.at(.8, .8)
qp.text('Times Bold')

qp.font('BitstreamCharter', 12, italic=True)
qp.at(.2, .8)
qp.text('Charter Italic')

qp.font('Times', 12, italic=True)
qp.text('Times Italic', dy=14)
