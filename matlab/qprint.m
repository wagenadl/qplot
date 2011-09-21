function qprint(nowait)
% QPRINT - Print current QPLOT figure to the default printer
%    QPRINT prints the current QPLOT figure using qplotml and lpr after
%    waiting for confirmation from the user.
%    QPRINT(1) does not wait.

if nargin<1
  nowait=0;
end

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

if ~nowait
  input('Press Enter to print to lpr, or Ctrl-C to cancel...');
end
unix(sprintf('lpr %s', ofn));
fprintf(1,'\nPostscript file sent to printer.\n');

delete(ofn);
