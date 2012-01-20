qfigure('eg_ticklen.qpt', 5, 3.5);

qticklen 3
qtextdist 3 3
qxaxis(1,[0.5 5.5],[1:5],'Axis A');

qticklen -5
qtextdist 3 3
qxaxis(2,[0.5 5.5],[1:5],'Axis B');

qticklen 3
qtextdist -5 3
qxaxis(3,[0.5 5.5],[1:5],'Axis C');

qticklen -3
qtextdist -3 -8
qxaxis(4,[0.5 5.5],[1:5],'Axis D');

qticklen 3
qtextdist 3 -3
qxaxis(5,[0.5 5.5],[1:5],'Axis E');
qticklen 1
qmticks([.5:.1:5.5]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

qticklen 3
qtextdist 3 3
qyaxis(7,[0.5 3.5],[1:3],'Axis F');

qticklen -3
qtextdist 3 3
qyaxis(9,[0.5 3.5],[1:3],'Axis G');

qticklen 3
qtextdist -3 3
qyaxis(11,[],[1:3],'Axis H');

qticklen -3
qtextdist -3 -3
qyaxis(13,[0.5 3.5],[1:3],'Axis I');

qticklen 3
qtextdist 3 -3
qyaxis(15,[0.5 3.5],[1:3],'Axis J');
qticklen 1
qmticks([.5:.1:3.5]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

qticklen 3
qtextdist 3 3

qylabelrot 0
qyaxis(8,[4:.5:5],[1 2 3],'Axis K');

qylabelrot -1
qyaxis(10,[4:.5:5],[1 2 3],'Axis L');

qtextdist 3 -3
qylabelrot -1
qyaxis(12,[4:.5:5],[1 2 3],'Axis M');

qtextdist -3 -3
qylabelrot -1
qyaxis(14,[4:.5:5],[1 2 3],'Axis N');

qfudge
