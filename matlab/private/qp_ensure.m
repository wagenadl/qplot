function fd = qp_ensure(x)

global qp_data

if isempty(qp_data)
  qp_data.curfn = '';
  
  qp_data.fn = {};
  qp_data.istemp = [];
  qp_data.fd = [];

  qp_data.ax.ticklen = 3;
  qp_data.ax.textdist = [3 3];
  qp_data.ax.last = '';
  qp_data.lut = repmat([0:.01:1]',[1 3]);
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
