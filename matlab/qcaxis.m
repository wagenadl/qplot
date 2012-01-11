function qcaxis(clim, varargin)
% QCAXIS - Plot colorbar axis
%    QCAXIS([c0 c1], cc) plots a colorbar axis with ticks at represented
%    values CC with the bar stretching to C0 and C1. (CC may be empty.)
%    QCAXIS(cc) calculates C0 and C1 from CC.
%    QCAXIS(..., lbls) where LBLS is either a cell array or numeric vector
%    the same size as CC overrides the default tick labels. Labels are
%    suppressed if LBLS is empty.
%    QCAXIS(..., ttl) adds a title to the axis.
% 
%    QCAXIS obeys settings from QTICKLEN, QTEXTDIST, and QAXSHIFT,
%    and is precisely analogous to QXAXIS and QYAXIS, except that:
%    - The coordinates are derived from the colorbar.
%    - For vertical colorbars (the typical case), the axis is drawn on the
%      right (left) for positive or zero (negative) AXSHIFT, with ticks 
%      sticking out (in) for positive (negative) TICKLEN, and text outward
%      (inward) for positive (negative) TEXTDIST.
%    - For horizontal colorbars (the typical case), the axis is drawn on the
%      bottom (top) for positive or zero (negative) AXSHIFT, with ticks 
%      sticking out (in) for positive (negative) TICKLEN, and text outward
%      (inward) for positive (negative) TEXTDIST.
%
%    Note that currently QMTICKS doesn't understand about this convention,
%    so QMTICKS will produce unexpected results when used with QCAXIS.

if nargin<1
  qxa_usage;
end
if ~isnvector(clim)
  qxa_usage;
end

if length(clim)~=2
  cpts = clim;
  clim = [clim(1) clim(end)];
elseif ~isempty(varargin) && isnvector(varargin{1})
  cpts = varargin{1};
  varargin = varargin(2:end);
elseif ~isempty(varargin) && isnumeric(varargin{1}) && isempty(varargin{1})
  cpts = [];
  varargin = varargin(2:end);
else
  cpts = clim;
end

if length(clim)~=2
  qxa_usage;
end

lbls = qp_format(cpts);
if ~isempty(varargin)
  if isnumeric(varargin{1})
    lbls = qp_format(varargin{1});
    varargin = varargin(2:end);
  elseif iscell(varargin{1})
    lbls = varargin{1};
    varargin = varargin(2:end);
  end
end

ttl = '';
if ~isempty(varargin)
  if ischar(varargin{1})
    ttl = varargin{1};
    varargin = varargin(2:end);
  end
end

if isempty(lbls)
  ;
elseif length(lbls) ~= length(cpts)
  qxa_usage;
end


idx = qp_idx;
global qp_data;
ticklen = qp_data.info(idx).ticklen;
axshift = qp_data.info(idx).axshift;
if axshift==0
  axshift = 1e-9;
end
lbldist = qp_data.info(idx).textdist(1);
ttldist = qp_data.info(idx).textdist(2);
cb = qp_cbinfo;

if cb.hori
  qp_data.info(idx).ticklen = sign(axshift) * ticklen;
  qp_data.info(idx).textdist = sign(axshift) * [lbldist ttldist];
else  
  qp_data.info(idx).ticklen = -sign(axshift) * ticklen;
  qp_data.info(idx).axshift = -axshift;
  qp_data.info(idx).textdist = -sign(axshift) * [lbldist ttldist];
end

dlim = qca_ctodat(clim, cb);
dpts = qca_ctodat(cpts, cb);
  
if cb.hori
  if axshift>=0
    y0 = cb.xywh(2);
  else
    y0 = cb.xywh(2) + cb.xywh(4);
  end
  qxaxis(y0, dlim, dpts, lbls, ttl);
else
  if axshift>=0
    x0 = cb.xywh(1) + cb.xywh(3);
  else
    x0 = cb.xywh(1);
  end
  qyaxis(x0, dlim, dpts, lbls, ttl);
end

qp_data.info(idx).ticklen = ticklen;
qp_data.info(idx).textdist = [lbldist ttldist];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function qxa_usage() 
error('Usage: qcaxis [clim] cpts [lbls] [title]');

function dat = qca_ctodat(cc, cb)
crel = (cc-cb.c0)/(cb.c1-cb.c0);

if cb.hori
  rng = cb.xywh(3);
  d0 = cb.xywh(1);
else
  rng = cb.xywh(4);
  d0 = cb.xywh(2);
end
if cb.flip
  d0 = d0+rng;
  rng = -rng;
end

dat = d0 + rng*crel;
