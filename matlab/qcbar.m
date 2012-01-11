function qcbar(xywh, vh)
% QCBAR - Adds a colorbar to the figure
%    QCBAR(xywh) represents the current LUT at location XYWH, specified
%    in data coordinates.
%    QCBAR(xywh, vh) draws a colorbar in a nonstandard direction:
%      VH = 'h' or 'r' draws a left-to-right colorbar,
%      VH = 'l' draws a right-to-left colorbar,
%      VH = 'd' draws a top-to-bottom colorbar,
%      VH = 'v' or 'u' draws a bottom-to-top colorbar (default).
%
%    In the future, QCBAR(xywh, hv, wid) will override the width of the 
%    bar with a specification in points, but the current "image" command
%    cannot yet handle that.

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
qp_data.info(idx).cbar.flip = flip;
qp_data.info(idx).cbar.hori = hori;
qp_data.info(idx).cbar.xywh = xywh;
