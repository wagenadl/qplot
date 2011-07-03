function qsave(ofn)
qp_ensure(0);
global qp_data;
ifn = qp_data.curfn;
s = unix(sprintf('qplot %s %s', ifn, ofn));
if s
  error('qplot failed');
end


