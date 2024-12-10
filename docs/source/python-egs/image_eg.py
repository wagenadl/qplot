import qplot as qp
import numpy as np

qp.figure('image', 3, 3)

xx, yy = np.meshgrid(range(10), range(10))
img = np.stack((xx/10, yy/10, 0.5 + 0*xx), 2)

qp.image(img, [0, 0, 1, 1])

