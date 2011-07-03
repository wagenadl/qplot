function qtextdist(lbl, ttl)

qp_ensure;
global qp_data;

if nargin==1
  ttl = lbl;
end

qp_data.ax.textdist = [lbl ttl];

