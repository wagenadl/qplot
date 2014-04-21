function qbars(xx, yy, w, y0)
% QBARS - Bar plot with bar width specified in data coordinates
%    QBARS(xx, yy, w) draws a bar graph of YY vs XX with bars
%    of width W specified in data coordinates.
%    QBARS(xx, yy, w, y0) specifies the baseline of the plot;
%    default for Y0 is 0. Y0 may also be a vector (which must
%    then be the same size as XX and YY). This is useful for
%    creating stacked bar graphs.

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


xx=xx(:)';
yy=yy(:)';
if nargin<4
  y0=0;
end
y0=y0(:)';
if length(y0)==1
  y0=repmat(y0,size(yy));
end

for k=1:length(xx)
  qpatch([-.5 .5 .5 -.5]*w+xx(k), [0 0 1 1]*yy(k)+y0(k));
end
