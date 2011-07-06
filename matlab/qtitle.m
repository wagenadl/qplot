function qtitle(ttl)

fd = qp_fd(1);
idx = qp_idx;
global qp_data

qat;
xywh = qp_data.info(idx).extent;
qalign top center
qtext(xywh(3)/2, 5, ttl);
