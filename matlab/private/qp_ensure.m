function qp_ensure

global qp_data

if isempty(qp_data)
  qp_data.curfn = '';
  
  qp_data.fn = {};
  qp_data.istemp = [];
  qp_data.fd = [];

  qp_data.extent = {};
  qp_data.ticklen = {};
  qp_data.textdist = {};
  qp_data.lastax = {};
  
  qp_data.lut = {};
end
