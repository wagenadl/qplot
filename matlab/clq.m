function clq 
% CLQ - Clear current QPlot figure
%   CLQ clears the current QPlot figure. 
global qp_data
fd = qp_fd(1);
fn = qp_data.curfn;
fclose(fd);
fd = fopen(fn, 'r');
l0 = fgets(fd);
fclose(fd);
fd = fopen(fn, 'w');
fprintf(fd, '%s', l0);
idx = strmatch(fn, qp_data.fns, 'exact');
qp_data.info(idx).fd = fd;

qp_reset(idx);

qp_flush(fd);

