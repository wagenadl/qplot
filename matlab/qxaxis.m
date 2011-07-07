function qxaxis(y0, xlim, varargin)
% QXAXIS - Plot x-xaxis
%    QXAXIS(y0, [x0 x1], xx) plots an x-axis with ticks at XX. (XX may be
%    empty.)
%    QXAXIS(y0, xx) calculates X0 and X1 from XX.
%    QXAXIS(..., lbls) where LBLS is either a cell array or numeric vector
%    the same size as XX overrides the default tick labels. Labels are
%    suppressed if LBLS is empty.
%    QXAXIS(..., ttl) adds a title to the axis.
% 
%    QXASIS obeys settings from QTICKLEN and QLABELDIST


if nargin<2
  qxa_usage;
end
if ~isnscalar(y0)
  qxa_usage;
end
if ~isnvector(xlim)
  qxa_usage;
end

if length(xlim)~=2
  xpts = xlim;
  xlim = [xlim(1) xlim(end)];
elseif ~isempty(varargin) & isnvector(varargin{1})
  xpts = varargin{1};
  varargin = varargin(2:end);
elseif ~isempty(varargin) & isnumeric(varargin{1}) & isempty(varargin{1})
  xpts = [];
  varargin = varargin(2:end);
else
  xpts = xlim;
end

if length(xlim)~=2
  qxa_usage;
end

lbls = num2strcell(xpts);
if ~isempty(varargin)
  if isnumeric(varargin{1})
    lbls = num2strcell(varargin{1});
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
elseif size(lbls) ~= size(xpts)
  qaxis_usage;
end

% -- Plotting starts here

qgroup;
qplot(xlim, [y0 y0]);

idx = qp_idx;
global qp_data;
ticklen = qp_data.info(idx).ticklen;
lbldist = qp_data.info(idx).textdist(1);
ttldist = qp_data.info(idx).textdist(2);

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
  qline([0 0], [0 ticklen]);
  if ~isempty(lbls)
    qtext(0, lbldist, lbls{k});
  end
end
qendgroup;
qreftext('');

if ~isempty(ttl) 
  if ttldist>=0
    qat(mean(xlim), 'bottom');
  else
    qat(mean(xlim), 'top');
  end
  qtext(0, ttldist, ttl);
end

qp_data.info(idx).lastax='x';
qp_data.info(idx).lastcoord=y0;
qp_data.info(idx).lastlim=xlim;
qendgroup

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function qxa_usage() 
error('Usage: qxaxis Y0 [xlim] xpts [lbls] [title]');