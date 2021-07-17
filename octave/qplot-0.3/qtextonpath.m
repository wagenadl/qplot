function qtextonpath(xx, yy, dx, dy, txt)
% QTEXTONPATH - Place text along a path
%    QTEXTONPATH(xx, yy, text) places the TEXT along a path (XX, YY)
%    defined in data coordinates.
%    QTEXTONPATH(xx, yy, dy, text) shifts the text down by DY pts in its 
%    local vertical direction.
%    QTEXTONPATH(xx, yy, dx, dy, text) shifts the text right by DX and
%    down by DY pts in its local direction.
%    QTEXTONPATH does not use coordinates set by QAT, but it does respect
%    alignment set by QALIGN.
%    In the present version, QTEXTONPATH only accepts plain Unicode; not
%    any of the special characters sequences accepted by QTEXT.

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

if nargin==3
  txt = dx;
  dx = 0;
  dy = 0;
elseif nargin==4
  txt = dy;
  dy = dx;
  dx = 0;
elseif nargin~=5
  error('Usage: qtextonpath xx yy [[dx] dy] text');
end

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
elseif ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
elseif length(xx) ~= length(yy)
  error('xx and yy must be equally long');
elseif ~isscalar(dx) || ~isreal(dx)
  error('dx must be a real scalar')
elseif ~isscalar(dy) || ~isreal(dy)
  error('dy must be a real scalar')
end

idx = find(~isnan(xx+yy));
xx = xx(idx);
yy = yy(idx);
N = length(xx);

fd = qp_fd(1);

fprintf(fd, 'textonpath *%i *%i %g %g "%s"\n', N, N, dx, dy, txt);
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);
