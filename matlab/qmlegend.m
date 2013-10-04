function qmlegend(str)
% QMLEGEND - Render legend element for marks
%    QMLEGEND(str) renders a sample of the most recently rendered 
%    mark at the location set by QLEGOPT and writes the given string
%    next to it.
%    QMLEGEND without a string renders the most recently used mark
%    over a previously rendered (line) legend.
%    See also QLEGEND and QPLEGEND.

qlegopt; % ensure that we have options
global qp_data;
idx = qp_idx(1);
opt = qp_data.info(idx).legopt;

qat(opt.x0, opt.y0);

if nargin==0
  qpmark(.5*opt.width+opt.dx, (opt.n-1)*opt.skip+opt.dy);
else
  qpmark(.5*opt.width+opt.dx, opt.n*opt.skip+opt.dy);
  qgroup
  qpen(opt.color);
  qalign left base
  qtext(opt.width+opt.indent+opt.dx, opt.n*opt.skip + opt.drop+opt.dy, str);
  qendgroup
  
  qp_data.info(idx).legopt.n = opt.n + 1;
end
