function qcbard(xywh, vh)
% QCBARD - Adds a colorbar to the figure
%    QCBARD(xywh) represents the current LUT at location XYWH, specified
%    in data coordinates.
%    QCBARD(xywh, vh) draws a colorbar in a nonstandard direction:
%      VH = 'h' or 'r' draws a left-to-right colorbar,
%      VH = 'l' draws a right-to-left colorbar,
%      VH = 'd' draws a top-to-bottom colorbar,
%      VH = 'v' or 'u' draws a bottom-to-top colorbar (default).

if nargin<2 || isempty(vh)
  vh = 'v';
end

if strcmp(vh, 'v') || strcmp(vh, 'u')
  hori = 0;
  flip = 0;
elseif strcmp(vh, 'd')
  hori = 0;
  flip = 1;
elseif strcmp(vh, 'h') || strcmp(vh, 'r')
  hori = 1;
  flip = 0;
elseif strcmp(vh,'l')
  hori = 1;
  flip = 1;
else
  error('Usage: qcbar XYWH [v|h|l|d]');
end
 
lut = qlut;
if flip 
  lut = flipud(lut);
end

C = size(lut,1);
if hori
  qimage(xywh, reshape(lut, [1 C 3]));
else
  qimage(xywh, reshape(flipud(lut), [C 1 3]));
end

idx = qp_idx;
global qp_data;
qp_data.info(idx).cbar.rev = flip;
if hori
  qp_data.info(idx).cbar.orient = 'x';
else
  qp_data.info(idx).cbar.orient = 'y';
end
qp_data.info(idx).cbar.xywh_d = xywh;
qp_data.info(idx).cbar.xywh_p = [0 0 0 0];
qp_data.info(idx).cbar.clim = qp_data.info(idx).clim;
