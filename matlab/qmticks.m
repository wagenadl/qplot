function qmticks(xx)
% QMTICKS - Add more ticks to an existing axis

idx = qp_idx(1);
global qp_data

if isempty(qp_data.info(idx).lastax)
  error('No previous axis');
end

xx = xx(xx>=qp_data.info(idx).lastlim(1) & xx<=qp_data.info(idx).lastlim(2));
X = length(xx);

if strcmp(qp_data.info(idx).lastax, 'x')
  for k=1:X
    qat(xx(k), qp_data.info(idx).lastcoord);
    qline([0 0], [0 qp_data.info(idx).ticklen]);
  end
elseif strcmp(qp_data.info(idx).lastax, 'y')
  for k=1:X
    qat(qp_data.info(idx).lastcoord, xx(k));
    qline([0 -qp_data.info(idx).ticklen], [0 0]);
  end
end
