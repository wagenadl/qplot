function qat(varargin)
% QAT - Specify location for future text
%    QAT(x,y) specifies that future text will be placed at data location (x,y)
%    QAT(x,y, phi) specifies that the text will be rotated by phi radians
%    QAT(x,y, dx,dy) specifies that the text will be rotated s.t. the baseline
%    points in the data direction (dx,dy).
%    QAT without arguments reverts to absolute placement relative to topleft.
%    Either X or Y may also be nan (or '-') to have absolute placement in
%    one dimension

fd = qp_fd(1);

if nargin==0
  fprintf(fd,'at -\n');
  return;
end

if nargin<2 | nargin>4
  error('Usage: qat x y [dx dy]|phi');
end

str = 'at';
for k=1:nargin
  a = varargin{k};
  if ischar(a) & ~isnan(str2double(a))
    str = sprintf('%s %s', str, a);
  elseif isnscalar(a) & isreal(a) & ~isnan(a)
    str = sprintf('%s %g', str, a);
  elseif k==1 & ~isempty(strmatch(a, strtoks('left right center'), 'exact'))
    str = sprintf('%s %s', str, a);
  elseif k==2 & ~isempty(strmatch(a, strtoks('top bottom middle'), 'exact'))
    str = sprintf('%s %s', str, a);
  elseif k<=2 & ((ischar(a) & strcmp(a, '-')) | (isnscalar(a) & isnan(a)))
    str = sprintf('%s -', str);
  else
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);