function pt = qticklen(pt)
% QTICKLEN - Specifies length of ticks for QXAXIS and QYAXIS
%    QTICKLEN(len) specifies length of ticks (in points) for QXAXIS and
%    QYAXIS. Positive means down or left, negative means up or right.
%    pt = QTICKLEN returns current setting.

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

idx = qp_idx;
global qp_data;

if nargin==0
  
  pt = qp_data.info(idx).ticklen;

else
  
  if ischar(pt)
    pt = str2double(pt);
  end
  
  if ~isnscalar(pt) || ~isreal(pt) || isnan(pt) || isinf(pt)
    error('ticklen must be a real scalar');
  end
  
  qp_data.info(idx).ticklen = pt;
  
  clear pt

end