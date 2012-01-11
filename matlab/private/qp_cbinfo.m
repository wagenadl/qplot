function cb = qp_cbinfo
% QP_CBINFO - Extract information about colorbar
%    cb = QP_CBINFO extracts information about the most recent QCOLORBAR.
%    CB will be a struct with fields:
%      hori: 1/0 if the colorbar is horizontal/vertical
%      flip: 1/0 if the orientation is flipped
%      c0: lower limit of data range represented
%      c1: upper limit of data range represented
%      xywh: rectangle of the colorbar in data space

idx = qp_idx;
global qp_data;

if ~isfield(qp_data.info(idx), 'cbar')
  error('QP_CBINFO cannot function without a colorbar');
end

cb = qp_data.info(idx).cbar;
[cb.c0, cb.c1] = qp_clim;

