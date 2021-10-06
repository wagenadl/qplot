function qarea(xx, yy)
% QAREA - Draw a polygon in paper space
%    QAREA(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
%    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
%    The polygon is filled with the current brush.
%    XX and YY are given in postscript points. See also QPATCH and QGAREA.

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

qp_plot(xx, yy, 'area');
