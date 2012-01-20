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

% Note that we use variable names from qxaxis, which may be confusing.

err = 'Usage: qyaxis X0 [ylim] ypts [lbls] [title]';
[xlim, xpts, lbls, ttl] = qp_axargs(err, varargin{:});

ticklen = qticklen;
axshift = qaxshift;
[lbldist, ttldist] = qtextdist;
lblrot = qylabelrot;

qp_axis('orient', 'y', 'lim_d', xlim, 'tick_d', xpts, 'tick_lbl', lbls, ...
    'ttl', ttl, ...
    'ticklen', -ticklen, 'lbldist', -lbldist, 'ttldist', -ttldist, ...
    'coord_d', y0, 'coord_p', -axshift, 'ttlrot', lblrot);
