function idx = qp_idx(autofig)

qp_ensure;
global qp_data

if nargin==0
  autofig=0;
end

if isempty(qp_data.curfn)
  if autofig>0
    qfigure;
  else
    error('No open window');
  end
end

idx = strmatch(qp_data.curfn, qp_data.fns, 'exact');
if isempty(idx)
  error('No open window');
end
