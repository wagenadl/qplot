function qplot(xx, yy)
% QPLOT - Draw a line series in data space
%    QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
%    coordinates. See also QLINE and QGLINE.

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

if nargin==1
  yy = xx;
  xx = [1:length(yy)];
end

qp_plot(xx, yy, 'plot');
