function qimsc(xywh, data, c0, c1)
% QIMSC - Plot 2D data as an image using lookup table
%    QIMSC(xywh, data) plots the DATA as an image using a lookup previously
%    set by QLUT. The color axis limits default to the min and max of the data.
%    QIMSC(xywh, data, c0, c1) overrides those limits.
%    QIMSC(data) or QIMSC(data, c0, c1) sets XYWH to (0,0)+(X,Y) as in QIMAGE.

if nargin==3
  c1 = c0;
  c0 = data;
  data = xywh;
  [Y X] = size(data);
  xywh = [0 0 X Y];
elseif nargin==1
  data = xywh;
  [Y X] = size(data);
  xywh = [0 0 X Y];
end  

if nargin<3
  c0 = min(data(:));
  c1 = max(data(:));
end

idx = qp_idx(1);
[N C] = size(qp_data.lut{idx});
data = floor(1+(N-.0001)*(data-c0)/(c1-c0)); % normalize to color range

qimage(xywh, reshape(qp_data.lut(reshape(data,[Y*X 1]),:), [Y X C]));
