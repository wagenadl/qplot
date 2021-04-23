function ld = qoverlinedist(ld)
% QOVERLINEDIST - Specifies distance between QOVERLINEs and data
%    QOVERLINEDIST(dist) specifies the distance between QOVERLINEs and 
%    the data, in points.
%    dist = QOVERLINEDIST returns current settings.
%
%    NOTE: Positive numbers are up, negative are down, unlike for most
%          displacements in QPlot.

% QPlot - Publication quality 2D graphs with dual coordinate systems
% Copyright (C) 2014-2019  Daniel Wagenaar
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

idx = qp_idx;
global qp_data;

if nargin==0
  ld = qp_data.info(idx).overlinedist;
else
  if ischar(ld)
    ld = str2double(ld);
  end
  qp_data.info(idx).overlinedist = ld;
  clear ld;
end
