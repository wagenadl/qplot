function alleg
% Run all examples and save output

dir0=pwd;
cd 'html/ref'

ff = glob('*_eg.m');
F = length(ff);

for f=1:F
  fn = ff{f};
  if length(fn)>5 && strcmp(fn(end-4:end), 'eg_.m')==0
    fn = fn(1:end-5);
  end
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
  qsave([ fn '.png' ], 100);  
  qclose([ fn '.qpt' ]);
end

cd(dir0);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function runone(fn)
[s,o] = system(sprintf('grep shrink %s_eg.m', fn));
eval([fn '_eg']);
if s
  qshrink(2);
end

