function qcaligraph(xx, yy, ww)
% QCALIGRAPH - Draw a variable-width line series in data space
%    QCALIGRAPH(xx, yy, ww) plots the data YY vs XX. XX and YY are given in 
%    data coordinates. WW specifies the line width at each point, in postscript
%    points.
%    The line is rendered in the current pen's color; dash patterns and cap
%    and join styles are not used.

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

if nargin<3
  error('Usage: qcaligraph xx yy ww');
end

fd = qp_fd(1);

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
end
if ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
end
if ~isnvector(ww) || ~isreal(ww)
  error('ww must be a real vector')
end
if length(xx) ~= length(yy) || length(xx) ~= length(ww)
  error('xx, yy, and ww must be equally long');
end
xx=xx(:);
yy=yy(:);
ww=ww(:);

[iup, idn] = qp_schmitt(~isnan(xx+yy+ww),.7,.3,2);

for k=1:length(iup)
  N = idn(k) - iup(k);
  fprintf(fd, 'caligraph *%i *%i *%i\n', N, N, N);
  fwrite(fd, xx(iup(k):idn(k)-1), 'double');
  fwrite(fd, yy(iup(k):idn(k)-1), 'double');
  fwrite(fd, ww(iup(k):idn(k)-1), 'double');
end

qp_flush(fd);
