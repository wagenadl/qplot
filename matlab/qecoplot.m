function qecoplot(x0, dx, yy, N)
% QECOPLOT - Economically plot large datasets
%    QECOPLOT(xx, yy, N) plots the data (xx,yy) using SAMPLEMINMAX to
%    reduce data length to the given number of points.
%    The results are plotted as a QPATCH.
%    It is mandatory that XX is uniformly spaced.
%    QECOPLOT(x0, dx, yy, N) specifies x-coordinates in a more efficicient
%    way: xx = (x0, x0+dx, x0+2*dx, ...).
%    If N is omitted, it defaults to 100.
%    Note: This is the kind of plot that MEABench calls "TrueBlue".

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

if length(x0)>1
  % Called as (xx, yy, ...)
  if nargin>=3
    N = yy;
  else
    N = [];
  end
  yy = dx;
  dx = mean(diff(x0));
  if any(abs(diff(x0) - dx) > .05*dx)
    error('qecoplot: XX vector must be uniformly spaced')
  end
  x0 = x0(1);
elseif nargin<4
  N = [];
end

if isempty(N)
  N = 100;
end

K = length(yy);

if N>K
  N=K;
end

ii = 1 + ceil([0:N]/N * K);
[ym, yM] = qp_sampleminmax(yy, ii);
ii = ii(1:end-1) - .5;

qpatch(x0+dx*[ii fliplr(ii)], [ym fliplr(yM)]);
