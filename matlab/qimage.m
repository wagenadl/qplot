function qimage(xywh, data)
fd = qp_ensure(1);

if ~isnvector(xywh) | ~isreal(xywh)
  error('xywh must be a real vector of length 4');
end
if ~isnumeric(data) | ~isreal(data)
  error('data must be a real numeric array');
end 
 
[Y X C] = size(data);
if C==1
  data = repmat(data,[1 1 3]);
elseif C~=3
  error('data must be YxXx1 or YxXx3');
end

fprintf(fd, 'image %g %g %g %g %i *%i\n', ...
    xywh(1), xywh(2), xywh(3), xywh(4), ...
    X, X*Y*C);
for y=1:Y
  for x=1:X
    fwrite(fd, data(y,x,:), 'double');
  end
end
