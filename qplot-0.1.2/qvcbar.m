function qvcbar(x0, y0, y1, w)
% QVCBAR - Add a vertical color bar to a figure
%   QVCBAR(x0, y0, y1) adds a vertical color bar to the figure between
%   (X0, Y0) and (X0, Y1), expressed in data coordinates.
%   If Y1>Y0, the color bar runs up, else down.
%   QVCBAR(..., w) specifies the width of the color bar in points (default:
%   5 points). If W is positive, the bar extends to the right of X0,
%   otherwise to the left.
%   This only works after a preceding QIMSC and uses the lookup table (QLUT)
%   used by that QIMSC.
%   QVCBAR uses QAXSHIFT to create distance between X0 and the color bar.
%   Positive QAXSHIFT creates space, negative creates overlap.
%   QVCBAR without arguments creates a color bar to the right of the QIMSC.


idx = qp_idx;
global qp_data;
lut = qlut;
C = size(lut,1);

if ~isfield(qp_data.info(idx), 'clim') ...
      || ~isfield(qp_data.info(idx), 'imrect')
  error('qvcbar needs a preceding qimsc');
end

if nargin==0
  xywh = qp_data.info(idx).imrect;
  x0 = xywh(1) + xywh(3);
  y0 = xywh(2);
  y1 = xywh(2) + xywh(4);
  w = 5;
  fprintf(1, 'qvcbar(%g, %g, %g, %g);\n', x0, y0, y1, w);
elseif nargin<4
  w = 5;
end

dx = qaxshift;
if w<0
  dx = -dx; + w;
end

isup = y1>y0;

if isup
  xywh_d = [x0 y0 0 y1-y0];
else
  xywh_d = [x0 y1 0 y0-y1];
end

xywh_p = [dx 0 w 0];

if isup
  lut = flipud(lut);
end


qgimage(xywh_d, xywh_p, reshape(lut,[C 1 3]));

idx = qp_idx;
global qp_data
qp_data.info(idx).cbar.xywh_d = xywh_d;
qp_data.info(idx).cbar.xywh_p = xywh_p;
qp_data.info(idx).cbar.orient = 'y';
qp_data.info(idx).cbar.rev = ~isup;
qp_data.info(idx).cbar.clim = qp_data.info(idx).clim;
end

