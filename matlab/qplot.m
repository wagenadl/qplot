function qplot(xx, yy)
% QPLOT - Draw a line series in data space
%    QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
%    coordinates. See also QLINE and QGLINE.

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

fprintf(fd, 'plot *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);
