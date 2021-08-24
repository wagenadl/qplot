function qmarker(varargin)
% QMARKER - Select a new marker for QMARK and QPMARK
%    QMARKER open|solid|brush  +|x|-|||o|s|d|<|>|^|v|p|h  size
%    selects a marker. An "open" mark is outlined with the current pen
%    and filled with white; a "solid" mark is outlined with the current pen
%    and filled with its color; a "brush" mark is outlined with the current
%    pen and filled with the current brush (which may be "none").
%    Marks are: o: circle/disk
%               + x: horizontal+vertical or diagonal crosses
%               - |: horizontal or vertical lines
%               s d p h: square, diamond, pentagon, or hexagon
%               < > ^ v: left / right / up / down pointing triangles
%    The fill style has no effect on +|x|-|| marks.

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

for n=1:nargin
  a = varargin{n};
  if ischar(a)
    if strmatch(a, strtoks('open solid brush'), 'exact')
      ; % This is a known keyword, so good
    elseif ~isempty(qp_mapmarker(a))
      ; % This is a good marker
      varargin{n} = qp_mapmarker(a);
    elseif ~isnan(str2double(a)) 
      ; % This is a number: size
    else
      error([ 'Cannot interpret ' a ' as an argument for qmarker' ]);
    end
  elseif isnscalar(a) && isreal(a)
    ; % This is size
    varargin{n} = sprintf('%g', a);
  else
    error([ 'Cannot interpret ' disp(a) ' as an argument for qmarker' ]);
  end
end

str = 'marker';
for n=1:nargin
  str = [ str ' ' varargin{n}];
end

fprintf(fd, '%s\n', str);
qp_flush(fd);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function str = qp_mapmarker(str)
switch str
  case 'o'
    str = 'circle';
  case 's'
    str = 'square';
  case 'd'
    str = 'diamond';
  case '<'
    str = 'left';
  case '>'
    str = 'right';
  case '^' 
    str = 'up';
  case 'v'
    str = 'down';
  case 'p'
    str = 'penta';
  case 'h'
    str = 'hexa';
  case '+'
    str = 'plus';
  case 'x'
    str = 'cross';
  case '-'
    str = 'hbar';
  case '|'
    str = 'vbar';
  otherwise
    str = [];
end


