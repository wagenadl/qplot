function qtextoncurve(xx, yy, dy, txt)
if nargin==3
  txt = dy;
  dy = 0;
elseif nargin~=4
  error('Usage: qtextoncurve xx yy [dy] text');
end

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
elseif ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
elseif length(xx) ~= length(yy)
  error('xx and yy must be equally long');
elseif ~isscalar(dy) || ~isreal(dy)
  error('dy must be a real scalar')
end

idx = find(~isnan(xx+yy));
xx = xx(idx);
yy = yy(idx);
N = length(xx);

fd = qp_fd(1);

fprintf(fd, 'textoncurve *%i *%i %g "%s"\n', N, N, dy, txt);
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);
