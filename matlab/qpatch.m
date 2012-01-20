function qpatch(xx, yy)
% QPATCH - Draw a polygonal patch in data space
%    QPATCH(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
%    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
%    The polygon is filled with the current brush.
%    XX and YY are given in data coordinates. See also QAREA and QGAREA.

qp_plot(xx, yy, 'patch');
