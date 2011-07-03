function qfudge(varargin)

fd = qp_ensure(1);

if nargin>2
  error('Usage: qfudge [margin] [ratio]');
end

str = 'fudge';
for k=1:nargin
  a = varargin{k};
  if strcmp(a, '-') & k<nargin
    str = sprintf('%s -', str);
  elseif ischar(a) & ~isnan(str2double(a))
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) & isreal(a)
    str = sprintf('%s %g', str, a);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);