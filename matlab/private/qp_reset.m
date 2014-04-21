function qp_reset(idx)

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

global qp_data

qp_data.info(idx).ticklen = 3;
qp_data.info(idx).axshift = 0;
qp_data.info(idx).ytitlerot = pi/2;
qp_data.info(idx).textdist = [3 3];
qp_data.info(idx).lastax = '';
qp_data.info(idx).lut = repmat([0:.01:1]',[1 3]);
qp_data.info(idx).lut_nan = [1 1 1];
qp_data.info(idx).panels = {'-'};
qp_data.info(idx).panelextent = { };
qp_data.info(idx).panel = '-';
qp_data.info(idx).numfmt = '';
qp_data.info(idx).legopt = [];