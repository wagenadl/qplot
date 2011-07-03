function qselect(fn)
global qp_data;
qp_ensure;

idx = strmatch(fn, qp_data.fn, 'exact');

if isempty(idx)
  error('No such figure');
end

qp_data.curfn = fn;
unix(sprintf('touch %s', fn));
