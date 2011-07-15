function id = qsubplot(x, y, w, h)
% QSUBPLOT - Define a new subpanel in relative units
%    QSUBPLOT(x, y, w, h) defines a new subpanel. X, Y, W, H are specified
%    as fractions of the figure size.
%    id = QSUBPLOT(...) returns the ID of the subpanel, for use with QPANEL.

if nargin==1
  xywh = x;
  x = xywh(1);
  y = xywh(2);
  w = xywh(3);
  h = xywh(4);
end
if ischar(x)
  x = str2double(x);
end
if ischar(y)
  y = str2double(y);
end
if ischar(w)
  w = str2double(w);
end
if ischar(h)
  h = str2double(h);
end

idx = qp_idx(1);
global qp_data;
extent = qp_data.info(idx).extent;

x = extent(1) + extent(3)*x;
y = extent(2) + extent(4)*y;
w = extent(3)*w;
h = extent(4)*h;

subno = 1;
while 1
  id = qp_id(subno);
  oldidx = strmatch(id, qp_data.info(idx).panels, 'exact');
  if isempty(oldidx)
    break;
  else
    subno = subno + 1;
  end
end

qpen none
qbrush none
qpanel(id, x, y, w, h);
qpen solid
