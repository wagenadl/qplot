function qreftext(varargin)
% QREFTEXT - Set reference text
%    QREFTEXT(text) sets the reference text used for vertical alignment
%    of subsequent QTEXT commands.
fd = qp_fd(1);

if nargin<1
  fprintf(fd, 'reftext\n');
else
  txt = varargin{1};
  for k=2:length(varargin);
    txt = [ txt ' ' varargin{k} ];
  end
  fprintf(fd,'reftext "%s"\n', txt);
end
