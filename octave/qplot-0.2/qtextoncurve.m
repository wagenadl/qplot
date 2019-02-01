function qtextoncurve(xx, yy, dy, txt)
if nargin==3
  txt = dy;
  dy = 0;
elseif nargin~=4
  error('Usage: qtextoncurve xx yy [dy] text');
end

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

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
elseif ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
elseif length(xx) ~= length(yy)
  error('xx and yy must be equally long');
elseif ~isscalar(dy) || ~isreal(dy)
  error('dy must be a real scalar')
end

idx = find(~isnan(xx+yy));
xx = xx(idx);
yy = yy(idx);
N = length(xx);

fd = qp_fd(1);

fprintf(fd, 'textoncurve *%i *%i %g "%s"\n', N, N, dy, txt);
fwrite(fd, xx, 'double');
fwrite(fd, yy, 'double');

qp_flush(fd);
