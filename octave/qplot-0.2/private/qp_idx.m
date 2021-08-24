function idx = qp_idx(autofig)

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

qp_ensure;
global qp_data

if nargin==0
  autofig=0;
end

if isempty(qp_data.curfn)
  if autofig>0
    qfigure;
  else
    error('No open window');
  end
end

idx = strmatch(qp_data.curfn, qp_data.fns, 'exact');
if isempty(idx)
  error('No open window');
end

