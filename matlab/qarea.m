function qarea(xx, yy)
% QAREA - Draw a polygon in paper space
%    QAREA(xx, yy) draws a polygon with vertices at (XX,YY). The polygon
%    is closed (i.e., it is not necessary for xx(end) to equal xx(1)).
%    The polygon is filled with the current brush.
%    XX and YY are given in postscript points. See also QPATCH and QGAREA.

qp_plot(xx, yy, 'area');
