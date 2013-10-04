function qsharelim(varargin)
% QSHARELIM - Share axis limits between QPlot panels
%    QSHARELIM [x|y] ID ... shares x and/or y-axis limits with the other named
%    panels.

fd = qp_fd(1);

if nargin<1
  error('Usage: qsharelim [x|y] ID ...');
end

str = 'sharelim';
for k=1:nargin
  a = varargin{k};
  if ischar(a) 
    if k==1 && (strcmp(a, 'x') || strcmp(a, 'y'))
      str = sprintf('%s %s', str, a);
    elseif a(1)>='A' && a(1)<='Z'
      str = sprintf('%s %s', str, a);
    else
      error('Cannot interpret arguments');
    end
  else
    error('Cannot interpret arguments');  
  end
end

fprintf(fd, '%s\n', str);
qp_flush(fd);

