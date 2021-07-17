function qsharelim(varargin)
% QSHARELIM - Share axis limits between QPlot panels
%    QSHARELIM [x|y] ID ... shares x and/or y-axis limits with the other named
%    panels.

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

if nargin<1
  error('Usage: qsharelim [x|y] ID ...');
end

str = 'sharelim';
for k=1:nargin
  a = varargin{k};
  if ischar(a) 
    if k==1 && (strcmp(a, 'x') || strcmp(a, 'y'))
      str = sprintf('%s %s', str, a);
    elseif a(1)>='A' && a(1)<='Z'
      str = sprintf('%s %s', str, a);
    else
      error('Cannot interpret arguments');
    end
  else
    error('Cannot interpret arguments');  
  end
end

fprintf(fd, '%s\n', str);
qp_flush(fd);

