function pt = qticklen(pt)
% QTICKLEN - Specifies length of ticks for QXAXIS and QYAXIS
%    QTICKLEN(len) specifies length of ticks (in points) for QXAXIS and
%    QYAXIS. Positive means down or left, negative means up or right.
%    pt = QTICKLEN returns current setting.

idx = qp_idx;
global qp_data;

if nargin==0
  
  pt = qp_data.info(idx).ticklen;

else
  
  if ischar(pt)
    pt = str2double(pt);
  end
  
  if ~isnscalar(pt) | ~isreal(pt) | isnan(pt) |  isinf(pt)
    error('ticklen must be a real scalar');
  end
  
  qp_data.info(idx).ticklen = pt;
  
  clear pt

end