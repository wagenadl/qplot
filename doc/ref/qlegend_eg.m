qfigure('qlegend', 3, 3);

qlegopt('x', 2*pi, 'y', 1, 'dx', 10);

xx=[0:.1:2*pi];

qpen b
qplot(xx, cos(xx));

qlegend('Cosine');

qpen r
qplot(xx, sin(xx));

qlegend('Sine');

qshrink
