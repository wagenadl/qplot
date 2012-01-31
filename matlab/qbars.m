function qbars(xx, yy, w, y0)
% QBARS - Bar plot with bar width specified in data coordinates
%    QBARS(xx, yy, w) draws a bar graph of YY vs XX with bars
%    of width W specified in data coordinates.
%    QBARS(xx, yy, w, y0) specifies the baseline of the plot;
%    default is 0.


xx=xx(:)';
yy=yy(:)';
if nargin<4
  y0=0;
end

for k=1:length(xx)
  qpatch([-.5 .5 .5 -.5]*w+xx(k), [0 0 1 1]*yy(k)+y0);
end
