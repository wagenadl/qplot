function pt = qytitlerot(pt)
% QYTITLEROT - Specifies the rotation of y-axis titles.
%    QYTITLEROT(phi) specifies the rotation of y-axis titles, in degrees:
%    phi=0 means upright,
%    phi>0 means rotated 90 degrees to the left,
%    phi<0 means rotated 90 degrees to the right.

idx = qp_idx;
global qp_data;

if nargin==0
  pt = qp_data.info(idx).ytitlerot;
else
  if ischar(pt)
    pt = str2double(pt);
  end
  
  if ~isnscalar(pt) || ~isreal(pt) || isnan(pt) || isinf(pt)
    error('ytitlerot must be a real scalar');
  end
  
  qp_data.info(idx).ytitlerot = sign(pt)*pi/2;
  
  clear pt

end