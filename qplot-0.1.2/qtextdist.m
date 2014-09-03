function [lbl, ttl] = qtextdist(lbl, ttl)
% QTEXTDIST - Specifies distance to text labels for QXAXIS and QYAXIS
%    QTEXTDIST(lbldist, ttldist) specifies distance between ticks and
%    tick labels and between tick labels and axis title, in points.
%    QTEXTDIST(dist) uses DIST for both distances.
%    Positive numbers are to the left and down; negative numbers are to the
%    right and up.
%    [lbl, ttl] = QTEXTDIST returns current settings.

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

  lbl = qp_data.info(idx).textdist(1);
  ttl = qp_data.info(idx).textdist(2);

else

  if nargin==1
    ttl = lbl;
  end
  
  if ischar(lbl)
    lbl = str2double(lbl);
  end
  if ischar(ttl)
    ttl = str2double(ttl);
  end
  
  qp_data.info(idx).textdist = [lbl ttl];

  clear lbl ttl
  
end

