function fd = qp_fd(varargin)

idx = qp_idx(varargin{:});
global qp_data

fd = qp_data.info(idx).fd;
if fd<0
  error('No open window');
end
