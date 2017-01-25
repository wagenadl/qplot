qfigure('eg_circ', 2.3, 2.);
xy =   [
  0.72584  -0.559
  0.11131  -.38611
  -.27279  .31731
  -0.36819  -0.36485
  .53813   0.46068
];

phi=[0:.01:2*pi];
qpen 777 0 dash
qplot(.5*cos(phi), .5*sin(phi));
qpen solid 
qplot(cos(phi), sin(phi));
qplot(1.05*[-1 1], [0 0]);
qplot([0, 0], 1.05*[-1 1]);

qpen k


qmarker o solid 4
qmark(xy(:,1), xy(:,2));

for k=1:length(xy)
  qat(xy(k,1), xy(k,2));
  qalign top left
  qtext(5,5, sprintf('%c', 'a'+k-1));
end


qat 1 0
qalign left middle
qtext 10 0 '0°'

qat -1 0
qalign right middle
qtext -10 0 '180°'

qat 0 1
qalign center bottom
qtext 0 -10 '90°'

qat 0 -1
qalign center top
qtext 0 10 '270°'

qshrink 1 1

qsave('pdf');
qsave png 120