function qsave(ofn)
% QSAVE - Saves a qplot figure
%    QSAVE(ofn) saves the current qplot figure to the named file.
%    QSAVE(ext), where EXT is just a filename extension (without the dot),
%    uses the name of the current figure.
%    QSAVE without arguments saves to pdf

qp_ensure;
global qp_data;
ifn = qp_data.curfn;
if isempty(ifn)
  error('No window');
end

if nargin<1
  ofn='pdf';
end

if isempty(find(ofn=='.'))
  % Extension only
  idx = find(ifn=='.');
  ofn = [ifn(1:idx(end)) ofn];
end

s = unix(sprintf('qplotml %s %s', ifn, ofn));
if s
  error('qplot failed');
end


