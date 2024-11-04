qfigure('qplegend', 3, 3);

qlegopt('x', 2*pi, 'y', 1, 'dx', 10)

xx=[0:.1:2*pi];

qpen none
qbrush b .5
qbars(xx, cos(xx), .1);

qplegend('Cosine');

qbrush r .5
qbars(xx, sin(xx), .1);

qplegend('Sine');

qshrink
