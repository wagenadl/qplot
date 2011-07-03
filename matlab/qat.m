function qat(varargin)
% QAT - Specify location for future text
%    QAT(x,y) specifies that future text will be placed at data location (x,y)
%    QAT(x,y, phi) specifies that the text will be rotated by phi radians
%    QAT(x,y, dx,dy) specifies that the text will be rotated s.t. the baseline
%    points in the data direction (dx,dy).

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
  elseif k==1 & ~isempty(strmatch(a, strtoks('left right center cleft cright ccenter'), 'exact'))
    str = sprintf('%s %s', str, a);
  elseif k==2 & ~isempty(strmatch(a, strtoks('top bottom middle ctop cbottom cmiddle'), 'exact'))
    str = sprintf('%s %s', str, a);
  else    
    error('Cannot interpret arguments');
  end
end

fprintf(fd, '%s\n', str);