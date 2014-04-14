qfigure('tut-03');


x = -10:0.1:10; 
qpen r 2 solid
qplot(x, sin(x));
qpen b 2 dot
qplot(x, cos(x));

qshrink; qsave('tut-03-01.png', 96);


qfigure('tut-03');


x = -10:.5:10; 
qpen r 2 solid
qbrush 955
qskyline(x, sin(x));

qshrink; qsave('tut-03-02.png', 96);


qfigure('tut-03');


x = -10:.5:10; 
qpen none
qbrush 559
qbars(x, sin(x), 0.33);

qshrink; qsave('tut-03-03.png', 96);


