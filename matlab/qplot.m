function qplot(xx, yy)
global qp_data
fd = qp_ensure(1);

if ~isnvector(xx) | ~isreal(xx)
  error('xx must be a real vector')
end
if ~isnvector(yy) | ~isreal(yy)
  error('yy must be a real vector')
end
if length(xx) ~= length(yy)
  error('xx and yy must be equally long');
end

fprintf(fd, 'plot *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');
