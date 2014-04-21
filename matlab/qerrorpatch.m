function qerrorpatch(xx, yy, dy, dir)
% QERRORPATCH - Draw error patch
%    QERRORPATCH(xx, yy, dy) plots an error patch at (XX,YY+-DY).
%    Normally, XX, YY, and DY have the same shape. However, it is permissible
%    for DY to be shaped Nx2, in which case lower and upper error bounds
%    are different.
%    QERRORPATCH(..., 'up') only plots upward; QERRORPATCH(..., 'down') only 
%    plots downward.

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
  dy_dn = -dy(:);
  dy_up = dy(:);
end

switch dir
  case 'up'
    dy_dn = 0;
  case 'down'
    dy_up = 0;
end

qpatch([xx; flipud(xx)], [yy+dy_dn; flipud(yy+dy_up)]);
