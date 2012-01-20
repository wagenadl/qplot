function qp_axis(varargin)
% QP_AXIS - Internal backend for axis rendering
%   QP_AXIS(k1, v1, ...) draws an axis according to the parameters:
%     orient: 'x' or 'y'
%     lim_d (2x1) limits of the axis in data coordinates (in the direction 
%                 of ORIENT)
%     lim_p (2x1) shift of those limits in paper coordinates
%     tick_d (Nx1) data coordinates (in the direction of ORIENT) of ticks
%     tick_p (Nx1) shift of those coords in paper coordinates
%     tick_lbl {Nx1} labels to be placed at those ticks
%     ttl (string) title
%     ticklen (scalar) length of ticks, +ve is down/right
%     lbldist (scalar) dist b/w labels and axis/ticks, +ve is down/right
%     ttldist (scalar) dist b/w title and labels/axis/ticks, +ve is down/right
%     coord_d (scalar) position of the axis in data coords (in the direction
%                      orthogonal to ORIENT)
%     coord_p (scalar) shift of that position in paper coordinates
%     ttlrot (scalar) rotation of title: 0=normal +ve=CCW -ve=CW

kv = getopt('orient=''x'' lim_d=[] lim_p=[] tick_d=[] tick_p=[] tick_lbl={} ttl='''' ticklen=3 lbldist=3 ttldist=3 coord_d=nan coord_p=0 ttlrot=0',  varargin);

idx = qp_idx;
global qp_data;
qp_data.info(idx).lastax=kv;

if strcmp(kv.orient,'x')
  ishori=1;
  isvert=0;
elseif strcmp(kv.orient,'y')
  ishori=0;
  isvert=1;
else
  error('orient must be ''x'' or ''y''');
end

if isempty(kv.lim_d)
  kv.lim_d = zeros(size(kv.lim_p)) + nan;
elseif isempty(kv.lim_p)
  kv.lim_p = zeros(size(kv.lim_d));
end

if isempty(kv.tick_d)
  kv.tick_d = zeros(size(kv.tick_p)) + nan;
elseif isempty(kv.tick_p)
  kv.tick_p = zeros(size(kv.tick_d));
end

qgroup;

tickdx = kv.tick_d;
tickdy = zeros(size(tickdx))+kv.coord_d;
tickpx = kv.tick_p;
tickpy = zeros(size(tickpx))+kv.coord_p;
ticklx = 0;
tickly = kv.ticklen;
lbllx = 0;
lblly = kv.lbldist;

if sign(tickly)==sign(lblly)
  lblly=lblly+tickly;
end

% Axis line position (x and y may be flipped later!)
limdx = kv.lim_d;
limdy = kv.coord_d+[0 0];
limpx = kv.lim_p;
limpy = kv.coord_p+[0 0];

if ~isempty(kv.lim_d) && ~isnan(kv.lim_d(1))
  ttldx = mean(limdx);
elseif ~isempty(kv.tick_d) && ~isnan(kv.tick_d(1))
  ttldx = mean([tickdx(1) tickdx(end)]);
else
  ttldx = nan;
end
ttldy = kv.coord_d;

if ~isempty(kv.lim_p)
  ttlpx = mean(limpx);
elseif ~isempty(kv.tick_p)
  ttlpx = mean([tickpx(1) tickpx(end)]);
else
  ttlpx = 0;
end
ttlpy = kv.coord_p;

% Draw an axis line if desired
if ~isempty(kv.lim_d)
  if isvert
    [ limdx, limdy ] = identity(limdy, limdx);
    [ limpx, limpy ] = identity(limpy, limpx);
  end
  qgline({ 'absdata',  limdx(1),limdy(1), ...
           'relpaper', limpx(1), limpy(1)}, ...
	 { 'absdata',  limdx(2), limdy(2), ...
	   'relpaper', limpx(2), limpy(2)});
end	   

% Draw ticks if desired
if isvert
  [tickdx, tickdy] = identity(tickdy, tickdx);
  [tickpx, tickpy] = identity(tickpy, tickpx);
  [ticklx, tickly] = identity(tickly, ticklx);
  [lbllx, lblly]   = identity(lblly, lbllx);
end
if kv.ticklen~=0
  for k=1:length(tickdx)
    qgline({ 'absdata',  tickdx(k), tickdy(k), ...
	     'relpaper', tickpx(k), tickpy(k) }, ...
	   { 'absdata',  tickdx(k), tickdy(k), ...
	     'relpaper', tickpx(k)+ticklx, tickpy(k)+tickly });
  end
end

% Draw labels if desired
if ~isempty(kv.tick_lbl)
  qgroup
  [xa, ya] = qpa_align(ishori, lbllx, lblly);
  qalign(xa, ya);
  if ishori
    reftxt='';
    for k=1:length(kv.tick_lbl)
      reftxt = [ reftxt kv.tick_lbl{k} ];
    end
    qreftext(reftxt);
  end
      
  for k=1:length(kv.tick_lbl)
    qat(tickdx(k), tickdy(k));
    qtext(tickpx(k)+lbllx, tickpy(k)+lblly, kv.tick_lbl{k});
  end

  qreftext('');
  qendgroup;
end

% Draw title if desired
if ~isempty(kv.ttl)
  ttllx = 0;
  ttlly = kv.ttldist;
  if isvert
    [ttlpx, ttlpy] = identity(ttlpy, ttlpx);
    [ttllx, ttlly] = identity(ttlly, ttllx);
    [ttldx, ttldy] = identity(ttldy, ttldx);
  end

  
  if isempty(kv.tick_lbl) || sign(kv.ttldist)~=sign(kv.lbldist)
    % Ignore labels when placing title: not on same side
    if sign(kv.ttldist)==sign(kv.ticklen)
      ttllx = ttllx + ticklx;
      ttlly = ttlly + tickly;
    end
    qat(ttldx, ttldy, -pi/2*sign(kv.ttlrot));
  else
    if ishori
      ttlpy=0;
    else
      ttlpx=0;
    end
    [xa, ya] = qpa_align(ishori, -kv.ttldist);
    if ishori
      qat(ttldx, ya, -pi/2*sign(kv.ttlrot));
    else
      qat(xa, ttldy, -pi/2*sign(kv.ttlrot));
    end
  end
  if kv.ttlrot==0
    [xa, ya] = qpa_align(ishori, kv.ttldist);
  else
    [xa, ya] = qpa_align(isvert, kv.ttldist*sign(kv.ttlrot));
  end
  qalign(xa, ya);
  if kv.ttlrot
    qtext(-sign(kv.ttlrot)*(ttlpy+ttlly), ...
	sign(kv.ttlrot)*(ttlpx+ttllx), kv.ttl);
  else
    qtext(ttlpx+ttllx, ttlpy+ttlly, kv.ttl);
  end
end
qendgroup

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function varargout = identity(varargin)
varargout=varargin;

function [xa, ya] = qpa_align(hori, dx, dy)
if nargin<3
  dy=dx;
end

xa = 'center';
ya = 'middle';
if hori
  if dy>0
    ya = 'top';
  else
    ya = 'bottom';
  end
else
  if dx>0
    xa = 'left';
  else
    xa = 'right';
  end
end
