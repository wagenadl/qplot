function qhcbar(y0, x0, x1, w)
% QHCBAR - Add a horizontal color bar to a figure
%   QHCBAR(y0, x0, x1) adds a horizontal color bar to the figure between
%   (X0, Y0) and (X1, Y0), expressed in data coordinates.
%   If X1>X0, the color bar to the right, else to the left.
%   QHCBAR(..., w) specifies the width of the color bar in points (default:
%   5 points). If W is positive, the bar extends down below Y0, otherwise 
%   to the left.
%   This only works after a preceding QIMSC and uses the lookup table (QLUT)
%   used by that QIMSC.
%   QHCBAR uses QAXSHIFT to create distance between Y0 and the color bar.
%   Positive QAXSHIFT creates space, negative creates overlap.
%   QHCBAR without arguments creates a color bar below the QIMSC.
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


idx = qp_idx;
global qp_data;
lut = qlut;
C = size(lut,1);

if ~isfield(qp_data.info(idx), 'clim') ...
      || ~isfield(qp_data.info(idx), 'imrect')
  error('qhcbar needs a preceding qimsc');
end

if nargin==0
  xywh = qp_data.info(idx).imrect;
  x0 = xywh(1);
  y0 = xywh(2);
  x1 = xywh(1) + xywh(3);
  w = 5;
  fprintf(1, 'qhcbar(%g, %g, %g, %g);\n', y0, x0, x1, w);
elseif nargin<4
  w = 5;
end

dy = qaxshift;
if w<0
  dy = -dy;
end

isright = x1>x0;

if isright
  xywh_d = [x0 y0 x1-x0 0];
else
  xywh_d = [x1 y0 x0-x1 0];
end

xywh_p = [0 dy 0 w];

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


