function qprint
% QPRINT - Print current QPLOT figure to the default printer
qp_ensure;
global qp_data;
ifn = qp_data.curfn;
if isempty(ifn)
  error('No window');
end
qselect(ifn);

ofn = sprintf('%s.ps', tempname);

s = unix(sprintf('qplotml %s %s', ifn, ofn));
if s
  error('qplot failed');
end

input('Press Enter to print to lpr, or Ctrl-C to cancel...');
unix(sprintf('lpr %s', ofn));
fprintf(1,'\nPostscript file sent to printer.\n');

delete(ofn);
