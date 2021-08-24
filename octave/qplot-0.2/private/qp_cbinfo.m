function cb = qp_cbinfo
% QP_CBINFO - Extract information about colorbar
%    cb = QP_CBINFO extracts information about the most recent QCOLORBAR.
%    CB will be a struct with fields:
%      hori: 1/0 if the colorbar is horizontal/vertical
%      flip: 1/0 if the orientation is flipped
%      c0: lower limit of data range represented
%      c1: upper limit of data range represented
%      xywh: rectangle of the colorbar in data space

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

if ~isfield(qp_data.info(idx), 'cbar')
  error('QP_CBINFO cannot function without a colorbar');
end

cb = qp_data.info(idx).cbar;
[cb.c0, cb.c1] = qp_clim;

