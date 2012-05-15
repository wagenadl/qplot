function qmark(xx, yy)
% QMARK - Draw on the current graph with the current marker
%   QMARK(xx, yy) draws marks at the given location in data space. See also
%   QMARKER and QPMARK.
fd = qp_fd(1);

if isempty(xx)
  return
end

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
end
if ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
end
if length(xx) ~= length(yy)
  error('xx and yy must be equally long');
end

ok = ~isnan(xx(:)+yy(:));
xx=xx(ok);
yy=yy(ok);

fprintf(fd, 'mark *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);

