function qmticks(xx)
% QMTICKS - Add more ticks to an existing axis

idx = qp_idx(1);
global qp_data

if isempty(qp_data.info(idx).lastax)
  error('No previous axis');
end

kv = qp_data.info(idx).lastax;
kv.lim_d=[];
kv.lim_p=[];
kv.tick_d = xx;
kv.tick_p = [];
kv.tick_lbl = {};
kv.ttl = [];
kv.ticklen = qticklen;
if strcmp(kv.orient,'y')
  kv.ticklen = -kv.ticklen;
end
qp_axis(kv);
