function [y_min,y_max] = qp_sampleminmax(xx,ii)
% QP_SAMPLEMINMAX - Find minima and maxima in bins of sampled data
%    [y_min,y_max] = SAMPLEMINMAX(xx,ii) finds the minima and the maxima
%    of the data XX in the intervals [ii_1,ii_2), [ii_2,ii_3), ...,
%    [ii_n-1,ii_n). Note that xx(ii_n) is never used. 
%    Usage note: This is useful for plotting an electrode trace at just
%    the resolution of the screen, without losing spikes.

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

% warning('this should have been a mex/oct file');

N=length(ii)-1;
y_min=zeros(1,N);
y_max=zeros(1,N);

for n=1:N
  y_min(n) = min(xx(ii(n):ii(n+1)-1));
  y_max(n) = max(xx(ii(n):ii(n+1)-1));
end
