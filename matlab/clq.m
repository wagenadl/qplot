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
qp_data.fd(strmatch(fn, qp_data.fn, 'exact')) = fd;

