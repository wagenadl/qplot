function qplot(xx, yy)
% QPLOT - Draw a line series in data space
%    QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
%    coordinates. See also QLINE and QGLINE.

if nargin==1
  yy = xx;
  xx = [1:length(yy)];
end

qp_plot(xx, yy, 'plot');
