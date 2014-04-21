function qmark(xx, yy)
% QMARK - Draw on the current graph with the current marker
%   QMARK(xx, yy) draws marks at the given location in data space. See also
%   QMARKER and QPMARK.
fd = qp_fd(1);

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

if isempty(xx)
  return
end

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
end
if ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
end
if length(xx) ~= length(yy)
  error('xx and yy must be equally long');
end

ok = ~isnan(xx(:)+yy(:));
xx=xx(ok);
yy=yy(ok);

fprintf(fd, 'mark *%i *%i\n', length(xx), length(yy));
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);

