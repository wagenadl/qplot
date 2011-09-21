function qalign(varargin)
% QALIGN - Set alignment for following text
%   QALIGN left|right|center|top|bottom|middle|base sets alignment for
%   subsequent QTEXT commands.
fd = qp_fd(1);

if nargin<1
  error('Usage: qalign left|right|center|top|bottom|middle|base ...');
end

txt = 'align';
for k=1:nargin
  if isempty(strmatch(varargin{k}, ...
	strtoks('left right center top bottom middle base')))
    error('Usage: qalign left|right|center|top|bottom|middle|base ...');
  end
  txt = [ txt ' ' varargin{k} ];
end

fprintf(fd, '%s\n', txt);

