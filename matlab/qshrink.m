function qshrink(varargin)
% QSHRINK - Add margin to QPLOT panel
%    QSHRINK adds 1 point of margin to the current QPLOT panel.
%    QSHRINK(margin) adds the given margin (in points).
%    QSHRINK(margin, ratio) forces a given aspect ratio on the data units.

fd = qp_fd(1);

if nargin>2
  error('Usage: qshrink [margin] [ratio]');
end

str = 'shrink';
for k=1:nargin
  a = varargin{k};
  if strcmp(a, '-') && k<nargin
    str = sprintf('%s -', str);
  elseif ischar(a) && ~isnan(str2double(a))
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) && isreal(a)
    str = sprintf('%s %g', str, a);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);
qp_flush(fd);

