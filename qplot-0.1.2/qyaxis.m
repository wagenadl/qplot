function qyaxis(y0, varargin)
% QYAXIS - Plot y-axis
%    QYAXIS(x0, [y0 y1], yy) plots an y-axis with ticks at YY. (YY may be
%    empty.)
%    QYAXIS(x0, yy) calculates Y0 and Y1 from YY.
%    QYAXIS(x0, [], yy) only draws ticks, not an axis line.
%    QYAXIS(..., lbls) where LBLS is either a cell array or numeric vector
%    the same size as YY overrides the default tick labels. Labels are
%    suppressed if LBLS is empty.
%    QYAXIS(..., ttl) adds a title to the axis.
% 
%    QYAXIS obeys settings from QTICKLEN, QTEXTDIST, and QAXSHIFT.
%    QYAXIS('r', ...) inverts the sign of these settings.
%    QYAXIS('R', ...) additionally orients the title the other way.
%
%    Either LBLS or YY (but not both) may be a function handle in which case
%    the labels are calculated from the tick positions (or vice versa). For
%    example:
%      QYAXIS(0, [0:0.2:1], @(y) (y*100), 'Value (%)')

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

% Note that we use variable names from qxaxis, which may be confusing.

err = 'Usage: qyaxis X0 [ylim] ypts [lbls] [title]';

if nargin<2
  % All automatic
  if nargin==1
    ttl = y0;
  else
    ttl = '';
  end
  global qp_data;
  idx = qp_idx;
  dr = qp_data.info(idx).datarange;
  if any(isnan(dr))
    error('QYAXIS needs previous plot for automatic operation');
  end
  yy = sensibleticks(dr(3:4), 1);
  xx = sensibleticks(dr(1:2), 1);
  tk_t = '';
  for k=1:length(yy)
    tk_t = [ tk_t sprintf(' %g', yy(k))];
  end
  fprintf(1,'qyaxis(%g, [%s], ''%s'');\n', xx(1), tk_t(2:end), ttl);
  qyaxis(xx(1), yy, ttl);
  return;
end

if ischar(y0)
  if strcmp(y0, 'r') || strcmp(y0, 'R')
    flip = 1;
    if y0=='R'
      rot = 1;
    else
      rot = 0;
    end
    y0 = varargin{1};
    varargin = varargin(2:end);
  else
    error(err);
  end
else
  flip = 0;
end

[xlim, xpts, lbls, ttl] = qp_axargs(err, varargin{:});

ticklen = qticklen;
axshift = qaxshift;
[lbldist, ttldist] = qtextdist;
lblrot = qytitlerot;

if flip
  ticklen = -ticklen;
  axshift = -axshift;
  lbldist = -lbldist;
  ttldist = -ttldist;
  if rot
    lblrot = -lblrot;
  end
end

qp_axis('orient', 'y', 'lim_d', xlim, 'tick_d', xpts, 'tick_lbl', lbls, ...
    'ttl', ttl, ...
    'ticklen', -ticklen, 'lbldist', -lbldist, 'ttldist', -ttldist, ...
    'coord_d', y0, 'coord_p', -axshift, 'ttlrot', lblrot);
