function pap = qca_ctopap(cc, cb)
% qca_ctopap: private function for qcaxis
crel = (cc-cb.clim(1))/(cb.clim(2)-cb.clim(1));

switch cb.orient
  case 'y'
    rng = cb.xywh_p(4);
    d0 = cb.xywh_p(2);
  case 'x'
    rng = cb.xywh_p(3);
    d0 = cb.xywh_p(1);
end
if ~cb.rev
  d0 = d0+rng;
  rng = -rng;
end

pap = d0 + rng*crel;
