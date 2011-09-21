function qtext(x, y, varargin)
% QTEXT - Render text 
%   QTEXT(text) renders text at the current anchor point.
%   QTEXT(dx, dy, text) renders text displaced by the given number of points.

fd = qp_fd(1);

if nargin==1
  txt = x;
  x = '0';
  y = '0';
else
  if nargin<3
    error('Usage: qtext x y text');
  end
  if isnscalar(x) & isreal(x)
    x = sprintf('%g', x);
  end
  if isnscalar(y) & isreal(y)
    y = sprintf('%g', y);
  end
  
  txt = varargin{1};
  for k=2:length(varargin);
    txt = [ txt ' ' varargin{k} ];
  end
end

if isnan(str2double(x)) | isnan(str2double(y))
  error('Usage: qtext x y text');
end

fprintf(fd,'text %s %s "%s"\n',x, y, txt);
