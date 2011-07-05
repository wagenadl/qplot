function qtextdist(lbl, ttl)

qp_ensure;
global qp_data;

if nargin==1
  ttl = lbl;
end

if ischar(lbl)
  lbl = str2double(lbl);
end
if ischar(ttl)
  ttl = str2double(ttl);
end

qp_data.ax.textdist = [lbl ttl];

