function u = qunix(cmd)
[u,s] = unix(cmd);
if nargout<1
  if u
    fprintf(1, '%s\n', s);
    fprintf(1, '=> %i\n', u);
  end
  clear u
end
