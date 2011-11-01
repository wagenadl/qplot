function qpatch(xx, yy)
% QPATCH - Draw a polygonal patch in data space
%    QPATCH(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
%    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
%    The polygon is filled with the current brush.
%    XX and YY are given in data coordinates. See also QAREA and QGAREA.

fd = qp_fd(1);

if ~isnvector(xx) | ~isreal(xx)
  error('xx must be a real vector')
end
if ~isnvector(yy) | ~isreal(yy)
  error('yy must be a real vector')
end
if length(xx) ~= length(yy)
  error('xx and yy must be equally long');
end

fprintf(fd, 'patch *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');
