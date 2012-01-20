function qp_plot(xx, yy, cmd)
% QPLOT - Draw a line series in data space
%    QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
%    coordinates. See also QLINE and QGLINE.

if nargin<3
  cmd = 'plot';
end

fd = qp_fd(1);

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
end
if ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
end
if length(xx) ~= length(yy)
  error('xx and yy must be equally long');
end

[iup, idn] = qp_schmitt(~isnan(xx+yy),.7,.3,2);

for k=1:length(iup)
  N = idn(k) - iup(k);
  fprintf(fd, '%s *%i *%i\n', cmd, N, N);
  fwrite(fd, xx(iup(k):idn(k)-1), 'double');
  fwrite(fd, yy(iup(k):idn(k)-1), 'double');
end

qp_flush(fd);
