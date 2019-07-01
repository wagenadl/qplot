function qxcaxis(y0, varargin)
% QXCAXIS - Plot x-axis with labels between ticks
%   QXCAXIS(y0, xx, xl) places labels XL at locations XX, but places
%   ticks between labels rather than at the labels. First and last ticks
%   are extrapolated.
%   QXCAXIS(y0, [x0 x1], xx, xl) specifies those end ticks explicitly.
%   QXCAXIS(..., ttl) adds a title to the axis.
%   QXCAXIS obeys settings from QTICKLEN, QTEXTDIST, and QAXSHIFT.
%   QXCAXIS('t', ...) inverts the sign of these settings.

% QPlot - Publication quality 2D graphs with dual coordinate systems
% Copyright (C) 2014-2016  Daniel Wagenaar
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

err = 'Usage: qxcaxis Y0 [xlim] xpts lbls [title]';

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

if xlim(1)==xpts(1)
  % Automatic xlims: must override
  inbtwn = (xpts(1:end-1) + xpts(2:end))/2;
  xl0 = inbtwn(1)-(xpts(2)-xpts(1));
  xl1 = inbtwn(end)+(xpts(end)-xpts(end-1));
  xlim = [xl0 xl1];
  inbtwn = [xl0; inbtwn(:); xl1];
end

% First, place labels
qp_axis('orient', 'x', 'lim_d', [], 'tick_d', xpts, 'tick_lbl', lbls, ...
    'ttl', ttl, ...
    'ticklen', 0, 'lbldist', lbldist+ticklen, 'ttldist', ttldist, ...
    'coord_d', y0, 'coord_p', axshift);

% Then, place ticks
qp_axis('orient', 'x', 'lim_d', xlim, 'tick_d', inbtwn, 'tick_lbl', {}, ...
    'ticklen', ticklen, 'coord_d', y0, 'coord_p', axshift);