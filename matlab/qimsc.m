function qimsc(varargin)
% QIMSC - Plot 2D data as an image using lookup table
%    QIMSC(xywh, data) plots the DATA as an image using a lookup previously
%    set by QLUT. The color axis limits default to the min and max of the data.
%    QIMSC(xywh, data, c0, c1) overrides those limits.
%    QIMSC(xx, yy, data) or QIMSC(xx, yy, data, c0, c1) specifies bin centers.
%    QIMSC(data) or QIMSC(data, c0, c1) sets XYWH to (0,0)+(X,Y) as in QIMAGE.

switch nargin
  case 1
    data = varargin{1};
    c0 = min(data(:));
    c1 = max(data(:));
    [Y X] = size(data);
    xywh = [0 0 X Y];
  case 2
    xywh = varargin{1};
    data = varargin{2};
    c0 = min(data(:));
    c1 = max(data(:));
  case 3    
    if isnscalar(varargin{3})
      % So we have QIMSC(data, c0, c1)
      data = varargin{1};
      c0 = varargin{2};
      c1 = varargin{3};
      [Y X] = size(data);
      xywh = [0 0 X Y];
    else
      % So we have QIMSC(xx, yy, data)
      xx = varargin{1};
      yy = varargin{2};
      data = varargin{3};
      [Y X] = size(data);
      dx = (xx(end)-xx(1))/(X-1);
      dy = (yy(end)-yy(1))/(Y-1);
      xywh = [xx(1)-dx/2 yy(1)-dy/2 X*dx Y*dy];
      c0 = min(data(:));
      c1 = max(data(:));
    end
  case 4
    xywh = varargin{1};
    data = varargin{2};
    c0 = varargin{3};
    c1 = varargin{4};
  case 5
    xx = varargin{1};
    yy = varargin{2};
    data = varargin{3};
    c0 = varargin{4};
    c1 = varargin{5};
    [Y X] = size(data);
    dx = (xx(end)-xx(1))/(X-1);
    dy = (yy(end)-yy(1))/(Y-1);
    xywh = [xx(1)-dx/2 yy(1)-dy/2 X*dx Y*dy];
  otherwise
    error('qimsc takes 1 to 5 arguments');
end

idx = qp_idx(1);
global qp_data;
lut = qp_data.info(idx).lut;
[N C] = size(lut);
data = floor(1+(N-.0001)*(data-c0)/(c1-c0)); % normalize to color range
data(data<1)=1;
data(data>N)=N;

qimage(xywh, reshape(lut(reshape(data,[Y*X 1]),:), [Y X C]));
