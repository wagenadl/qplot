function qcaxis(varargin)
% QCAXIS - Plot colorbar axis
%    QCAXIS([c0 c1], cc) plots a colorbar axis with ticks at represented
%    values CC with the bar stretching to C0 and C1. (CC may be empty.)
%    QCAXIS(cc) calculates C0 and C1 from CC.
%    QCAXIS(..., lbls) where LBLS is either a cell array or numeric vector
%    the same size as CC overrides the default tick labels. Labels are
%    suppressed if LBLS is empty.
%    QCAXIS(..., ttl) adds a title to the axis.
%    QCAXIS normally places the axis to the right or below the color bar, but
%    if the color bar was created with negative width, the axis goes to the
%    left or above instead.
%    QCAXIS(dir, ...), where DIR is one of 'l', 't', 'b', or 'r', overrides
%    the default location.
% 
%    QCAXIS interprets settings from QTICKLEN, QTEXTDIST, and QAXSHIFT
%    differently from QXAXIS and QYAXIS: positive values are away from the
%    colorbar.
%    Note that currently QMTICKS doesn't understand about this convention,
%    so QMTICKS will produce unexpected results when used with QCAXIS.

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

idx = qp_idx;
global qp_data;
if ~isfield(qp_data.info(idx), 'cbar')
  error('QCAXIS needs a previous QCBAR');
end
cb = qp_data.info(idx).cbar;

if nargin<=1
  if nargin==1
    ttl = varargin{1};
  else
    ttl = '';
  end
  % Automatic everything
  clim = cb.clim;
  tkx = sensibleticks(clim);
  clim_t = sprintf('[%g %g]', clim);
  tkx_t = '';
    for i=1:length(tkx)
      tkx_t = [tkx_t sprintf(' %g', tkx(i))];
    end
    tkx_t = [ tkx_t ']' ];
  tkx_t(1) = '[';
  fprintf(1, 'qcaxis(%s, %s, ''%s'');\n', clim_t, tkx_t, ttl);
  qcaxis(clim, tkx, ttl);
  return
end

side = sign(cb.xywh_p(3)+cb.xywh_p(4));

if ~isempty(varargin)
  if ischar(varargin{1})
    switch varargin{1};
      case 'l'
	side = -1;
      case 't'
	side = -1;
      case 'b'
	side = 1;
      case 'r'
	side = -1;
      otherwise
	error('Side must be l/t/b/r');
    end
    varargin = varargin(2:end);
  end
end

err = 'Usage: qcaxis [side] [clim] cpts [lbls] [title]';
[clim, cpts, lbls, ttl] = qp_axargs(err, varargin{:});

ticklen = qp_data.info(idx).ticklen;
axshift = qp_data.info(idx).axshift;
lbldist = qp_data.info(idx).textdist(1);
ttldist = qp_data.info(idx).textdist(2);

dlim = qca_ctodat(clim, cb);
dpts = qca_ctodat(cpts, cb);
plim = qca_ctopap(clim, cb);
ppts = qca_ctopap(cpts, cb);

plim(isnan(plim))=0;
ppts(isnan(ppts))=0;

switch cb.orient
  case 'y'
    lblrot = qytitlerot;
    dcoord = cb.xywh_d(1);
    pcoord = cb.xywh_p(1);
    if side>0
      dcoord = dcoord+cb.xywh_d(3);
      if cb.xywh_p(3)>0
	pcoord = pcoord+cb.xywh_p(3);
      end
    else
      if cb.xywh_p(3)<0
	pcoord = pcoord+cb.xywh_p(3);
      end
    end
  case 'x'
    lblrot = 0;
    dcoord = cb.xywh_d(2);
    pcoord = cb.xywh_p(2);
    if side<0
      dcoord = dcoord+cb.xywh_d(4);
      if cb.xywh_p(4)<0
	pcoord = pcoord+cb.xywh_p(4);
      end
    else
      if cb.xywh_p(4)>0
	pcoord = pcoord+cb.xywh_p(4);
      end
    end
end
ticklen = ticklen*side;
lbldist = lbldist*side;
ttldist = ttldist*side;
axshift = axshift*side;

qp_axis('orient', cb.orient, ...
    'lim_d', dlim, 'lim_p', plim, ...
    'tick_d', dpts, 'tick_p', ppts, ...
    'coord_d', dcoord, 'coord_p', pcoord+axshift, ...
    'tick_lbl', lbls, 'ttl', ttl, ...
    'ticklen', ticklen, 'lbldist', lbldist, 'ttldist', ttldist, ...
    'ttlrot', lblrot, 'cbar', cb);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function dat = qca_ctodat(cc, cb)
crel = (cc-cb.clim(1))/(cb.clim(2)-cb.clim(1));

switch cb.orient
  case 'y'
    rng = cb.xywh_d(4);
    d0 = cb.xywh_d(2);
  case 'x'
    rng = cb.xywh_d(3);
    d0 = cb.xywh_d(1);
end
if cb.rev
  d0 = d0+rng;
  rng = -rng;
end

dat = d0 + rng*crel;

function pap = qca_ctopap(cc, cb)
crel = (cc-cb.clim(1))/(cb.clim(2)-cb.clim(1));

switch cb.orient
  case 'y'
    rng = cb.xywh_p(4);
    d0 = cb.xywh_p(2);
  case 'x'
    rng = cb.xywh_p(3);
    d0 = cb.xywh_p(1);
end
if ~cb.rev
  d0 = d0+rng;
  rng = -rng;
end

pap = d0 + rng*crel;
