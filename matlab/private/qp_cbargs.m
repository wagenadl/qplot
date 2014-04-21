function [dh,dx,dy] = qp_cbargs(dflt, varargin)

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

switch length(varargin)
case 0
  dh = dflt;
  dx = 0;
  dy = 0;
case 1
  dh = varargin{1};
  dx = 0;
  dy = 0;
case 2
  dx = varargin{1};
  dy = varargin{2};
  dh = dflt;
case 3
  dx = varargin{1};
  dy = varargin{2};
  dh = varargin{3};
otherwise
  error('QCBAR: syntax error');
end
