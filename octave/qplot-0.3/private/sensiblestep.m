function dx=sensiblestep(mx)
% dx = SENSIBLESTEP(mx) returns a sensible step size not much smaller
% than MX:
%
%   1<=MX<2  -> DX=1
%   2<=MX<5  -> DX=2
%   5<=MX<10 -> DX=5
%   etc.
%
% To get a dense inclusive tick bar, use as in:
%
%   dx = sensiblestep((maxx-minx)/5);
%   minx = floor(minx/dx)*dx;
%   maxx = ceil(maxx/dx)*dx;
%   set(gca,'xtick',[minx:dx:maxx]);
%
% Or, to get a smaller tick bar:
%
%   dx = sensiblestep((maxx-minx)/2);
%   minx = ceil(minx/dx)*dx;
%   maxx = floor(maxx/dx)*dx;
%   xtickbar([minx:dx:maxx],0,-.05,[],'');

lg=log10(mx);
ord=floor(lg);
sub=10.^(lg-ord);
if sub>5
  sub=5;
elseif sub>2
  sub=2;
else
  sub=1;
end
dx = sub * 10^ord;
