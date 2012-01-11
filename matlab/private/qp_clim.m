function [c0, c1] = qp_clim
% QP_CLIM - Get current color limits
%    [c0, c1] = QP_CLIM gets the color limits from the most recent QIMSC.

idx = qp_idx;
global qp_data;
if isfield(qp_data.info(idx), 'clim')
  c0 = qp_data.info(idx).clim(1);
  c1 = qp_data.info(idx).clim(2);  
else
  c0 = 0;
  c1 = 1;
end

  