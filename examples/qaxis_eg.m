qfigure('qaxis_eg.qpt', 5, 3.5);

xx = [-pi:.001:pi]*3;

qpen b 1
qplot(xx, cos(xx))
qpen r 1
qplot(xx, sin(xx))

qpen k 0
qxaxis(-1.1, pi*[-3:3], strtoks('-3π -2π -π 0 π 2π 3π'), 'Angle (rad)');
qyaxis(-3.1*pi, [-1:1], 'Cosine and sine');
qticklen 2.5
qmticks([-.5 .5])
qticklen 1.5
qmticks([-1:.1:1])

qfudge
