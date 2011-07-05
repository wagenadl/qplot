function qticklen(pt)

qp_ensure;
global qp_data;
if ischar(pt)
  pt = str2double(pt);
end
if isnscalar(pt) & isreal(pt) & pt>0 & ~isinf(pt)
  qp_data.ax.ticklen = pt;
else
  error('ticklen must be positive and finite');
end

