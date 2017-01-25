qfigure('qlegopt', 3, 3);

qlegopt('x', 2*pi, 'y', 1, 'dx', 10, 'height', 16, 'skip', 20, 'drop', 5);
qfont Helvetica 16

xx=[0:.1:2*pi];

qpen none
qbrush b .5
qbars(xx, cos(xx), .1);

qlegopt('color', 'b');

qplegend('Cosine');

qbrush r .5
qbars(xx, sin(xx), .1);

qlegopt('color', 'r');

qplegend('Sine');

qshrink
