function qarrow(l, w, dl, dimple, dw)
% QARROW - Draw an arrowhead
%   QARROW draws an arrow head pointing to the current anchor set by QAT.
%   QARROW(l, w) specifies length and (full) width of the arrow head
%   These are specified in points, and default to L=8, W=5.
%   QARROW(l, w, dl) specifies that the arrow is to be displaced from the
%   anchor by a distance DL along the arrow's axis.
%   QARROW(l, w, dl, dimple) specifies that the back of the arrow head is
%   indented by DIMPLE points.
%   QARROW(l, w, dl, dimple, dw) specifies that the arrow is to be displaced
%   from the anchor by DW points in the orthogonal direction of the arrow's
%   axis.

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

if nargin<1 || isempty(l)
  l = 8;
end
if nargin<2 || isempty(w)
  w = 0.6 * l;
end
if nargin<3 || isempty(dl)
  dl = 0;
end
if nargin<4 || isempty(dimple)
  dimple = 0;
end
if nargin<5 || isempty(dw)
  dw = 0;
end

qarea([0 -l dimple-l -l]-dl, [0 w 0 -w]/2+dw);
