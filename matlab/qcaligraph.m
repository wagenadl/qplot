function qcaligraph(xx, yy, ww)
% QCALIGRAPH - Draw a variable-width line series in data space
%    QCALIGRAPH(xx, yy, ww) plots the data YY vs XX. XX and YY are given in 
%    data coordinates. WW specifies the line width at each point, in postscript
%    points.
%    The line is rendered in the current pen's color; dash patterns and cap
%    and join styles are not used.

if nargin<3
  error('Usage: qcaligraph xx yy ww');
end

fd = qp_fd(1);

if ~isnvector(xx) || ~isreal(xx)
  error('xx must be a real vector')
end
if ~isnvector(yy) || ~isreal(yy)
  error('yy must be a real vector')
end
if ~isnvector(ww) || ~isreal(ww)
  error('ww must be a real vector')
end
if length(xx) ~= length(yy) || length(xx) ~= length(ww)
  error('xx, yy, and ww must be equally long');
end
xx=xx(:);
yy=yy(:);
ww=ww(:);

[iup, idn] = qp_schmitt(~isnan(xx+yy+ww),.7,.3,2);

for k=1:length(iup)
  N = idn(k) - iup(k);
  fprintf(fd, 'caligraph *%i *%i *%i\n', N, N, N);
  fwrite(fd, xx(iup(k):idn(k)-1), 'double');
  fwrite(fd, yy(iup(k):idn(k)-1), 'double');
  fwrite(fd, ww(iup(k):idn(k)-1), 'double');
end

qp_flush(fd);
