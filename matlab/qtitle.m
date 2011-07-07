function qtitle(ttl)

fd = qp_fd(1);
idx = qp_idx;
global qp_data

qat;
pid = qp_data.info(idx).panel;
if pid=='-'
  xywh = qp_data.info(idx).extent;
else
  xywh = qp_data.info(idx).panelextent{1+pid-'A'};
end

qalign top center
qtext(xywh(1) + xywh(3)/2, xywh(2) + 5, ttl);
