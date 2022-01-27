import qplot as qp
import numpy as np
qp.figure('c:/users/wagenaar/desktop/test.qpt')
qp.plot([0,1,2], [1,2,0])
x = np.arange(0,10,.001)
y = np.cos(x)
qp.plot(x,y)
qp.save("test.pdf")