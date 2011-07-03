function qat(varargin)

fd = qp_ensure(1);

if nargin<2 | nargin>4
  error('Usage: qat x y [dx dy]|phi');
end

str = 'at';
for k=1:nargin
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