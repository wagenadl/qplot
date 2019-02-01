function qoverline(xx, yy, txt)
% QOVERLINE - Draw a line above data with a text above it
%   QOVERLINE(xx, y, text), where XX is a 2-vector and Y a scalar, draws
%   a horizontal line just above (XX(1), Y) to (XX(2), Y) and places the
%   given TEXT over it.
%   QOVERLINE(xx, yy, text), where both XX and YY are 2-vectors, draws the
%   line just above the larger YY value and extends a vertical line down 
%   to the smaller YY value.
%   The whole thing is displaced by a distance QOVERLINEDIST from the data,
%   and the text placement uses the absolute value of QTEXTDIST.
%   If QOVERLINEMIN is non-zero, a vertical line is drawn on both ends.
%   QOVERLINE(xx, y) or QOVERLINE(xx, yy) is permitted: no text is drawn.

s = qoverlinedist;
h = qoverlinemin;

ymax = max(yy);

if length(yy)==2 
  qshiftedline(xx(1)+[0 0], [yy(1) ymax], 0, s + [0 sign(s)*h]);
  qshiftedline(xx(2)+[0 0], [yy(2) ymax], 0, s + [0 sign(s)*h]);  
elseif h>0
  qshiftedline(xx(1)+[0 0], [ymax ymax], 0, s + [0 sign(s)*h]);
  qshiftedline(xx(2)+[0 0], [ymax ymax], 0, s + [0 sign(s)*h]);  
end
qshiftedline(xx, [ymax ymax], 0, (s + sign(s)*h) + [0 0]);

if nargin>=3 && ~isempty(txt)
  qat(mean(xx), ymax);
  td = abs(qtextdist);
  if s>0
    qalign center top
  else
    qalign center bottom
  end
  qtext(0, s + sign(s)*[h + td], txt);
end