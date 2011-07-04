function qgroup
% QGROUP - Starts a group for bbox collection
fd = qp_ensure(1);
fprintf(fd, 'group\n');
