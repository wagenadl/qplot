function pt = qaxshift(pt)
% QAXSHIFT - Specifies shift of drawn axis for QXAXIS and QYAXIS
%    QAXSHIFT(len) specifies shift (in points) for QXAXIS and
%    QYAXIS. Positive means down or left, negative means up or right.
%    pt = QAXSHIFT returns current setting.

idx = qp_idx;
global qp_data;

if nargin==0
  
  pt = qp_data.info(idx).axshift;

else
  
  if ischar(pt)
    pt = str2double(pt);
  end
  
  if ~isnscalar(pt) || ~isreal(pt) || isnan(pt) || isinf(pt)
    error('axshift must be a real scalar');
  end
  
  qp_data.info(idx).axshift = pt;
  
  clear pt

end