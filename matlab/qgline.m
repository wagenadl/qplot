function qgline(varargin)
% QGLINE - Generalized line drawing
%   QGLINE(ptspec1, ptspec2, ...).

fd = qp_fd(1);

args = varargin;
if length(args)==1 & iscell(args)
  args = args{:};
end

cmd = 'gline';
for k=1:length(args)
  cmd = [ cmd ' (' ];
  for q=1:length(args{k})
    x = args{k}{q};
    if ischar(x)
      cmd = [ cmd ' ' x ];
    else
      cmd = [ cmd ' ' sprintf('%g', x) ];
    end
  end
  cmd = [ cmd ' )' ];
end

fprintf(fd, '%s\n', cmd);
