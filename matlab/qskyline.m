function qskyline(xx, yy, y0)
% QSKYLINE - Skyline plot (bar plot)
%    QSKYLINE(xx, yy) draws a bar plot of YY vs XX with bars touching.
%    QSKYLINE(xx, yy, y0) specifies the baseline of the plot; default is 0.

xx=xx(:)';
yy=yy(:)';
if nargin<3
  y0=0;
end

if length(xx)==1
  xxx = [-.5; .5] + xx;
  yyy = [yy; yy];
else
  dx = diff(xx);
  dx = [dx(1) dx dx(end)];
  xxx = [xx-dx(1:end-1)/2; xx+dx(2:end)/2];
  xxx = xxx(:);
  yyy = [yy; yy];
  yyy = yyy(:);
end

qpatch([xxx(1); xxx; xxx(end)],[y0; yyy; y0]);
