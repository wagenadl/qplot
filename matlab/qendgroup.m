function qendgroup
% QENDGROUP - Ends a group for bbox collection
fd = qp_fd(1);
fprintf(fd, 'endgroup\n');
