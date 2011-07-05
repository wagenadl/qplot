function qmticks(xx)
% QMTICKS - Add more ticks to an existing axis

qp_ensure(1);
global qp_data

if isempty(qp_data.ax.last)
  error('No previous axis');
end

xx = xx(xx>=qp_data.ax.lastlim(1) & xx<=qp_data.ax.lastlim(2));
X = length(xx);

if strcmp(qp_data.ax.last, 'x')
  for k=1:X
    qat(xx(k), qp_data.ax.lastcoord);
    qline([0 0], [0 qp_data.ax.ticklen]);
  end
elseif strcmp(qp_data.ax.last, 'y')
  for k=1:X
    qat(qp_data.ax.lastcoord, xx(k));
    qline([0 -qp_data.ax.ticklen], [0 0]);
  end
end
