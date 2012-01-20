qfigure('eg_mark.qpt', 5, 3.5);

qpen k
qbrush r
qmarker 10

qmarker open o
qmark([1 1.1], [1 1])

qmarker solid o
qmark([1.5 1.6], [1 1])

qmarker brush o
qmark([2 2.1], [1 1])

mrks='+x-|osd<>^vph';
L = length(mrks);
for l=1:L
  qmarker(mrks(l));
  qmark(1+l/L, 2);
end

qpen k 4

qpen solid
qplot([1 1],[1.2 1.8]);

qpen dash
qplot([1 1]+.2,[1.2 1.8]);

qpen dot
qplot([1 1]+.4,[1.2 1.8]);

qpen dashdot
qplot([1 1]+.6,[1.2 1.8]);

qpen dashdotdot
qplot([1 1]+.8,[1.2 1.8]);

qpen solid 10
qpen miterjoin
qplot([1 1.1 1],[2.2 2.3 2.4]);

qpen beveljoin
qplot([1 1.1 1]+.15,[2.2 2.3 2.4]);

qpen roundjoin
qplot([1 1.1 1]+.3,[2.2 2.3 2.4]);

qpen flatcap
qplot([1  1]+.55,[2.2 2.4]);

qpen squarecap
qplot([1  1]+.7,[2.2 2.4]);

qpen roundcap
qplot([1  1]+.85,[2.2 2.4]);

qxlim(.8,2.2);
qylim(.8,2.2);

qfudge
