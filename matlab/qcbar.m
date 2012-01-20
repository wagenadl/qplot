function qcbar(w, l, varargin)
% QCBAR - Add a color bar to a figure
%   QCBAR(w, h) adds a vertical color bar of given width and height (in points)
%   at the position specified by QAT. H may be positive or negative. In either
%   case, the color scale runs from bottom to top.
%   QCBAR(w, h, 'd') makes the color scale run down.
%   QCBAR(w, h, dx, dy) or QCBAR(w, h, dx, dy, 'd') shifts the bar by the 
%   given number of points to the right and down.
%   QCBAR(w, [], dh) or QCBAR(w,[], dx, dy, dh) specifies the height in data 
%   coordinates instead. In this case, the color scale runs up (down) if DH 
%   is positive (negative).
%   This command only works after a previous QIMSC.

[dh, dx, dy] = qp_cbargs('u', varargin{:});

idx = qp_idx;
global qp_data;
if ~isfield(qp_data.info(idx), 'atcoord')
  error('QCBAR needs a previous QAT');
end
xy = qp_data.info(idx).atcoord;

lut = qlut;
C = size(lut,1);

if isempty(l)
  l=0;
end
if l<0
  dy=dy+l;
  l=-l;
end
if w<0
  dx=dx+w;
  w=-w;
end

if ischar(dh)
  isup = strcmp(dh, 'u');
  xywh_d = [xy(1) xy(2) 0 0];
  xywh_p = [dx dy w l];
else
  isup = dh>0;
  if dh<0
    xy(2) = xy(2)+dh;
    dh = -dh;
  end
  xywh_d = [xy(1) xy(2) 0 dh];
  xywh_p = [dx dy w l];
end
if isup
  lut = flipud(lut);
end
qgimage(xywh_d, xywh_p, reshape(lut,[C 1 3]));

idx = qp_idx;
global qp_data
qp_data(idx).info.cbar.xywh_d = xywh_d;
qp_data(idx).info.cbar.xywh_p = xywh_p;
qp_data(idx).info.cbar.orient = 'y';
qp_data(idx).info.cbar.rev = ~isup;
qp_data(idx).info.cbar.clim = qp_data(idx).info.clim;

