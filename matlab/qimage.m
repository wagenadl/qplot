function qimage(varargin)
% QIMAGE - Plot an image
%    QIMAGE(xywh, data) plots an image. XYWH specifies a rectangle in
%    data coordinates. The image data must be YxXx1 or YxXx3 and may
%    either be UINT8 or DOUBLE.
%    QIMAGE(data) plots the image at (0,0)+(XxY). Note that that differs
%    by 0.5 units from matlab conventions.
%    QIMAGE(xx, yy, data) specifies bin centers. (Only the first and last
%    elements of XX and YY actually matter).
%    It is permissable for W or H to be negative; in that case, the
%    image will be plotted upside down.

fd = qp_fd(1);

switch nargin
  case 1
    data = varargin{1};
    [Y X C] = size(data);
    xywh=[0 0 X Y];
  case 2
    xywh = varargin{1};
    data = varargin{2};
  case 3
    xx = varargin{1};
    yy = varargin{2};
    data = varargin{3};
    [Y X] = size(data);
    dx = (xx(end)-xx(1))/(X-1);
    dy = (yy(end)-yy(1))/(Y-1);
    xywh = [xx(1)-dx/2 yy(1)-dy/2 Y*dx Y*dy];
    data = flipud(data);
  otherwise
    error('qimage takes 1 to 3 arguments');
end

if ~isnvector(xywh) || ~isreal(xywh)
  error('xywh must be a real vector of length 4');
end
if ~isnumeric(data) || ~isreal(data)
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
  C=3;
elseif C~=3
  error('data must be YxXx1 or YxXx3');
end

data = permute(data,[3 2 1]);
fprintf(fd, 'image %g %g %g %g %i *uc%i\n', ...
    xywh(1), xywh(2), xywh(3), xywh(4), ...
    X, X*Y*C);
if ~isa(data, 'uint8')
  data = uint8(floor(255*data+.5));
end
fwrite(fd, data, 'uint8');

qp_flush(fd);

