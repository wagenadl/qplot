qfigure('qpen.qpt', 3, 3);

qpen r 2
qplot([0 1],[0 0]);

qpen('b', 'dash', [ 10 6 1 6]);
qplot([0 1],[1 1]);

qpen 930 dot 6
qplot([0 1], [2 2]);

qpen([1 0 1], 'solid');
qplot([0 1], [3 3]);

qpen k miterjoin roundcap 10
qplot([.3 .5 .7],[.2 .8 .2]);

qpen k roundjoin squarecap 10
qplot([.3 .5 .7],[.2 .8 .2]+1);

qpen k beveljoin flatcap 10
qplot([.3 .5 .7],[.2 .8 .2]+2);

