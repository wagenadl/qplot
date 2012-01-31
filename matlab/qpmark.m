function qpmark(xx, yy)
% QPMARK - Draw on the current graph with the current marker
%   QPMARK(xx, yy) draws marks at the given location in paper space. See also
%   QMARKER and QMARK.
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

fprintf(fd, 'pmark *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);

