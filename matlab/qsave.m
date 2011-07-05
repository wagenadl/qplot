function qsave(ofn)
qp_ensure;
global qp_data;
ifn = qp_data.curfn;
if isempty(ifn)
  error('No window');
end
s = unix(sprintf('qplot %s %s', ifn, ofn));
if s
  error('qplot failed');
end


