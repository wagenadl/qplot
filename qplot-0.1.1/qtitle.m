function qtitle(ttl)
% QTITLE - Render a title on the current QPlot
%    QTITLE(text) renders the given text centered along the top of the
%    current QPlot figure.

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

fd = qp_fd(1);
idx = qp_idx;
global qp_data

qat;
pid = qp_data.info(idx).panel;
if pid=='-'
  xywh = qp_data.info(idx).extent;
else
  oldidx = strmatch(pid, qp_data.info(idx).panels, 'exact');
  if isempty(oldidx)
    error('Confused about panels');
  end
  xywh = qp_data.info(idx).panelextent{oldidx};
end

qalign top center
qtext(xywh(1) + xywh(3)/2, xywh(2) + 5, ttl);
