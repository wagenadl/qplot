function qlegend(str)
% QLEGEND - Render legend element for plotted line
%    QLEGEND(str) renders a sample of the most recently plotted line
%    at the location set by QLEGOPT and writes the given string
%    next to it.
%    See also QMLEGEND and QPLEGEND.

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

qlegopt; % ensure that we have options
global qp_data;
idx = qp_idx(1);
opt = qp_data.info(idx).legopt;

qat(opt.x0, opt.y0);
qline([0 1]*opt.width+opt.dx, opt.n*opt.skip + [0 0]+opt.dy);
qgroup
qpen(opt.color);
qalign left base
qtext(opt.width+opt.indent+opt.dx, opt.n*opt.skip + opt.drop+opt.dy, str);
qendgroup

qp_data.info(idx).legopt.n = opt.n + 1;
