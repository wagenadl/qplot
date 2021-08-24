function qskyline(xx, yy, y0)
% QSKYLINE - Skyline plot (bar plot)
%    QSKYLINE(xx, yy) draws a bar plot of YY vs XX with bars touching.
%    QSKYLINE(xx, yy, y0) specifies the baseline of the plot; default is 0.

% QPlot - Publication quality 2D graphs with dual coordinate systems
% Copyright (C) 2014  Daniel Wagenaar
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

if isnan(y0)
  qplot([xxx(1); xxx; xxx(end)],[yyy(1); yyy; yyy(end)]);
else
  qpatch([xxx(1); xxx; xxx(end)],[y0; yyy; y0]);
end
