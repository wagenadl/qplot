function qline(xx, yy)
% QLINE - Draw a line series in paper space
%    QLINE(xx, yy) draws a line series between the points (XX,YY).
%    XX and YY are given in postscript points. See also QPLOT.

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

fprintf(fd, 'line *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');
