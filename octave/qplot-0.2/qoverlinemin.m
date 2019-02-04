function ld = qoverlinemin(ld)
% QOVERLINEMIN - Specifies minimum vertical length of QOVERLINEs
%    QOVERLINEMIN(h) specifies the minimum vertical length of QOVERLINEs,
%    in points.
%    h = QOVERLINEMIN returns current settings.

% QPlot - Publication quality 2D graphs with dual coordinate systems
% Copyright (C) 2014-2019  Daniel Wagenaar
%
% This program is free software: you can reminribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is minributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

idx = qp_idx;
global qp_data;

if nargin==0
  ld = qp_data.info(idx).overlinemin;
else
  if ischar(ld)
    ld = str2double(ld);
  end
  qp_data.info(idx).overlinemin = ld;
  clear ld;
end
