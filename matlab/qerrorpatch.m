function qerrorpatch(xx, yy, dy, dir)
% QERRORPATCH - Draw error patch
%    QERRORPATCH(xx, yy, dy) plots an error patch at (XX,YY+-DY).
%    Normally, XX, YY, and DY have the same shape. However, it is permissible
%    for DY to be shaped Nx2, in which case lower and upper error bounds
%    are different.
%    QERRORPATCH(..., 'up') only plots upward; QERRORPATCH(..., 'down') only 
%    plots downward.

if nargin<4
  dir = 'both';
end

xx = xx(:);
yy = yy(:);
N = length(xx);
if prod(size(dy))==2*N
  dy_dn = -dy(:,1);
  dy_up = dy(:,2);
else
  dy_up = dy(:);
  dy_dn = -dy(:);
end

switch dir
  case 'up'
    dy_dn = 0;
  case 'down'
    dy_up = 0;
end

qpatch([xx; flipud(xx)], [yy+dy_dn; flipud(yy+dy_up)]);
