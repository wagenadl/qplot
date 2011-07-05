function qticklen(pt)

if ischar(pt)
  pt = str2double(pt);
end

if ~isnscalar(pt) | ~isreal(pt) | isnan(pt) |  ~isinf(pt)
  error('ticklen must be a real scalar');
end

idx = qp_idx;
global qp_data;
qp_data.ticklen{idx} = pt;


