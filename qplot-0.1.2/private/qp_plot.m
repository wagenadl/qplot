function qp_plot(xx, yy, cmd)
% QPLOT - Draw a line series in data space
%    QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
%    coordinates. See also QLINE and QGLINE.

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
  cmd = 'plot';
end

fd = qp_fd(1);

if length(xx)~=prod(size(xx)) || ~isreal(xx)
  error('xx must be a real vector')
end
if length(yy)~=prod(size(yy)) || ~isreal(yy)
  error('yy must be a real vector')
end
if length(xx) ~= length(yy)
  error('xx and yy must be equally long');
end
xx=xx(:);
yy=yy(:);
if isempty(xx)
  return;
end

[iup, idn] = qp_schmitt(~isnan(xx+yy),.7,.3,2);

for k=1:length(iup)
  N = idn(k) - iup(k);
  fprintf(fd, '%s *%i *%i\n', cmd, N, N);
  fwrite(fd, xx(iup(k):idn(k)-1), 'double');
  fwrite(fd, yy(iup(k):idn(k)-1), 'double');
end

global qp_data;
idx = qp_idx;
dr = qp_data.info(idx).datarange;
mx = min(xx);
Mx = max(xx);
my = min(yy);
My = max(yy);
if isnan(dr(1)) || mx<dr(1)
  dr(1) = mx;
end
if isnan(dr(2)) || Mx>dr(2)
  dr(2) = Mx;
end
if isnan(dr(3)) || my<dr(3)
  dr(3) = my;
end
if isnan(dr(4)) || My>dr(4)
  dr(4) = My;
end
qp_data.info(idx).datarange = dr;

qp_flush(fd);
