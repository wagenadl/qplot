function qcbar(w, l, varargin)
% QCBAR - Add a vertical color bar to a figure
%   QCBAR(w, h) adds a vertical color bar of given width and height (in points)
%   at the position specified by QAT. H may be positive or negative. In either
%   case, the color scale runs from bottom to top.
%   QCBAR(w, h, 'd') makes the color scale run down.
%   QCBAR(w, h, dx, dy) or QCBAR(w, h, dx, dy, 'd') shifts the bar by the 
%   given number of points to the right and down.
%   QCBAR(w, [], h) or QCBAR(w,[], dx, dy, h) specifies the height in data 
%   coordinates instead. In this case, the color scale runs up (down) if H 
%   is positive (negative).
%   This command only works after a previous QIMSC.
%   QVCBAR and QHCBAR offer the same functionality with an easier interface.
%   See also QCAXIS.

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

[dh, dx, dy] = qp_cbargs('u', varargin{:});

idx = qp_idx;
global qp_data;
if ~isfield(qp_data.info(idx), 'atcoord')
  error('QCBAR needs a previous QAT');
end
xy = qp_data.info(idx).atcoord;

lut = qlut;
C = size(lut,1);

if isempty(l)
  l=0;
end
if l<0
  dy=dy+l;
  l=-l;
end
if w<0
  dx=dx+w;
  w=-w;
end

if ischar(dh)
  isup = strcmp(dh, 'u');
  xywh_d = [xy(1) xy(2) 0 0];
  xywh_p = [dx dy w l];
else
  isup = dh>0;
  if dh<0
    xy(2) = xy(2)+dh;
    dh = -dh;
  end
  xywh_d = [xy(1) xy(2) 0 dh];
  xywh_p = [dx dy w l];
end
if isup
  lut = flipud(lut);
end
qgimage(xywh_d, xywh_p, reshape(lut,[C 1 3]));

idx = qp_idx;
global qp_data
qp_data.info(idx).cbar.xywh_d = xywh_d;
qp_data.info(idx).cbar.xywh_p = xywh_p;
qp_data.info(idx).cbar.orient = 'y';
qp_data.info(idx).cbar.rev = ~isup;
qp_data.info(idx).cbar.clim = qp_data.info(idx).clim;

