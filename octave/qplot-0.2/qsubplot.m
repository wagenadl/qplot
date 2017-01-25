function id = qsubplot(x, y, w, h)
% QSUBPLOT - Define a new subpanel in relative units
%    QSUBPLOT(x, y, w, h) defines a new subpanel. X, Y, W, H are specified
%    as fractions of the figure size.
%    QSUBPLOT(rows, cols, idx) defines a new subpanel in Matlab style.
%    id = QSUBPLOT(...) returns the ID of the subpanel, for use with QPANEL.

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

if nargin==1
  xywh = x;
  x = xywh(1);
  y = xywh(2);
  w = xywh(3);
  h = xywh(4);
end
if ischar(x)
  x = str2double(x);
end
if ischar(y)
  y = str2double(y);
end
if ischar(w)
  w = str2double(w);
end
if nargin>=4 && ischar(h)
  h = str2double(h);
end
if nargin==3
  rows = x;
  cols = y;
  idx = w;
  h=1/rows;
  w=1/cols;
  x=w*mod(idx-1, cols);
  y=h*floor((idx-1)/cols);
end

idx = qp_idx(1);
global qp_data;
extent = qp_data.info(idx).extent;

x = extent(1) + extent(3)*x;
y = extent(2) + extent(4)*y;
w = extent(3)*w;
h = extent(4)*h;

subno = 1;
while 1
  id = qp_id(subno);
  oldidx = strmatch(id, qp_data.info(idx).panels, 'exact');
  if isempty(oldidx)
    break;
  else
    subno = subno + 1;
  end
end

qpen none
qbrush none
qpanel(id, x, y, w, h);
qpen solid

if nargout==0
  clear id
end
