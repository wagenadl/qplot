function qpanel(varargin)
% QPANEL - Define a new subpanel or reenter a previous one
%    QPANEL(id, x, y, w, h) or QPANEL(id, xywh) defines a new panel.
%    QPANEL(id) revisits a previously defined panel. ID must be a single
%    capital or a dash ('-') to revert to the top level.
%    Coordinates are in points from top left.
%    See also QSUBPLOT.

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

ok=0;
if nargin==1
  ok=1;
elseif nargin==5
  ok=1;
elseif nargin==2
  if length(varargin{2})==4
    xywh = varargin{2};
    varargin{2} = xywh(1);
    varargin{3} = xywh(2);
    varargin{4} = xywh(3);
    varargin{5} = xywh(4);
    ok=1;
  end
end

if ~ok
  error('Usage: qpanel ID [x y w h] | -');
end
id = varargin{1};
if ~ischar(id) 
  error('Usage: qpanel ID [x y w h] | -');
end
if strcmp(id,'-') && length(varargin)>1
  error('Usage: qpanel ID [x y w h] | -');
end

str = sprintf('panel %s', id);
xywh = [];
for k=2:length(varargin)
  a = varargin{k};
  if ischar(a) && ~isnan(str2double(a))
    xywh(end+1) = str2double(a);
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) && isreal(a)
    xywh(end+1) = a;
    str = sprintf('%s %g', str, a);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);

idx = qp_idx;
global qp_data;
oldidx = strmatch(id, qp_data.info(idx).panels, 'exact');
if isempty(oldidx)
  qp_data.info(idx).panels{end+1} = id;
  oldidx = length(qp_data.info(idx).panels);
end
if ~isempty(xywh)
  n = 1 + id-'A';
  qp_data.info(idx).panelextent{oldidx} = xywh;
end
qp_data.info(idx).panel = id;

