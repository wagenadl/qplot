function qsave(ofn, reso)
% QSAVE - Saves a qplot figure
%    QSAVE(ofn) saves the current qplot figure to the named file.
%    QSAVE(ext), where EXT is just a filename extension (without the dot),
%    uses the name of the current figure.
%    QSAVE(ofn, reso) specifies bitmap resolution for png/jpeg output.
%    QSAVE without arguments saves to pdf.

if nargin<2
  reso = [];
end

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

if ischar(reso)
  reso = atoi(reso);
end

if isempty(reso)
  cmd = sprintf('qplotml %s %s', ifn, ofn);
else
  cmd = sprintf('qplotml -r%i %s %s', floor(reso), ifn, ofn);
end

s = unix(cmd);
if s
  error('qplot failed');
end


