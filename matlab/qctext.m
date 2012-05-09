function qctext(x, y, varargin)
% QCTEXT - Render ctext 
%   QCTEXT(ctext) renders ctext at the current anchor point.
%   QCTEXT(dx, dy, ctext) renders ctext displaced by the given number of points.

fd = qp_fd(1);

if nargin==1
  txt = x;
  x = '';
  y = '';
else
  if nargin<3
    error('Usage: qctext [x y] ctext');
  end
  if isnscalar(x) && isreal(x)
    x = sprintf('%g', x);
  elseif isnan(str2double(x))  
    error('Usage: qctext [x y] ctext')
  end
  if isnscalar(y) && isreal(y)
    y = sprintf('%g', y);
  elseif isnan(str2double(y))  
    error('Usage: qctext [x y] ctext')
  end
  txt = varargin{1};
  for k=2:length(varargin);
    txt = [ txt ' ' varargin{k} ];
  end
end

fprintf(fd,'ctext %s %s "%s"\n',x, y, txt);

qp_flush(fd);
