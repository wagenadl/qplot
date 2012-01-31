function qlegend(str)
% QLEGEND - Render legend element for plotted line
%    QLEGEND(str) renders a sample of the most recently plotted line
%    at the location set by QLEGOPT and writes the given string
%    next to it.

qlegopt; % ensure that we have options
global qp_data;
idx = qp_idx(1);
opt = qp_data.info(idx).legopt;

qat(opt.x0, opt.y0);
qline([0 1]*opt.width+opt.dx, opt.n*opt.skip + [0 0]+opt.dy);
qgroup
qpen(opt.color);
qalign left base
qtext(opt.width+opt.indent+opt.dx, opt.n*opt.skip + opt.drop+opt.dy, str);
qendgroup

qp_data.info(idx).legopt.n = opt.n + 1;
