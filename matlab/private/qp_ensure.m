function qp_ensure

global qp_data

if isempty(qp_data)
  qp_data.curfn = '';
  qp_data.fns = {};
  qp_data.info = [];
end
