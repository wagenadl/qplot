%%% Call this as a script, not as a function!

1; % So the next local fuction won't be treated as a function

fprintf(1, 'ALLEG\n')

function runone(fn)
[s,o] = system(sprintf('grep shrink %s_eg.m', fn));
eval([fn '_eg']);
if s
  qshrink(2);
end
endfunction

ff = glob('*_eg.m');
F = length(ff);

for f=1:F
  ifn = ff{f};
  fn = ifn;
  if length(fn)>5 && strcmp(fn(end-4:end), 'eg_.m')==0
    fn = fn(1:end-5);
  end
  ofn = [fn '.png'];
  fprintf(1, 'looking for %s -> %s\n', ifn, ofn) 
  if exist(ofn)
    ms = stat(ifn);
    ps = stat(ofn);
    fprintf(1, 'time: %g %g -> %g\n', ms.mtime, ps.mtime, ps.mtime - ms.mtime)
    if ps.mtime>ms.mtime
      continue;
    end
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
  
  fprintf(1, 'RUNNING : %s\n', fn);
  fflush(1);
  runone(fn);
  qselect([ fn '.qpt' ]);
  qsave([ fn '.pdf' ]);
  qsave([ fn '.png' ], 100);  
  qclose([ fn '.qpt' ]);
end
