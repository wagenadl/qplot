function qshrink(varargin)
% QSHRINK - Add margin to QPlot panel
%    QSHRINK adds 1 point of margin to the current QPlot panel.
%    QSHRINK(margin) adds the given margin (in points).
%    QSHRINK(margin, ratio) forces a given aspect ratio on the data units.

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

if nargin>2
  error('Usage: qshrink [margin] [ratio]');
end

str = 'shrink';
for k=1:nargin
  a = varargin{k};
  if strcmp(a, '-') && k<nargin
    str = sprintf('%s -', str);
  elseif ischar(a) && ~isnan(str2double(a))
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) && isreal(a)
    str = sprintf('%s %g', str, a);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);
qp_flush(fd);

