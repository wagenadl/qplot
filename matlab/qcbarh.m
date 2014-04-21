function qcbarh(w, l, varargin)
% QCBARH - Add a horizontal color bar to a figure
%   QCBARH(w, h) adds a horizontal color bar of given width and height
%   (in points) at the position specified by QAT. W may be positive or 
%   negative. In either case, the color scale runs from left to right.
%   QCBARH(w, h, 'l') makes the color scale run right-to-left.
%   QCBARH(w, h, dx, dy) or QCBARH(w, h, dx, dy, 'l') shifts the bar by the 
%   given number of points to the right and down.
%   QCBARH(w, [], dw) or QCBARH(w,[], dx, dy, dw) specifies the width in data 
%   coordinates instead. In this case, the color scale runs l->r (r->l) if DW 
%   is positive (negative).
%   This command only works after a previous QIMSC.

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

[dw, dx, dy] = qp_cbargs('r', varargin{:});

idx = qp_idx;
global qp_data;
if ~isfield(qp_data.info(idx), 'atcoord')
  error('QCBARH needs a previous QAT');
end
xy = qp_data.info(idx).atcoord;

lut = qlut;
C = size(lut,1);

if isempty(w)
  w=0;
end
if l<0
  dy=dy+l;
  l=-l;
end
if w<0
  dx=dx+w;
  w=-w;
end

if ischar(dw)
  isright = strcmp(dw, 'r');
  xywh_d = [xy(1) xy(2) 0 0];
  xywh_p = [dx+w dy -w l];
else
  isright = dw>0;
  if dw<0
    xy(1) = xy(1)+dw;
    dw = -dw;
  end
  xywh_d = [xy(1) xy(2) dw 0];
  xywh_p = [dx+w dy -w l];
end
if ~isright
  lut = flipud(lut);
end
qgimage(xywh_d, xywh_p, reshape(lut,[1 C 3]));

idx = qp_idx;
global qp_data
qp_data.info(idx).cbar.xywh_d = xywh_d;
qp_data.info(idx).cbar.xywh_p = xywh_p;
qp_data.info(idx).cbar.orient = 'x';
qp_data.info(idx).cbar.rev = ~isright;
qp_data.info(idx).cbar.clim = qp_data.info(idx).clim;

