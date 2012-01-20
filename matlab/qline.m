function qline(xx, yy)
% QLINE - Draw a line series in paper space
%    QLINE(xx, yy) draws a line series between the points (XX,YY).
%    XX and YY are given in postscript points. See also QPLOT and QGLINE.

qp_plot(xx, yy, 'line');
