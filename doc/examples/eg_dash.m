qfigure('eg_dash.qpt', 4, 4);
qplot([-2 2],[-2 2]);
qxaxis(0,[-2:2]);
qyaxis(0,[-2:2]);


qpen 1 dash 18
qplot([-2 2],[0 0]-1.5);

qpen 2 dash 18
qplot([-2 2],[0 0] -1.4);

qpen 0.5 dash 18
qplot([-2 2],[0 0] -1.3);

qpen 0 dash 18
qplot([-2 2],[0 0] -1.2);
qpen 0 solid
qplot([-2 2],[0 0] -1.1);

qpen 1 dash 18
qplot([-2 2],[0 0] -1);
qpen 2
qplot([-2 2],[0 0] -.9);
qpen .5
qplot([-2 2],[0 0] -.8);

qpen 1 dash 9
qplot([-2 2],[0 0]+1.5);

qpen 2 dash 9
qplot([-2 2],[0 0] +1.4);
qpen 0.5 dash 9
qplot([-2 2],[0 0] +1.3);

qpen 0 dash 9
qplot([-2 2],[0 0] +1.2);
qpen 0 solid
qplot([-2 2],[0 0] +1.1);
qpen 1 dash 9
qplot([-2 2],[0 0] +1);
qpen 2
qplot([-2 2],[0 0] +.9);
qpen .5
qplot([-2 2],[0 0] +.8);


qpen 0 dot 9
qplot([-2 2],[0 0] + .1);
qpen .5 dot 9
qplot([-2 2],[0 0] + .2);
qpen 1 dot 9
qplot([-2 2],[0 0] + .3);
qpen 2 dot 9
qplot([-2 2],[0 0] + .4);
qpen 4 dot 9
qplot([-2 2],[0 0] + .5);

qpen roundcap
qpen 0 dot 9
qplot([-2 2],[0 0] - .1);
qpen .5 dot 9
qplot([-2 2],[0 0] - .2);
qpen 1 dot 9
qplot([-2 2],[0 0] - .3);
qpen 2 dot 9
qplot([-2 2],[0 0] - .4);
qpen 4 dot 9
qplot([-2 2],[0 0] - .5);



qsave('/tmp/eg_dash.pdf');
qsave('/tmp/eg_dash.png');
qsave('/tmp/eg_dash.svg');
