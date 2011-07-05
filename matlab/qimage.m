function qimage(xywh, data)
% QIMAGE - Plot an image
%    QIMAGE(xywh, data) plots an image. XYWH specifies a rectangle in
%    data coordinates. The image data must be YxXx1 or YxXx3 and may
%    either be UINT8 or DOUBLE.
%    QIMAGE(data) plots the image at (0,0)+(XxY). Note that that differs
%    by 0.5 units from matlab conventions.
%    It is permissable for W or H to be negative; in that case, the
%    image will be plotted upside down.

fd = qp_fd(1);

if nargin==1
  data = xywh;
  [Y X C] = size(data);
  xywh=[0 0 X Y];
end

if ~isnvector(xywh) | ~isreal(xywh)
  error('xywh must be a real vector of length 4');
end
if ~isnumeric(data) | ~isreal(data)
  error('data must be a real numeric array');
end 

if xywh(3)<0
  data = fliplr(data);
  xywh(3) = -xywh(3);
  xywh(1) = xywh(1) - xywh(3);
end
if xywh(4)<0
  data = flipud(data);
  xywh(4) = -xywh(4);
  xywh(2) = xywh(2) - xywh(4);
end
 
[Y X C] = size(data);
if C==1
  data = repmat(data,[1 1 3]);
elseif C~=3
  error('data must be YxXx1 or YxXx3');
end

fprintf(fd, 'image %g %g %g %g %i *uc%i\n', ...
    xywh(1), xywh(2), xywh(3), xywh(4), ...
    X, X*Y*C);
if isa(data, 'uint8')
  for y=1:Y
    for x=1:X
      fwrite(fd, data(y,x,:), 'uint8');
    end
  end
else
  for y=1:Y
    for x=1:X
      fwrite(fd, floor(255*data(y,x,:)+.5), 'uint8');
    end
  end
end
