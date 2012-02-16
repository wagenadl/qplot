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

if nargin<1 || nargin>4
  error('Cannot interpret arguments');
end

str = 'at';
atcoord = zeros(length(nargin),1) + nan;
  
if ischar(varargin{1}) && ~isempty(varargin{1}) && ...
      varargin{1}(1)>='A' && varargin{1}(1)<='Z'
  % at ID [dx dy]|[angle]
  str = sprintf('%s %s', str, varargin{1});
  if nargin>3
    error('Cannot interpret arguments following ID');
  end
  for k=2:nargin
    a = varargin{k};
    if ischar(a) && ~isnan(str2double(a))
      str = sprintf('%s %s', str, a);
    elseif isnscalar(a) && isreal(a) && ~isnan(a)
      str = sprintf('%s %g', str, a);
    else
      error('Cannot interpret arguments following ID');
    end
  end
else
  if nargin<2
    error('Cannot interpret arguments');
  end
  % at x y [dx dy]|[angle]|[ID]
  for k=1:nargin
    a = varargin{k};
    if nargin==3 && k==3 && ischar(a) && a>='A' && a<='Z'
      str = sprintf('%s %s', str, a); % add ID
    elseif ischar(a) && ~isnan(str2double(a))
      str = sprintf('%s %s', str, a);
      atcoord(k) = str2double(a);
    elseif isnscalar(a) && isreal(a) && ~isnan(a)
      str = sprintf('%s %g', str, a);
      atcoord(k) = a;
    elseif k==1 && ischar(a) && ~isempty(strmatch(a, strtoks('left right center'), 'exact'))
      str = sprintf('%s %s', str, a);
    elseif k==2 && ischar(a) && ~isempty(strmatch(a, strtoks('top bottom middle'), 'exact'))
      str = sprintf('%s %s', str, a);
    elseif k<=2 && ((ischar(a) && strcmp(a, '-')) || (isnscalar(a) && isnan(a)))
      str = sprintf('%s -', str);
    else
      error('Cannot interpret arguments');
    end
  end
end

fprintf(fd, '%s\n', str);

idx = qp_idx;
global qp_data;
qp_data.info(idx).atcoord = atcoord;
