function qp_updaterange(xx, yy);

global qp_data;
idx = qp_idx;
dr = qp_data.info(idx).datarange;
mx = min(xx);
Mx = max(xx);
my = min(yy);
My = max(yy);
if isnan(dr(1)) || mx<dr(1)
  dr(1) = mx;
end
if isnan(dr(2)) || Mx>dr(2)
  dr(2) = Mx;
end
if isnan(dr(3)) || my<dr(3)
  dr(3) = my;
end
if isnan(dr(4)) || My>dr(4)
  dr(4) = My;
end
qp_data.info(idx).datarange = dr;
