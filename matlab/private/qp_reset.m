function qp_reset(idx)

global qp_data

qp_data.info(idx).ticklen = 3;
qp_data.info(idx).axshift = 0;
qp_data.info(idx).ytitlerot = pi/2;
qp_data.info(idx).textdist = [3 3];
qp_data.info(idx).lastax = '';
qp_data.info(idx).lut = repmat([0:.01:1]',[1 3]);
qp_data.info(idx).lut_nan = [1 1 1];
qp_data.info(idx).panels = {'-'};
qp_data.info(idx).panelextent = { };
qp_data.info(idx).panel = '-';
qp_data.info(idx).numfmt = '';
