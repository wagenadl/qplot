function pt = qnumfmt(pt)
% QNUMFMT - Specifies the format of numbers as tick labels
%    QNUMFMT(fmt) specifies the format of numeric axis tick labels.
%    FMT may be anything that SPRINTF understands, for instance: "%.1f".
%    The default is "".

idx = qp_idx;
global qp_data;

if nargin==0
  
  pt = qp_data.info(idx).numfmt;

else
  
  qp_data.info(idx).numfmt = pt;
  clear pt

end