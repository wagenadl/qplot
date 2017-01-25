qfigure('eg_bars', 3, 2.5);

yy = [
  1.3 1.5
  0.6 0.7
  1.25 1.4
  ];

qlegopt x0 3.6 y0 1.5 

qbrush 955
qpen none
qbars([1:3]-.2, yy(:,1), .3);
qplegend 'Trial A'

qbrush 559
qbars([1:3]+.2, yy(:,2), .3);
qplegend 'Trial B'

qpen k 0 solid
qxaxis(0, [.5 3.5], [1:3], {'Baseline', 'Expt.', 'Wash'});
qyaxis(.5, [0:.5:1.5], 'Activity');

ym = max(yy,[],2);
dy = [ nan 5 30];
txt = {'', '**', 'n.s.'};
for k=2:3
  qshiftedline(1+.35*[-1 1], ym(1), 0, -dy(k));
  qshiftedline(k+.35*[-1 1], ym(k), 0, -dy(k));
  qshiftedline([1 1 k k], [ym(1) ym(1) ym(1) ym(k)], 0, -dy(k) - [0 10 10 0]);
  qat(mean([1 k]), max(ym([1 k])));
  qalign bottom center
  qtext(0, -dy(k)-12, txt{k});
end

qshrink

qsave pdf
qsave png 120
