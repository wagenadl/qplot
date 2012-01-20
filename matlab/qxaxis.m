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

err = 'Usage: qxaxis Y0 [xlim] xpts [lbls] [title]';
[xlim, xpts, lbls, ttl] = qp_axargs(err, varargin{:});

ticklen = qticklen;
axshift = qaxshift;
[lbldist, ttldist] = qtextdist;

qp_axis('orient', 'x', 'lim_d', xlim, 'tick_d', xpts, 'tick_lbl', lbls, ...
    'ttl', ttl, ...
    'ticklen', ticklen, 'lbldist', lbldist, 'ttldist', ttldist, ...
    'coord_d', y0, 'coord_p', axshift);
