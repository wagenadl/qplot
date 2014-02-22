function qbars(xx, yy, w, y0)
% QBARS - Bar plot with bar width specified in data coordinates
%    QBARS(xx, yy, w) draws a bar graph of YY vs XX with bars
%    of width W specified in data coordinates.
%    QBARS(xx, yy, w, y0) specifies the baseline of the plot;
%    default for Y0 is 0. Y0 may also be a vector (which must
%    then be the same size as XX and YY). This is useful for
%    creating stacked bar graphs.


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
