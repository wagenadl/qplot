function qylim(varargin)
% QYLIM - Set y-axis limits
%   QYLIM(y0, y1) sets y-axis limits in the current panel.

fd = qp_fd(1);

if nargin<2 || nargin>2
  error('Usage: qylim x0 x1');
end

str = 'ylim';
for k=1:nargin
  a = varargin{k};
  if ischar(a) && ~isnan(str2double(a))
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) && isreal(a)
    str = sprintf('%s %g', str, a);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);
qp_flush(fd);

