function qcbarh(w, l, varargin)
% QCBAR - Add a horizontal color bar to a figure
%   QCBAR(w, h) adds a horizontal color bar of given width and height
%   (in points) at the position specified by QAT. W may be positive or 
%   negative. In either case, the color scale runs from left to right.
%   QCBAR(w, h, 'l') makes the color scale run right-to-left.
%   QCBAR(w, h, dx, dy) or QCBAR(w, h, dx, dy, 'l') shifts the bar by the 
%   given number of points to the right and down.
%   QCBAR(w, [], dw) or QCBAR(w,[], dx, dy, dw) specifies the width in data 
%   coordinates instead. In this case, the color scale runs l->r (r->l) if DW 
%   is positive (negative).
%   This command only works after a previous QIMSC.

[dw, dx, dy] = qp_cbargs('r', varargin{:});

idx = qp_idx;
global qp_data;
if ~isfield(qp_data.info(idx), 'atcoord')
  error('QCBAR needs a previous QAT');
end
xy = qp_data.info(idx).atcoord;

lut = qlut;
C = size(lut,1);

if isempty(w)
  w=0;
end
if l<0
  dy=dy+l;
  l=-l;
end
if w<0
  dx=dx+w;
  w=-w;
end

if ischar(dw)
  isright = strcmp(dw, 'r');
  xywh_d = [xy(1) xy(2) 0 0];
  xywh_p = [dx+w dy -w l];
else
  isright = dw>0;
  if dw<0
    xy(1) = xy(1)+dw;
    dw = -dw;
  end
  xywh_d = [xy(1) xy(2) dw 0];
  xywh_p = [dx+w dy -w l];
end
if ~isright
  lut = flipud(lut);
end
qgimage(xywh_d, xywh_p, reshape(lut,[1 C 3]));

idx = qp_idx;
global qp_data
qp_data.info(idx).cbar.xywh_d = xywh_d;
qp_data.info(idx).cbar.xywh_p = xywh_p;
qp_data.info(idx).cbar.orient = 'x';
qp_data.info(idx).cbar.rev = ~isright;
qp_data.info(idx).cbar.clim = qp_data.info(idx).clim;

