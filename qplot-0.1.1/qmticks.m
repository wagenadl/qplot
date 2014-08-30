function qmticks(xx)
% QMTICKS - Add more ticks to an existing axis

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

idx = qp_idx(1);
global qp_data

if isempty(qp_data.info(idx).lastax)
  error('No previous axis');
end

kv = qp_data.info(idx).lastax;
kv.lim_d=[];
kv.lim_p=[];
kv.tick_d = xx;
kv.tick_p = [];
kv.tick_lbl = {};
kv.ttl = [];
kv.ticklen = qticklen;
if strcmp(kv.orient,'y')
  kv.ticklen = -kv.ticklen;
end
if ~isempty(kv.cbar)
  kv.tick_d = qca_ctodat(kv.tick_d, kv.cbar);
end

qp_axis(kv);
