function fd = qp_ensure(x)

global qp_data

if ~isfield(qp_data, 'curfn')
  qp_data.curfn = '';
end
if ~isfield(qp_data, 'fn')
  qp_data.fn = {};
  qp_data.istemp = [];
  qp_data.fd = [];
end

if nargin>0
  if isempty(qp_data.curfn)
    if x>0
      qfigure;
    else
      error('No open window');
    end
  end
  idx = strmatch(qp_data.curfn, qp_data.fn, 'exact');
  if isempty(idx)
    error('No open window');
  end
  fd = qp_data.fd(idx);
  if fd<0
    error('No open window');
  end
end
