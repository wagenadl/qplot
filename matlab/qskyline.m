function qskyline(xx, yy)
% QSKYLINE - Skyline plot (bar plot)
%    QSKYLINE(xx, yy) draws a bar plot of yy vs xx with bars touching.

xx=xx(:)';
yy=yy(:)';

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
qpatch([xxx(1); xxx; xxx(end)],[0; yyy; 0]);