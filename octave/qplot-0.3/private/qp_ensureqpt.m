function fn = qp_ensureqpt(fn)
% QP_ENSUREQPT - Ensure that filename ends in .qpt

dotidx = find(fn=='.');
slashidx = find(fn=='/');
if ~isempty(slashidx)
  dotidx = dotidx(dotidx>slashidx(end));
end
if isempty(dotidx)
  fn = [ fn '.qpt' ];
end
