function qctext(x, y, varargin)
% QCTEXT - Render text after previous text
%   QCTEXT(ctext) renders text where previous text plotting left off.
%   QCTEXT(dx, dy, ctext) modifies placement by the given number of points.

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

if nargin==1
  txt = x;
  x = '';
  y = '';
else
  if nargin<3
    error('Usage: qctext [x y] ctext');
  end
  if isnscalar(x) && isreal(x)
    x = sprintf('%g', x);
  elseif isnan(str2double(x))  
    error('Usage: qctext [x y] ctext')
  end
  if isnscalar(y) && isreal(y)
    y = sprintf('%g', y);
  elseif isnan(str2double(y))  
    error('Usage: qctext [x y] ctext')
  end
  txt = varargin{1};
  for k=2:length(varargin);
    txt = [ txt ' ' varargin{k} ];
  end
end

fprintf(fd,'ctext %s %s "%s"\n',x, y, txt);

qp_flush(fd);
