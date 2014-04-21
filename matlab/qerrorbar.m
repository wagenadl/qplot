function qerrorbar(xx, yy, dy, varargin)
% QERRORBAR - Draw error bars
%    QERRORBAR(xx, yy, dy) plots error bars at (XX,YY+-DY).
%    Normally, XX, YY, and DY have the same shape. However, it is permissible
%    for DY to be shaped Nx2, in which case lower and upper error bounds
%    are different. (DY should always be positive).
%    QERRORBAR(xx, yy, dy, w) adorns the error bars with horizontal lines of
%    given width (W in points).
%    QERRORBAR(..., 'up') only plots upward; QERRORBAR(..., 'down') only plots
%    downward.

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

dir = 'both';
w = 0;
while ~isempty(varargin)
  if ischar(varargin{1})
    dir = varargin{1};
  else
    w = varargin{1};
  end
  varargin=varargin(2:end);
end

xx = xx(:);
yy = yy(:);
N = length(xx);
if prod(size(dy))==2*N
  dy_dn = -dy(:,1);
  dy_up = dy(:,2);
else
  dy_up = dy(:);
  dy_dn = -dy(:);
end

switch dir
  case 'both'
    for n=1:N
      qplot(xx(n)+[0 0],yy(n)+[dy_dn(n) dy_up(n)]);
    end
  case 'up'
    for n=1:N
      qplot(xx(n)+[0 0],yy(n)+[0 dy_up(n)]);
    end
  case 'down'
    for n=1:N
      qplot(xx(n)+[0 0],yy(n)+[dy_dn(n) 0]);
    end
  otherwise
    error([ 'Bad direction name: ' dir]);
end

if w>0 
  if ~strcmp(dir, 'down')
    % Draw top ticks
    for n=1:N
      qat(xx(n), yy(n)+dy_up(n));
      qline([-1 1]*w/2,[0 0]);
    end
  end
  if ~strcmp(dir, 'up')
    % Draw down ticks
    for n=1:N
      qat(xx(n), yy(n)+dy_dn(n));
      qline([-1 1]*w/2,[0 0]);
    end
  end
end

     