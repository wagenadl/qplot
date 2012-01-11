function qyaxis(y0, xlim, varargin)
% QYAXIS - Plot y-axis
%    QYAXIS(x0, [y0 y1], yy) plots an y-axis with ticks at YY. (YY may be
%    empty.)
%    QYAXIS(x0, yy) calculates Y0 and Y1 from YY.
%    QYAXIS(..., lbls) where LBLS is either a cell array or numeric vector
%    the same size as YY overrides the default tick labels. Labels are
%    suppressed if LBLS is empty.
%    QYAXIS(..., ttl) adds a title to the axis.
% 
%    QYAXIS obeys settings from QTICKLEN and QTEXTDIST.

% Note that we use variable names from qxaxis, which may be confusing.

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
elseif length(lbls) ~= length(xpts)
  qxa_usage;
end

%-- Plotting starts here

qgroup;
qreftext('');
qplot([y0 y0], xlim);

ticklen = qticklen;
[lbldist, ttldist] = qtextdist;

if lbldist>=0
  valign = 'right';
  if ticklen>0
    lbldist = lbldist + ticklen;
  end
else
  valign = 'left';
  if ticklen<0
    lbldist = lbldist + ticklen;
  end
end
qalign(valign, 'middle');

qgroup;
for k=1:length(xpts)
  qat(y0, xpts(k));
  qline([0 -ticklen], [0 0]);
  if ~isempty(lbls)
    qtext(-lbldist, 0, lbls{k});
  end
end
qendgroup;

if ~isempty(ttl) 
  if lbldist>=0
    whr = 'left';
  else
    whr = 'right';
  end
  if ttldist>=0
    ang=-pi/2;
  else
    ang=pi/2;
  end
  if sign(lbldist)==sign(ttldist)
    algn='bottom';
    sgn=-1;
  else
    algn='top';
    sgn=1;
  end
  qat(whr, mean(xlim), ang);
  qalign('center', algn);
  qtext(0, sgn*abs(ttldist), ttl);
end

idx = qp_idx;
global qp_data;
qp_data.info(idx).lastax='y';
qp_data.info(idx).lastcoord=y0;
qp_data.info(idx).lastlim=xlim;
qendgroup;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function qxa_usage() 
error('Usage: qyaxis X0 [ylim] ypts [lbls] [title]');
