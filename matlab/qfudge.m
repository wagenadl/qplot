function qfudge(varargin)
% QFUDGE - Add margin to QPLOT panel
%    QFUDGE adds 1 point of margin to the current QPLOT panel.
%    QFUDGE(margin) adds the given margin (in points).
%    QFUDGE(margin, ratio) forces a given aspect ratio on the data units.

fd = qp_fd(1);

if nargin>2
  error('Usage: qfudge [margin] [ratio]');
end

str = 'fudge';
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

