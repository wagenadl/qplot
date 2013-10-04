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

% Note that we use variable names from qxaxis, which may be confusing.

err = 'Usage: qyaxis X0 [ylim] ypts [lbls] [title]';

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
