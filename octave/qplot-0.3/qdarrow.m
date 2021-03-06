function qdarrow(x, y, ang, l, w, dist, dimple)
% QDARROW - Draw an arrowhead
%   QDARROW(x, y, ang) draws an arrow head pointing to (X,Y)
%   in the direction ANG. ANG may be given in radians in paper (0: pointing
%   right, pi/2: pointing down), or as a (DX,DY) pair of data coordinates.
%   QDARROW(x, y, ang, l, w) specifies length and (full) width of the arrow
%   head. These are specified in points, and default to L=8, W=5.
%   QDARROW(x, y, ang, l, w, dist) specifies that the arrow is to be retracted
%   a given distance from the point (X, Y).
%   QDARROW(x, y, ang, l, w, dist, dimple) specifies that the back of the 
%   arrow head is indented by DIMPLE points.

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


if length(ang)==2
  qat(x, y, ang(1), ang(2));
else
  qat(x, y, ang);
end

if nargin<4 || isempty(l)
  l = 8;
end
if nargin<5 || isempty(w)
  w = .6*l;
end
if nargin<6 || isempty(dist)
  dist=0;
end
if nargin<7 || isempty(dimple)
  dimple=0;
end

qarea([0 -l dimple-l -l]-dist, [0 w 0 -w]/2);
