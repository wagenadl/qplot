function qlut(lut) 
% QLUT - Set lookup table for future QIMSC.
idx = qp_idx;
global qp_data;
qp_data.info(idx).lut = lut;
