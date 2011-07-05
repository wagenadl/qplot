function qmticks(xx)
% QMTICKS - Add more ticks to an existing axis

idx = qp_idx(1);
global qp_data

if isempty(qp_data.lastax{idx})
  error('No previous axis');
end

xx = xx(xx>=qp_data.lastlim{idx}(1) & xx<=qp_data.lastlim{idx}(2));
X = length(xx);

if strcmp(qp_data.lastax{idx}, 'x')
  for k=1:X
    qat(xx(k), qp_data.lastcoord{idx});
    qline([0 0], [0 qp_data.ticklen{idx}]);
  end
elseif strcmp(qp_data.lastax{idx}, 'y')
  for k=1:X
    qat(qp_data.lastcoord{idx}, xx(k));
    qline([0 -qp_data.ticklen{idx}], [0 0]);
  end
end
