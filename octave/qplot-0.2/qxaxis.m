function qxaxis(y0, varargin)
% QXAXIS - Plot x-axis
%    QXAXIS(y0, [x0 x1], xx) plots an x-axis with ticks at XX. (XX may be
%    empty.)
%    QXAXIS(y0, xx) calculates X0 and X1 from XX.
%    QXAXIS(y0, [], xx) only draws ticks, not an axis line.
%    QXAXIS(..., lbls) where LBLS is either a cell array or numeric vector
%    the same size as XX overrides the default tick labels. Labels are
%    suppressed if LBLS is empty.
%    QXAXIS(..., ttl) adds a title to the axis.
% 
%    QXAXIS obeys settings from QTICKLEN, QTEXTDIST, and QAXSHIFT.
%    QXAXIS('t', ...) inverts the sign of these settings.
%
%    Either LBLS or XX (but not both) may be a function handle in which case
%    the labels are calculated from the tick positions (or vice versa). For
%    example:
%      QXAXIS(0, @(x) (x/100), [0:25:100], 'Value (%)')
%
%    Without any arguments or with just a title as an argument, QXAXIS tries
%    to determine sensible defaults based on previous calls to QPLOT. Your
%    mileage may vary.


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

err = 'Usage: qxaxis Y0 [xlim] xpts [lbls] [title]';

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
    error('QXAXIS needs previous plot for automatic operation');
  end
  yy = sensibleticks(dr(3:4), 1);
  xx = sensibleticks(dr(1:2), 1);
  tk_t = '';
  for k=1:length(xx)
    tk_t = [ tk_t sprintf(' %g', xx(k))];
  end
  fprintf(1,'qxaxis(%g, [%s], ''%s'');\n', yy(1), tk_t(2:end), ttl);
  qxaxis(yy(1), xx, ttl);
  return;
end

if ischar(y0)
  if strcmp(y0, 't')
    flip = 1;
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

if flip
  ticklen = -ticklen;
  axshift = -axshift;
  lbldist = -lbldist;
  ttldist = -ttldist;
end

qp_axis('orient', 'x', 'lim_d', xlim, 'tick_d', xpts, 'tick_lbl', lbls, ...
    'ttl', ttl, ...
    'ticklen', ticklen, 'lbldist', lbldist, 'ttldist', ttldist, ...
    'coord_d', y0, 'coord_p', axshift);
