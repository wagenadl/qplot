function runmeg(ifn)
[dir,fn,ext] = fileparts(ifn);
fn = fn(1:end-3);

ifn = [fn '_eg.m'];

if strcmp(fn, 'qclose') || strcmp(fn, 'qselect') || strcmp(fn, 'qfigure')
  system(sprintf('touch %s.png', fn));
  system(sprintf('touch %s.pdf', fn));
  return
end

[s,o] = system(sprintf('grep shrink %s', ifn));
fprintf(1, 'Eval %s_eg\n', fn)
eval([fn '_eg'], ...
     'printf("Error: %s\n", lasterr()); exit(1);');
fprintf(1, 'Back\n');
if s
  qshrink(2);
end

qselect([ fn '.qpt' ]);
qsave([ fn '.pdf' ]);
qsave([ fn '.png' ], 100);  
qclose([ fn '.qpt' ]);

