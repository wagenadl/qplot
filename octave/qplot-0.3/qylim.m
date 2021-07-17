function qylim(varargin)
% QYLIM - Set y-axis limits
%   QYLIM(y0, y1) sets y-axis limits in the current panel.

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
  a = varargin{1};
  if isnvector(a) && length(a)==2
    fprintf(fd,'ylim %g %g\n',a(1), a(2));
    qp_flush(fd);
    return;
  end
end

if nargin<2 || nargin>2
  error('Usage: qylim x0 x1');
end

str = 'ylim';
for k=1:nargin
  a = varargin{k};
  if ischar(a) && ~isnan(str2double(a))
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) && isreal(a)
    str = sprintf('%s %g', str, a);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);
qp_flush(fd);

