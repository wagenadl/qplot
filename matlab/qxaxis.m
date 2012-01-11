function qxaxis(y0, xlim, varargin)
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


if nargin<2
  qxa_usage;
end
if ~isnscalar(y0)
  qxa_usage;
end
if isempty(xlim)
  xlim=[nan nan];
end
if ~isnvector(xlim)
  qxa_usage;
end

if length(xlim)~=2
  xpts = xlim;
  xlim = [xlim(1) xlim(end)];
elseif ~isempty(varargin) && isnvector(varargin{1})
  xpts = varargin{1};
  varargin = varargin(2:end);
elseif ~isempty(varargin) && isnumeric(varargin{1}) && isempty(varargin{1})
  xpts = [];
  varargin = varargin(2:end);
else
  xpts = xlim;
end

if length(xlim)~=2
  qxa_usage;
end

lbls = qp_format(xpts);
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
elseif length(lbls) ~= length(xpts)
  qxa_usage;
end

% -- Plotting starts here

ticklen = qticklen;
axshift = qaxshift;
[lbldist, ttldist] = qtextdist;

qgroup;
if any(isnan(xlim))
  xlim(1) = min(xpts);
  xlim(2) = max(xpts);
else
  qgline({'absdata',xlim(1),y0,'relpaper',0,axshift},...
      {'absdata',xlim(2),y0,'relpaper',0,axshift});
end

if ~isempty(lbls)
  reftxt='';
  for k=1:length(lbls)
    reftxt = [ reftxt lbls{k} ];
  end
  qreftext(reftxt);
end

if lbldist>=0
  valign = 'top';
  if ticklen>0
    lbldist = lbldist + ticklen;
  end
else
  valign = 'bottom';
  if ticklen<0
    lbldist = lbldist + ticklen;
  end
end
qalign(valign, 'center');

qgroup;
for k=1:length(xpts)
  qat(xpts(k), y0);
  qline([0 0], [0 ticklen]+axshift);
  if ~isempty(lbls)
    qtext(0, lbldist+axshift, lbls{k});
  end
end
qendgroup;
qreftext('');

if ~isempty(ttl) 
  if sign(ttldist)==sign(lbldist)
    if ttldist>=0
      qat(mean(xlim), 'bottom');
    else
      qat(mean(xlim), 'top');
    end
  else
    if sign(ttldist)==sign(ticklen)
      ttldist = ttldist + ticklen;
    end
    qat(mean(xlim), y0);
  end
  if ttldist>0
    valign='top';
  else
    valign='bottom';
  end
  qalign(valign, 'center');
  
  qtext(0, ttldist+axshift, ttl);
end

idx = qp_idx;
global qp_data;
qp_data.info(idx).lastax='x';
qp_data.info(idx).lastcoord=y0;
qp_data.info(idx).lastlim=xlim;
qendgroup

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function qxa_usage() 
error('Usage: qxaxis Y0 [xlim] xpts [lbls] [title]');