function tx = sensibleticks(xxx, cnt, inc)
% SENSIBLETICKS - Coordinates of sensible ticks
%    tx = SENSIBLETICKS(xxx) returns approx. 5 ticks that span the range of  
%    the data XXX.
%    tx = SENSIBLETICKS(xx, cnt) overrides the number of approx. ticks.
%    tx = SENSIBLETICKS(..., 1) makes the ticks extend past the data. (The
%    default is for the ticks to not go beyond the data limits.)

if nargin<2
  cnt = 5;
end
if nargin<3
  if cnt==1
    inc=1;
    cnt=5;
  else
    inc=0;
  end
end

x0 = min(xxx);
x1 = max(xxx);
rng = x1 - x0;

tx=[];
scl=1;
while length(tx)<cnt
  dx = sensiblestep(rng/scl);
  if inc
    x0a = floor(x0/dx)*dx;
  else
    x0a = ceil(x0/dx)*dx;
  end
  if inc
    x1a = ceil(x1/dx)*dx;
  else
    x1a = floor(x1/dx)*dx;
  end
  tx = [x0a:dx:x1a];
  scl=scl*1.5;
end

