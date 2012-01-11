function qmark(xx, yy)
% QMARK - Draw on the current graph with the current marker
%   QMARK(xx, yy) draws marks at the given location in data space. See also
%   QMARKER.
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

fprintf(fd, 'mark *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);

