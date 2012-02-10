function alleg
% Run all examples and save output

cd html

ff = glob('*_eg.m');
F = length(ff);

for f=1:F
  fn = basename(ff{f}, '_eg.m');
  if exist([fn '.png'])
    continue;
  end
  if strcmp(fn, 'qclose')
    continue;
  end
  if strcmp(fn, 'qselect')
    continue;
  end
  if strcmp(fn, 'qfigure')
    continue;
  end
  
  fprintf(1, ': %s\n',fn);
  fflush(1);
  runone(fn);
  qselect([ fn '.qpt' ]);
  qsave([ fn '.pdf' ]);
  qsave([ fn '.png' ], 72);  
  qclose([ fn '.qpt' ]);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function runone(fn)
eval([fn '_eg'])
