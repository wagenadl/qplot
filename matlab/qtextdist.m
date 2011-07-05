function qtextdist(lbl, ttl)

if nargin==1
  ttl = lbl;
end

if ischar(lbl)
  lbl = str2double(lbl);
end
if ischar(ttl)
  ttl = str2double(ttl);
end

idx = qp_idx;
global qp_data;
qp_data.textdist{idx} = [lbl ttl];

