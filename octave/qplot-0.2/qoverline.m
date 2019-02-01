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

% QPlot - Publication quality 2D graphs with dual coordinate systems
% Copyright (C) 2014  Daniel Wagenaar
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

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