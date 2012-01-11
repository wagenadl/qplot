function qp_ensure

global qp_data

if isempty(qp_data)
  qp_data.curfn = '';
  qp_data.fns = {};
  qp_data.info = [];
  
  qp_data.ismatlab = length(ver('Matlab'));
  qp_data.isoctave = length(ver('Octave'));
end
