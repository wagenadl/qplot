function [c0, c1] = qp_clim
% QP_CLIM - Get current color limits
%    [c0, c1] = QP_CLIM gets the color limits from the most recent QIMSC.

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
if isfield(qp_data.info(idx), 'clim')
  c0 = qp_data.info(idx).clim(1);
  c1 = qp_data.info(idx).clim(2);  
else
  c0 = 0;
  c1 = 1;
end

  