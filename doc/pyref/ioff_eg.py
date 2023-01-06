import qplot as qp
import numpy as np

qp.ioff()

qp.figure('ioff', 3, 3)

qp.at(0, 0)
qp.text("This figure will only be saved to a file")
qp.save("pdf")
