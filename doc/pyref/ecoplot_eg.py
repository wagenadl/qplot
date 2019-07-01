import pyqplot.all as qp

qp.figure('ecoplot', 3, 3)

N=1e6
tt=[1:N]
yy=(mod(tt,100000)==30000)-(mod(tt,130000)==45000)+randn(1,N)/15

qp.pen k 0
qp.brush k

# Plot at 300 dpi but don't lose any spikes

qp.ecoplot(tt, yy, 3*300)
