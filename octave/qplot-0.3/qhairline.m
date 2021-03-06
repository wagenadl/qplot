function qhairline(x)
% QHAIRLINE - Specify hairline width
%    QHAIRLINE(width) specifies the width of hairlines (lines with 
%    nominal width 0) as rendered to screen or pdf.
%    The default is 0.25 pt when rendering to pdf. When rendering to
%    screen, the default is 0, which implies "one pixel wide".

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

if nargin~=1
  qhairline_usage;
end
if ischar(x)
  x = str2double(x);
end
if ~isnscalar(x)
  qhairline_usage;
end

fprintf(fd, 'hairline %g\n', x);
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function qhairline_usage()
error('Usage: qhairline width');


