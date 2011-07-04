function qendgroup
% QENDGROUP - Ends a group for bbox collection
fd = qp_ensure(1);
fprintf(fd, 'endgroup\n');
