function qplegend(str)
% QPLEGEND - Render legend element for patch
%    QPLEGEND(str) renders a sample of the most recently rendered 
%    patch at the location set by QLEGOPT and writes the given string
%    next to it.
%    See also QLEGEND and QMLEGEND.

qlegopt; % ensure that we have options
global qp_data;
idx = qp_idx(1);
opt = qp_data.info(idx).legopt;

qat(opt.x0, opt.y0);
qarea([0 1 1 0]*opt.width+opt.dx, opt.n*opt.skip + [-.5 -.5 .5 .5]*opt.height+opt.dy);
qgroup
qpen(opt.color);
qalign left base
qtext(opt.width+opt.indent+opt.dx, opt.n*opt.skip + opt.drop+opt.dy, str);
qendgroup

qp_data.info(idx).legopt.n = opt.n + 1;
