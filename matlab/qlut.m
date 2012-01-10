function [lut, nanc] = qlut(lut, nanc) 
% QLUT - Set lookup table for future QIMSC.
%    QLUT(lut) where LUT is Nx3 sets a new lookup table for QIMSC.
%    QLUT(lut, nanc) where NANC is 1x3 (or 3x1) sets a special color to use
%    for NaN values. (The default is white.)
%    [lut, nanc] = QLUT returns current values.

if nargin<2
  nanc=[1 1 1];
end

idx = qp_idx;
global qp_data;

if nargin>=1
  qp_data.info(idx).lut = lut;
  qp_data.info(idx).lut_nan = nanc;
end

clear nanc lut

if nargout>=1
  lut = qp_data.info(idx).lut;
end
if nargout>=2
  nanc = qp_data.info(idx).nanc;
end


