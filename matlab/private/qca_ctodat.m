function dat = qca_ctodat(cc, cb)
% qca_ctodat: private function for qcaxis
crel = (cc-cb.clim(1))/(cb.clim(2)-cb.clim(1));

switch cb.orient
  case 'y'
    rng = cb.xywh_d(4);
    d0 = cb.xywh_d(2);
  case 'x'
    rng = cb.xywh_d(3);
    d0 = cb.xywh_d(1);
end
if cb.rev
  d0 = d0+rng;
  rng = -rng;
end

dat = d0 + rng*crel;
