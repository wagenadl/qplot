function qsharelim(varargin)
% QSHARELIM - Add margin to QPLOT panel
%    QSHARELIM adds 1 point of margin to the current QPLOT panel.
%    QSHARELIM(margin) adds the given margin (in points).
%    QSHARELIM(margin, ratio) forces a given aspect ratio on the data units.

fd = qp_fd(1);

if nargin>2
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

