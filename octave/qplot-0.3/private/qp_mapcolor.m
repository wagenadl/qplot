function str = qp_mapcolor(str)
switch str
  case 'r'
    str = 'red';
  case 'g'
    str = 'green';
  case 'b'
    str = 'blue';
  case 'm'
    str = 'magenta';
  case 'y'
    str = 'yellow';
  case 'c'
    str = 'cyan';
  case 'k'
    str = 'black';
  case 'w'
    str = 'white';
  otherwise
    str = [];
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

