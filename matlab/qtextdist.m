function [lbl, ttl] = qtextdist(lbl, ttl)
% QTEXTDIST - Specifies distance to text labels for QXAXIS and QYAXIS
%    QTEXTDIST(lbldist, ttldist) specifies distance between ticks and
%    tick labels and between tick labels and axis title, in points.
%    QTEXTDIST(dist) uses DIST for both distances.
%    Positive numbers are to the left and down; negative numbers are to the
%    right and up.
%    [lbl, ttl] = QTEXTDIST returns current settings.

idx = qp_idx;
global qp_data;

if nargin==0

  lbl = qp_data.info(idx).textdist(1);
  ttl = qp_data.info(idx).textdist(2);

else

  if nargin==1
    ttl = lbl;
  end
  
  if ischar(lbl)
    lbl = str2double(lbl);
  end
  if ischar(ttl)
    ttl = str2double(ttl);
  end
  
  qp_data.info(idx).textdist = [lbl ttl];

  clear lbl ttl
  
end

