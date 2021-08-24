function qshiftedline(xx, yy, dx, dy)
% QSHIFTEDLINE - Renders a line displaced from data points
%   QSHIFTEDLINE(xx, yy, dx, dy) is like QPLOT(xx, yy) except that the 
%   plot is displaced by (dx, dy) points on the graph.
%   XX, YY, DX, DY may be vectors or scalars. Any scalars are automatically
%   converted to vectors of the appropriate length. All vectors must be
%   the same length.
%   See also QGLINE.

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

N = max([length(xx), length(yy), length(dx), length(dy)]);

if length(xx)==1
  xx = repmat(xx, N, 1);
end
if length(yy)==1
  yy = repmat(yy, N, 1);
end
if length(dx)==1
  dx = repmat(dx, N, 1);
end
if length(dy)==1
  dy = repmat(dy, N, 1);
end

ar = cell(N, 1);

for n=1:N
  ar{n} = { 'absdata', xx(n), yy(n), 'relpaper', dx(n), dy(n) };
end

qgline(ar{:});


