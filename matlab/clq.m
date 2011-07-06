function clq 
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
qp_data.info(idx).ticklen = 3;
qp_data.info(idx).textdist = [3 3];
qp_data.info(idx).lastax = '';
qp_data.info(idx).lut = repmat([0:.01:1]',[1 3]);
qp_data.info(idx).panels = {'-'};
