function qfont(varargin)
% QFONT - Select font 
%    QFONT family [bold] [italic] size  selects a new font for QPLOT.

fd = qp_fd(1);

if nargin<2 | nargin>4
  qfont_usage;
end
if isnscalar(varargin{end})
  varargin{end} = sprintf('%g', varargin{end});
end
for k=1:nargin
  if ~ischar(varargin{k})
    qfont_usage;
  end
end
for k=2:nargin-1
  if isempty(strmatch(varargin{k},strtoks('bold italic'), 'exact'))
    qfont_usage;
  end
end

str = 'font';
for k=1:nargin
  str = [ str ' ' varargin{k} ];
end
fprintf(fd, '%s\n', str);

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function qfont_usage()
  error('Usage: qfont family [bold] [italic] size');