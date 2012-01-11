function qyaxis(y0, xlim, varargin)
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

%-- Plotting starts here

ticklen = qticklen;
axshift = qaxshift;
lblrot = qylabelrot;
[lbldist, ttldist] = qtextdist;

qgroup;
qreftext('');
if any(isnan(xlim))
  xlim(1) = min(xpts);
  xlim(2) = max(xpts);
else
  qgline({'absdata',y0,xlim(1),'relpaper',-axshift,0},...
      {'absdata',y0,xlim(2),'relpaper',-axshift,0});
end

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
  qline([0 -ticklen]-axshift, [0 0]);
  if ~isempty(lbls)
    qtext(-lbldist-axshift, 0, lbls{k});
  end
end
qendgroup;

if ~isempty(ttl) 
  if sign(ttldist)==sign(lbldist)
    if ttldist>=0
      qat('left', mean(xlim), -lblrot);
    else
      qat('right', mean(xlim), -lblrot);
    end
  else
    if sign(ttldist)==sign(ticklen)
      ttldist = ttldist + ticklen;
    end
    qat(y0, mean(xlim), -lblrot);
  end

  if lblrot==0
    if ttldist>0
      qalign('right','middle');
    else
      qalign('left','middle');
    end
    qtext(-ttldist-axshift, 0, ttl);
  else
    if sign(ttldist)==sign(lblrot)
      qalign('center','bottom');
    else
      qalign('center','top');
    end
    qtext(0-axshift, -ttldist*sign(lblrot), ttl);
  end
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
