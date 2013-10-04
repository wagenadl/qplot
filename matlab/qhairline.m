function qhairline(x)
% QHAIRLINE - Select hairline 
%    QHAIRLINE family [bold] [italic] size  selects a new hairline for QPlot.

fd = qp_fd(1);

if nargin~=1
  qhairline_usage;
end
if ischar(x)
  x = str2double(x);
end
if ~isnscalar(x)
  qhairline_usage;
end

fprintf(fd, 'hairline %g\n', x);
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function qhairline_usage()
error('Usage: qhairline width');


