function pt = qylabelrot(pt)
% QYLABELROT - Specifies the rotation of y-axis labels.
%    QYLABELROT(phi) specifies the rotation of y-axis labels, in degrees:
%    phi=0 means upright,
%    phi>0 means rotated 90 degrees to the left,
%    phi<0 means rotated 90 degrees to the right.

idx = qp_idx;
global qp_data;

if nargin==0
  pt = qp_data.info(idx).ylabelrot;
else
  if ischar(pt)
    pt = str2double(pt);
  end
  
  if ~isnscalar(pt) || ~isreal(pt) || isnan(pt) || isinf(pt)
    error('ylabelrot must be a real scalar');
  end
  
  qp_data.info(idx).ylabelrot = sign(pt)*pi/2;
  
  clear pt

end