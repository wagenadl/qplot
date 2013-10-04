clq


x = -10:0.1:10; 
qplot(x, sin(x));


qxaxis(-1.1, [-10:5:10]); 
qxaxis(-1.4, [-10 10], [], 'Time');
qxaxis(-1.7, [-10 10], [-2*pi 0 2*pi], {'-2π', '0', '2π'}, 'Angle');


qfont Times bold 15
qaxshift 5
qticklen 10
qtextdist 5
qpen r 2
qyaxis(-10, [-1:1], 'Height');


qshrink
