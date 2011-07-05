function qpanel(varargin)

fd = qp_fd(1);

ok=1;
if nargin<1
  ok=0;
elseif nargin>5
  ok=0;
elseif nargin>1 & nargin<5
  ok=0;
end
if ~ok
  error('Usage: qpanel ID [x y w h] | -');
end
if ~ischar(varargin{1}) | length(varargin{1})>1
  error('Usage: qpanel ID [x y w h] | -');
end

str = sprintf('panel %s', varargin{1});
for k=2:nargin
  a = varargin{k};
  if ischar(a) & ~isnan(str2double(a))
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) & isreal(a)
    str = sprintf('%s %g', str, a);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);
