function qshiftedline(xx, yy, dx, dy)
% QSHIFTEDLINE - Renders a line displaced from data points
%   QSHIFTEDLINE(xx, yy, dx, dy) is like QPLOT(xx, yy) except that the 
%   plot is displaced by (dx, dy) points on the graph.
%   XX, YY, DX, DY may be vectors or scalars. Any scalars are automatically
%   converted to vectors of the appropriate length. All vectors must be
%   the same length.
%   See also QGLINE.

N = max([length(xx), length(yy), length(dx), length(dy)]);

if length(xx)==1
  xx = repmat(xx, N, 1);
end
if length(yy)==1
  yy = repmat(yy, N, 1);
end
if length(dx)==1
  dx = repmat(dx, N, 1);
end
if length(dy)==1
  dy = repmat(dy, N, 1);
end

ar = cell(N, 1);

for n=1:N
  ar{n} = { 'absdata', xx(n), yy(n), 'relpaper', dx(n), dy(n) };
end

qgline(ar{:});


