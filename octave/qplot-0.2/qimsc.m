function qimsc(varargin)
% QIMSC - Plot 2D data as an image using lookup table
%    QIMSC(xywh, data) plots the DATA as an image using a lookup previously
%    set by QLUT. The color axis limits default to the min and max of the data.
%    QIMSC(xywh, data, c0, c1) overrides those limits.
%    QIMSC(xx, yy, data) or QIMSC(xx, yy, data, c0, c1) specifies bin centers.
%    QIMSC(data) or QIMSC(data, c0, c1) sets XYWH to (0,0)+(X,Y) as in QIMAGE.

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

switch nargin
  case 1
    data = varargin{1};
    c0 = min(data(:));
    c1 = max(data(:));
    [Y X] = size(data);
    xywh = [0 0 X Y];
  case 2
    xywh = varargin{1};
    data = varargin{2};
    [Y X] = size(data);
    c0 = min(data(:));
    c1 = max(data(:));
  case 3    
    if isnscalar(varargin{3})
      % So we have QIMSC(data, c0, c1)
      data = varargin{1};
      c0 = varargin{2};
      c1 = varargin{3};
      [Y X] = size(data);
      xywh = [0 0 X Y];
    else
      % So we have QIMSC(xx, yy, data)
      xx = varargin{1};
      yy = varargin{2};
      data = varargin{3};
      [Y X] = size(data);
      if X==1
	dx = 1;
      else
	dx = (xx(end)-xx(1))/(X-1);
      end
      if Y==1
	dy = 1;
      else
	dy = (yy(end)-yy(1))/(Y-1);
      end
      xywh = [xx(1)-dx/2 yy(1)-dy/2 X*dx Y*dy];
      c0 = min(data(:));
      c1 = max(data(:));
      data = flipud(data);
    end
  case 4
    xywh = varargin{1};
    data = varargin{2};
    [Y X] = size(data);
    c0 = varargin{3};
    c1 = varargin{4};
  case 5
    xx = varargin{1};
    yy = varargin{2};
    data = varargin{3};
    c0 = varargin{4};
    c1 = varargin{5};
    [Y X] = size(data);
    if X==1
      dx = 1;
    else
      dx = (xx(end)-xx(1))/(X-1);
    end
    if Y==1
      dy = 1;
    else
      dy = (yy(end)-yy(1))/(Y-1);
    end
    xywh = [xx(1)-dx/2 yy(1)-dy/2 X*dx Y*dy];
    data = flipud(data);
  otherwise
    error('qimsc takes 1 to 5 arguments');
end

idx = qp_idx(1);
global qp_data;
lut = qp_data.info(idx).lut;
nanc = qp_data.info(idx).lut_nan;
qp_data.info(idx).clim = [c0 c1];

[N C] = size(lut);
data = floor(1+(N-.0001)*double(data-c0)/(c1-c0)); % normalize to color range
data(data<1)=1;
data(data>N)=N;

isn = find(isnan(data));
data(isn)=1;
imd = lut(reshape(data,[Y*X 1]),:);
imd(isn,:) = repmat(nanc(:)',length(isn),1);

qimage(xywh, reshape(imd, [Y X C]));
