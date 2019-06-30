
class AxArgs:
    orient='x'
    lim_d=None
    tick_d=None
    tick_p=None
    tick_lbl=None
    ttl=''
    ticklen=3
    lbldist=3
    ttldist=3
    coord_d=None
    coord_p=0
    ttlrot=0
    cbar=None

# ------------------------------------------------------
#  function [xlim, xpts, lbls, ttl] = qi.axargs(err, varargin)
def qi.axargs(err, *args):
    '''QI.AXARGS - Regularize arguments for qxaxis and qyaxis'''
    nargin = 1 + len(args)
    
    
    if nargin<2:
        error(err)
    xlim = varargin{1}
    varargin=varargin(2:end)
    
    if isempty(xlim):
        xlim=[nan nan]
    if ~isa(xlim, 'function_handle') && ~isnvector(xlim):
        error(err)
    
    if length(xlim)~=2:
        if isa(xlim, 'function_handle'):
            if isempty(varargin):
                error(err)
            else:
                xpts = xlim(varargin{1})
        else:
            xpts = xlim
        xlim = [xpts(1) xpts(end)]
    elif ~isempty(varargin) && isnvector(varargin{1})
        xpts = varargin{1}
        varargin = varargin(2:end)
    elif ~isempty(varargin) && isnumeric(varargin{1}) && isempty(varargin{1})
        xpts = []
        varargin = varargin(2:end)
    elif length(varargin)>=2 && isa(varargin{1}, 'function_handle') ...
                && isnvector(varargin{2})
        xpts = varargin{1}(varargin{2})
        varargin = varargin(2:end)
    else:
        xpts = xlim
    
    if length(xlim)~=2:
        error(err)
    
    lbls = qi.format(xpts)
    if ~isempty(varargin):
        if isnumeric(varargin{1}):
            lbls = qi.format(varargin{1})
            varargin = varargin(2:end)
        elif iscell(varargin{1})
            lbls = varargin{1}
            varargin = varargin(2:end)
        elif isa(varargin{1}, 'function_handle') && ~isempty(xpts)
            lbls = cell(size(xpts))
            for k=1:length(xpts):
                lb = varargin{1}(xpts(k))
                if isnumeric(lb):
    	lb = qi.format(lb)
    	lbls{k} = lb{1}
                else:
    	lbls{k} = lb
            varargin = varargin(2:end)
    
    ttl = ''    if ~isempty(varargin):
        if ischar(varargin{1}):
            ttl = varargin{1}
            varargin = varargin(2:end)
    
    if isempty(lbls):
    
    elif length(lbls) ~= length(xpts)
        error(err)
    

# ------------------------------------------------------
#  function qi.axis(varargin)
def qi.axis(orient='x', lim_d=None, tick_d=None, tick_p=None,
            tick_lbl=None, ttl='',
            ticklen=3, lbldist=3, ttldist=3,
            coord_d=None, coord_p=0,
            ttlrot=0,
            cbar=None):
    '''QI.AXIS - Internal backend for axis rendering
    QI.AXIS(...) draws an axis according to the parameters:
      orient: 'x' or 'y'
      lim_d (2x1) limits of the axis in data coordinates (in the direction
                              of ORIENT)
      lim_p (2x1) shift of those limits in paper coordinates
      tick_d (Nx1) data coordinates (in the direction of ORIENT) of ticks
      tick_p (Nx1) shift of those coords in paper coordinates
      tick_lbl {Nx1} labels to be placed at those ticks
      ttl (string) title
      ticklen (scalar) length of ticks, +ve is down/right
      lbldist (scalar) dist b/w labels and axis/ticks, +ve is down/right
      ttldist (scalar) dist b/w title and labels/axis/ticks, +ve is down/right
      coord_d (scalar) position of the axis in data coords (in the direction
                                         orthogonal to ORIENT)
      coord_p (scalar) shift of that position in paper coordinates
      ttlrot (scalar) rotation of title: 0=normal +ve=CCW -ve=CW
          cbar (struct) optional reference to colorbar'''

    idx = qi.idx()
    global qdata
    
    qdata.figs[fn].lastax=kv
    
    if strcmp(kv.orient,'x'):
        ishori=1
        isvert=0
    elif strcmp(kv.orient,'y')
        ishori=0
        isvert=1
    else:
        error('orient must be ''x'' or ''y''')    
    if isempty(kv.lim_d):
        kv.lim_d = zeros(size(kv.lim_p)) + nan
    elif isempty(kv.lim_p)
        kv.lim_p = zeros(size(kv.lim_d))
    
    if isempty(kv.tick_d):
        kv.tick_d = zeros(size(kv.tick_p)) + nan
    elif isempty(kv.tick_p)
        kv.tick_p = zeros(size(kv.tick_d))
    
    qgroup
    
    tickdx = kv.tick_d
    tickdy = zeros(size(tickdx))+kv.coord_d
    tickpx = kv.tick_p
    tickpy = zeros(size(tickpx))+kv.coord_p
    ticklx = 0
    tickly = kv.ticklen
    lbllx = 0
    lblly = kv.lbldist
    
    if sign(tickly)==sign(lblly):
        lblly=lblly+tickly
    
    # Axis line position (x and y may be flipped later!)
    limdx = kv.lim_d
    limdy = kv.coord_d+[0 0]
    limpx = kv.lim_p
    limpy = kv.coord_p+[0 0]
    
    if ~isempty(kv.lim_d) && ~isnan(kv.lim_d(1)):
        ttldx = mean(limdx)
    elif ~isempty(kv.tick_d) && ~isnan(kv.tick_d(1))
        ttldx = mean([tickdx(1) tickdx(end)])
    else:
        ttldx = nan
    ttldy = kv.coord_d
    
    if ~isempty(kv.lim_p):
        ttlpx = mean(limpx)
    elif ~isempty(kv.tick_p)
        ttlpx = mean([tickpx(1) tickpx(end)])
    else:
        ttlpx = 0
    ttlpy = kv.coord_p
    
    # Draw an axis line if desired
    if ~isempty(kv.lim_d):
        if isvert:
            [ limdx, limdy ] = identity(limdy, limdx)
            [ limpx, limpy ] = identity(limpy, limpx)
        qgline({ 'absdata',    limdx(1),limdy(1), ...
                         'relpaper', limpx(1), limpy(1)}, ...
    	 { 'absdata',    limdx(2), limdy(2), ...
    	     'relpaper', limpx(2), limpy(2)})
    
    # Draw ticks if desired
    if isvert:
        [tickdx, tickdy] = identity(tickdy, tickdx)
        [tickpx, tickpy] = identity(tickpy, tickpx)
        [ticklx, tickly] = identity(tickly, ticklx)
        [lbllx, lblly]     = identity(lblly, lbllx)
    if kv.ticklen~=0:
        for k=1:length(tickdx):
            qgline({ 'absdata',    tickdx(k), tickdy(k), ...
    	         'relpaper', tickpx(k), tickpy(k) }, ...
    	     { 'absdata',    tickdx(k), tickdy(k), ...
    	         'relpaper', tickpx(k)+ticklx, tickpy(k)+tickly })
    
    # Draw labels if desired
    if ~isempty(kv.tick_lbl):
        qgroup
        [xa, ya] = qpa_align(ishori, lbllx, lblly)
        qalign(xa, ya)
        if ishori:
            reftxt=''
            for k=1:length(kv.tick_lbl):
                if str2double(kv.tick_lbl{k}) < 0:
    	kv.tick_lbl{k} = [ kv.tick_lbl{k} ' ' ]
                reftxt = [ reftxt kv.tick_lbl{k} ]
            qreftext(reftxt)
    
        for k=1:length(kv.tick_lbl):
            qat(tickdx(k), tickdy(k))
            qtext(tickpx(k)+lbllx, tickpy(k)+lblly, kv.tick_lbl{k})
    
        qreftext('')
        qendgroup
    
    # Draw title if desired
    if ~isempty(kv.ttl):
        ttllx = 0
        ttlly = kv.ttldist
        if isvert:
            [ttlpx, ttlpy] = identity(ttlpy, ttlpx)
            [ttllx, ttlly] = identity(ttlly, ttllx)
            [ttldx, ttldy] = identity(ttldy, ttldx)
    
    
        if isempty(kv.tick_lbl) || sign(kv.ttldist)~=sign(kv.lbldist):
            # Ignore labels when placing title: not on same side
            if sign(kv.ttldist)==sign(kv.ticklen):
                ttllx = ttllx + ticklx
                ttlly = ttlly + tickly
            qat(ttldx, ttldy, -pi/2*sign(kv.ttlrot))
        else:
            if ishori:
                ttlpy=0
            else:
                ttlpx=0
            [xa, ya] = qpa_align(ishori, -kv.ttldist)
            if ishori:
                qat(ttldx, ya, -pi/2*sign(kv.ttlrot))
            else:
                qat(xa, ttldy, -pi/2*sign(kv.ttlrot))
        if kv.ttlrot==0:
            [xa, ya] = qpa_align(ishori, kv.ttldist)
        else:
            [xa, ya] = qpa_align(isvert, kv.ttldist*sign(kv.ttlrot))
        qalign(xa, ya)
        if kv.ttlrot:
            qtext(-sign(kv.ttlrot)*(ttlpy+ttlly), ...
    	sign(kv.ttlrot)*(ttlpx+ttllx), kv.ttl)
        else:
            qtext(ttlpx+ttllx, ttlpy+ttlly, kv.ttl)
    qendgroup
    
    
    ######################################################################
    function varargout = identity(varargin)
    varargout=varargin
    
    function [xa, ya] = qpa_align(hori, dx, dy)
    if nargin<3:
        dy=dx
    
    xa = 'center'
    ya = 'middle'
    if hori:
        if dy>0:
            ya = 'top'
        else:
            ya = 'bottom'
    else:
        if dx>0:
            xa = 'left'
        else:
            xa = 'right'
    

# ------------------------------------------------------
#  function [dh,dx,dy] = qi.cbargs(dflt, varargin)
def qi.cbargs(dflt, *args):
    '''
'''
    
    
    switch length(varargin)
    case 0
        dh = dflt
        dx = 0
        dy = 0
    case 1
        dh = varargin{1}
        dx = 0
        dy = 0
    case 2
        dx = varargin{1}
        dy = varargin{2}
        dh = dflt
    case 3
        dx = varargin{1}
        dy = varargin{2}
        dh = varargin{3}
    otherwise
        error('QCBAR: syntax error')

# ------------------------------------------------------
#  function cb = qi.cbinfo
def qi.cbinfo():
    '''QI.CBINFO - Extract information about colorbar
   cb = QI.CBINFO extracts information about the most recent QCOLORBAR.
   CB will be a struct with fields:
     hori: 1/0 if the colorbar is horizontal/vertical
     flip: 1/0 if the orientation is flipped
     c0: lower limit of data range represented
     c1: upper limit of data range represented
     xywh: rectangle of the colorbar in data space'''
    
    
    idx = qi.idx
    global qdata
    
    if ~isfield(qdata.figs[fn], 'cbar'):
        error('QI.CBINFO cannot function without a colorbar')
    
    cb = qdata.figs[fn].cbar
    [cb.c0, cb.c1] = qi.clim
    

# ------------------------------------------------------
#  function [c0, c1] = qi.clim
def qi.clim():
    '''QI.CLIM - Get current color limits
   [c0, c1] = QI.CLIM gets the color limits from the most recent QIMSC.'''
    
    
    idx = qi.idx
    global qdata
    if isfield(qdata.figs[fn], 'clim'):
        c0 = qdata.figs[fn].clim(1)
        c1 = qdata.figs[fn].clim(2);
    else:
        c0 = 0
        c1 = 1


# ------------------------------------------------------
#  function str = qi.id(n)
def qi.id(n):    ''''''
    str = ''    n=n-1
    while n>0 || isempty(str):
        x = mod(n,26)
        n = floor(n/26)
        str = [ char(x+'A') str ]
    

    
# ------------------------------------------------------
#  function n = qi.revid(str)
def qi.revid(str):    '''
'''
    n=0
    while ~isempty(str):
        n = 26*n + str(1)-'A'
        str=str(2:end)
    n = n+1;

# ------------------------------------------------------
#  function [y_min,y_max] = qi.sampleminmax(xx,ii)
def qi.sampleminmax(xx,ii):
    '''QI.SAMPLEMINMAX - Find minima and maxima in bins of sampled data
   [y_min,y_max] = SAMPLEMINMAX(xx,ii) finds the minima and the maxima
   of the data XX in the intervals [ii_1,ii_2), [ii_2,ii_3), ...,
   [ii_n-1,ii_n). Note that xx(ii_n) is never used. 
   Usage note: This is useful for plotting an electrode trace at just
   the resolution of the screen, without losing spikes.'''
    
    
    # warning('this should have been a mex/oct file')
    
    N=length(ii)-1
    y_min=zeros(1,N)
    y_max=zeros(1,N)
    
    for n=1:N:
        y_min(n) = min(xx(ii(n):ii(n+1)-1))
        y_max(n) = max(xx(ii(n):ii(n+1)-1))

# ------------------------------------------------------
#  function [on,off] = qi.schmitt(xx,thr_on,thr_off,laststyle)
def qi.schmitt(xx,thr_on,thr_off,laststyle):
    '''SCHMITT  Schmitt trigger of a continuous process.
  [on,off] = SCHMITT(xx,thr_on,thr_off) is like a Schmitt trigger:
  ON are the indices when XX crosses up through THR_ON coming from 
  below THR_OFF;
  OFF are the indices when XX crosses down through THR_OFF coming from 
  above THR_ON.
  If XX is high at the beginning, the first ON value will be 1.
  By default, if XX is high at the end, the last upward crossing is ignored.
  [on,off] = SCHMITT(xx,thr_on,thr_off,1) detects the last upward crossing,
  making ON be 1 longer than OFF.
  [on,off] = SCHMITT(xx,thr_on,thr_off,2) detects the last upward crossing,
  making the last entry of OFF be length(XX)+1.
  [on,off] = SCHMITT(xx,thr_on,thr_off,3) detects the last upward crossing,
  making the last entry of OFF be +inf.
  If THR_OFF is not specified, it defaults to THR_ON/2.
  If neither THR_ON nor THR_OFF are specified, THR_ON=2/3 and THR_OFF=1/3.'''
    nargin = 4
    
    
    if nargin<3 :
            thr_off=[]
    if nargin<2:
        thr_on=[]
    if isempty(thr_on):
        thr_on = 2/3
    if isempty(thr_off):
        thr_off=thr_on/2
    
    if thr_on<=thr_off:
        on=[]
        off=[]
        return
    
    if nargin<4:
        laststyle=0
    
    xx=xx(:)
    up = xx>=thr_on & [-inf; xx(1:end-1)]<thr_on
    dn = xx<thr_off & [inf;    xx(1:end-1)]>=thr_off
    any = up|dn
    idx_any = find(any)
    
    if isempty(idx_any):
        on=[]
        off=[]
        return
    
    
    typ_any = up(any)
    use = [1; diff(typ_any)]
    
    idx_use =idx_any(use~=0)
    typ_use = typ_any(use~=0)
    
    if ~isempty(typ_use):
        if typ_use(1)==0:
            idx_use = idx_use(2:end)
            typ_use = typ_use(2:end)
    
    if laststyle==0:
        if ~isempty(typ_use):
            if typ_use(end)==1:
                idx_use = idx_use(1:end-1)
                typ_use = typ_use(1:end-1)
    
    on = idx_use(typ_use==1)
    off = idx_use(typ_use==0)
    
    if laststyle>=2:
        if length(off)<length(on):
            if laststyle==3:
                off=[off;inf]
            else:
                off=[off;length(xx)+1]



# ------------------------------------------------------
#  function y=strtoks(x,s,needle)
def strtoks(x,s,needle):
    '''y = STRTOKS(x) returns a cell array of strings consisting of the
space delimited parts of X.
y = STRTOKS(x,s) uses S instead of space.
y = STRTOKS(...,needle) only returns those tokens that contain NEEDLE
as a substring.'''
    nargin = 3
    
    
    if nargin<2:
        s=[]
    
    if iscell(x):
        y=x
        return
    
    n=1
    y=cell(0,1)
    while length(x)>0:
        if ~isempty(s):
            [ z, x ] = strtok(x,sprintf(s))
        else:
            [ z, x ] = strtok(x)
        if length(z):
            y{n}=z
            n=n+1
    
    if nargin>=3:
        z=cell(0,1)
        m=1
        for n=1:length(y):
            if strfind(y{n},needle):
                z{m}=y{n}
                m=m+1
        y=z

# ------------------------------------------------------
#  function qclf 
def qclf():
    '''QCLF - Clear current QPlot figure
  QCLF clears the current QPlot figure. '''
    global qdata
    fd = qi.fd(1)
    fn = qdata.curfn
    fclose(fd)
    fd = fopen(fn, 'r')
    l0 = fgets(fd)
    fclose(fd)
    fd = fopen(fn, 'w')
    fprintf(fd, '#s', l0)
    idx = strmatch(fn, qdata.fns, 'exact')
    qdata.figs[fn].fd = fd
    
    
    qi.reset(idx)
    
    qi.flush(fd)
    



    

# ------------------------------------------------------
#  function qcaligraph(xx, yy, ww)
def qcaligraph(xx, yy, ww):
    '''QCALIGRAPH - Draw a variable-width line series in data space
   QCALIGRAPH(xx, yy, ww) plots the data YY vs XX. XX and YY are given in 
   data coordinates. WW specifies the line width at each point, in postscript
   points.
   The line is rendered in the current pen's color; dash patterns and cap
   and join styles are not used.'''
    nargin = 3
    
    
    if nargin<3:
        error('Usage: qcaligraph xx yy ww')
    
    fd = qi.fd(1)
    
    if ~isnvector(xx) || ~isreal(xx):
        error('xx must be a real vector')
    if ~isnvector(yy) || ~isreal(yy):
        error('yy must be a real vector')
    if ~isnvector(ww) || ~isreal(ww):
        error('ww must be a real vector')
    if length(xx) ~= length(yy) || length(xx) ~= length(ww):
        error('xx, yy, and ww must be equally long')
    xx=xx(:)
    yy=yy(:)
    ww=ww(:)
    
    [iup, idn] = qi.schmitt(~isnan(xx+yy+ww),.7,.3,2)
    
    for k=1:length(iup):
        N = idn(k) - iup(k)
        fprintf(fd, 'caligraph *#i *#i *#i\n', N, N, N)
        fwrite(fd, xx(iup(k):idn(k)-1), 'double')
        fwrite(fd, yy(iup(k):idn(k)-1), 'double')
        fwrite(fd, ww(iup(k):idn(k)-1), 'double')
    
    qi.flush(fd)

# ------------------------------------------------------
#  function qcaxis(varargin)
def qcaxis(*args):
    '''QCAXIS - Plot colorbar axis
   QCAXIS([c0 c1], cc) plots a colorbar axis with ticks at represented
   values CC with the bar stretching to C0 and C1. (CC may be empty.)
   QCAXIS(cc) calculates C0 and C1 from CC.
   QCAXIS(..., lbls) where LBLS is either a cell array or numeric vector
   the same size as CC overrides the default tick labels. Labels are
   suppressed if LBLS is empty.
   QCAXIS(..., ttl) adds a title to the axis.
   QCAXIS normally places the axis to the right or below the color bar, but
   if the color bar was created with negative width, the axis goes to the
   left or above instead.
   QCAXIS(dir, ...), where DIR is one of 'l', 't', 'b', or 'r', overrides
   the default location.

   QCAXIS interprets settings from QTICKLEN, QTEXTDIST, and QAXSHIFT
   differently from QXAXIS and QYAXIS: positive values are away from the
   colorbar.
   Note that currently QMTICKS doesn't understand about this convention,
   so QMTICKS will produce unexpected results when used with QCAXIS.'''
    nargin = 0 + len(args)
    
    
    idx = qi.idx
    global qdata
    if ~isfield(qdata.figs[fn], 'cbar'):
        error('QCAXIS needs a previous QCBAR')
    cb = qdata.figs[fn].cbar
    
    if nargin==0 || (nargin==1 && ischar(varargin{1})):
        if nargin==1:
            ttl = varargin{1}
        else:
            ttl = ''        # Automatic everything
        clim = cb.clim
        tkx = sensibleticks(clim)
        clim_t = sprintf('[#g #g]', clim)
        tkx_t = ''
            for i=1:length(tkx):
                tkx_t = [tkx_t sprintf(' #g', tkx(i))]
            tkx_t = [ tkx_t ']' ]
        tkx_t(1) = '['
        fprintf(1, 'qcaxis(#s, #s, ''#s'');\n', clim_t, tkx_t, ttl)
        qcaxis(clim, tkx, ttl)
        return
    
    side = sign(cb.xywh_p(3)+cb.xywh_p(4))
    
    if ~isempty(varargin):
        if ischar(varargin{1}):
            switch varargin{1}
                case 'l'
    	side = -1
                case 't'
    	side = -1
                case 'b'
    	side = 1
                case 'r'
    	side = -1
                otherwise
    	error('Side must be l/t/b/r')
            varargin = varargin(2:end)
    
    err = 'Usage: qcaxis [side] [clim] cpts [lbls] [title]'
    [clim, cpts, lbls, ttl] = qi.axargs(err, varargin{:})
    
    ticklen = qdata.figs[fn].ticklen
    axshift = qdata.figs[fn].axshift
    lbldist = qdata.figs[fn].textdist(1)
    ttldist = qdata.figs[fn].textdist(2)
    
    dlim = qca_ctodat(clim, cb)
    dpts = qca_ctodat(cpts, cb)
    plim = qca_ctopap(clim, cb)
    ppts = qca_ctopap(cpts, cb)
    
    plim(isnan(plim))=0
    ppts(isnan(ppts))=0
    
    switch cb.orient
        case 'y'
            lblrot = qytitlerot
            dcoord = cb.xywh_d(1)
            pcoord = cb.xywh_p(1)
            if side>0:
                dcoord = dcoord+cb.xywh_d(3)
                if cb.xywh_p(3)>0:
    	pcoord = pcoord+cb.xywh_p(3)
            else:
                if cb.xywh_p(3)<0:
    	pcoord = pcoord+cb.xywh_p(3)
        case 'x'
            lblrot = 0
            dcoord = cb.xywh_d(2)
            pcoord = cb.xywh_p(2)
            if side<0:
                dcoord = dcoord+cb.xywh_d(4)
                if cb.xywh_p(4)<0:
    	pcoord = pcoord+cb.xywh_p(4)
            else:
                if cb.xywh_p(4)>0:
    	pcoord = pcoord+cb.xywh_p(4)
    ticklen = ticklen*side
    lbldist = lbldist*side
    ttldist = ttldist*side
    axshift = axshift*side
    
    qi.axis('orient', cb.orient, ...
            'lim_d', dlim, 'lim_p', plim, ...
            'tick_d', dpts, 'tick_p', ppts, ...
            'coord_d', dcoord, 'coord_p', pcoord+axshift, ...
            'tick_lbl', lbls, 'ttl', ttl, ...
            'ticklen', ticklen, 'lbldist', lbldist, 'ttldist', ttldist, ...
            'ttlrot', lblrot, 'cbar', cb)
    
    ######################################################################
    
    function dat = qca_ctodat(cc, cb)
    crel = (cc-cb.clim(1))/(cb.clim(2)-cb.clim(1))
    
    switch cb.orient
        case 'y'
            rng = cb.xywh_d(4)
            d0 = cb.xywh_d(2)
        case 'x'
            rng = cb.xywh_d(3)
            d0 = cb.xywh_d(1)
    if cb.rev:
        d0 = d0+rng
        rng = -rng
    
    dat = d0 + rng*crel
    
    function pap = qca_ctopap(cc, cb)
    crel = (cc-cb.clim(1))/(cb.clim(2)-cb.clim(1))
    
    switch cb.orient
        case 'y'
            rng = cb.xywh_p(4)
            d0 = cb.xywh_p(2)
        case 'x'
            rng = cb.xywh_p(3)
            d0 = cb.xywh_p(1)
    if ~cb.rev:
        d0 = d0+rng
        rng = -rng
    
    pap = d0 + rng*crel

# ------------------------------------------------------
#  function qcbar(w, l, varargin)
def qcbar(w, l, *args):    '''
QCBAR - Add a vertical color bar to a figure
  QCBAR(w, h) adds a vertical color bar of given width and height (in points)
  at the position specified by QAT. H may be positive or negative. In either
  case, the color scale runs from bottom to top.
  QCBAR(w, h, 'd') makes the color scale run down.
  QCBAR(w, h, dx, dy) or QCBAR(w, h, dx, dy, 'd') shifts the bar by the 
  given number of points to the right and down.
  QCBAR(w, [], h) or QCBAR(w,[], dx, dy, h) specifies the height in data 
  coordinates instead. In this case, the color scale runs up (down) if H 
  is positive (negative).
  This command only works after a previous QIMSC.
  QVCBAR and QHCBAR offer the same functionality with an easier interface.
  See also QCAXIS.
'''
    
    
    [dh, dx, dy] = qi.cbargs('u', varargin{:})
    
    idx = qi.idx
    global qdata
    if ~isfield(qdata.figs[fn], 'atcoord'):
        error('QCBAR needs a previous QAT')
    xy = qdata.figs[fn].atcoord
    
    lut = qlut
    C = size(lut,1)
    
    if isempty(l):
        l=0
    if l<0:
        dy=dy+l
        l=-l
    if w<0:
        dx=dx+w
        w=-w
    
    if ischar(dh):
        isup = strcmp(dh, 'u')
        xywh_d = [xy(1) xy(2) 0 0]
        xywh_p = [dx dy w l]
    else:
        isup = dh>0
        if dh<0:
            xy(2) = xy(2)+dh
            dh = -dh
        xywh_d = [xy(1) xy(2) 0 dh]
        xywh_p = [dx dy w l]
    if isup:
        lut = flipud(lut)
    qgimage(xywh_d, xywh_p, reshape(lut,[C 1 3]))
    
    idx = qi.idx
    global qdata
    qdata.figs[fn].cbar.xywh_d = xywh_d
    qdata.figs[fn].cbar.xywh_p = xywh_p
    qdata.figs[fn].cbar.orient = 'y'
    qdata.figs[fn].cbar.rev = ~isup
    qdata.figs[fn].cbar.clim = qdata.figs[fn].clim
    

# ------------------------------------------------------
#  function qcbard(xywh, vh)
def qcbard(xywh, vh):
    '''QCBARD - Adds a colorbar to the figure
   QCBARD(xywh) represents the current LUT at location XYWH, specified
   in data coordinates.
   QCBARD(xywh, vh) draws a colorbar in a nonstandard direction:
     VH = 'h' or 'r' draws a left-to-right colorbar,
     VH = 'l' draws a right-to-left colorbar,
     VH = 'd' draws a top-to-bottom colorbar,
     VH = 'v' or 'u' draws a bottom-to-top colorbar (default).'''
    nargin = 2
    
    
    if nargin<2 || isempty(vh):
        vh = 'v'
    
    if strcmp(vh, 'v') || strcmp(vh, 'u'):
        hori = 0
        flip = 0
    elif strcmp(vh, 'd')
        hori = 0
        flip = 1
    elif strcmp(vh, 'h') || strcmp(vh, 'r')
        hori = 1
        flip = 0
    elif strcmp(vh,'l')
        hori = 1
        flip = 1
    else:
        error('Usage: qcbard XYWH [v|h|l|d]')
    
    lut = qlut
    if flip :
        lut = flipud(lut)
    
    C = size(lut,1)
    if hori:
        qimage(xywh, reshape(lut, [1 C 3]))
    else:
        qimage(xywh, reshape(flipud(lut), [C 1 3]))
    
    idx = qi.idx
    global qdata
    qdata.figs[fn].cbar.rev = flip
    if hori:
        qdata.figs[fn].cbar.orient = 'x'
    else:
        qdata.figs[fn].cbar.orient = 'y'
    qdata.figs[fn].cbar.xywh_d = xywh
    qdata.figs[fn].cbar.xywh_p = [0 0 0 0]
    qdata.figs[fn].cbar.clim = qdata.figs[fn].clim

# ------------------------------------------------------
#  function qcbarh(w, l, varargin)
def qcbarh(w, l, *args):
    '''QCBARH - Add a horizontal color bar to a figure
  QCBARH(w, h) adds a horizontal color bar of given width and height
  (in points) at the position specified by QAT. W may be positive or 
  negative. In either case, the color scale runs from left to right.
  QCBARH(w, h, 'l') makes the color scale run right-to-left.
  QCBARH(w, h, dx, dy) or QCBARH(w, h, dx, dy, 'l') shifts the bar by the 
  given number of points to the right and down.
  QCBARH(w, [], dw) or QCBARH(w,[], dx, dy, dw) specifies the width in data 
  coordinates instead. In this case, the color scale runs l->r (r->l) if DW 
  is positive (negative).
  This command only works after a previous QIMSC.'''
    
    
    [dw, dx, dy] = qi.cbargs('r', varargin{:})
    
    idx = qi.idx
    global qdata
    if ~isfield(qdata.figs[fn], 'atcoord'):
        error('QCBARH needs a previous QAT')
    xy = qdata.figs[fn].atcoord
    
    lut = qlut
    C = size(lut,1)
    
    if isempty(w):
        w=0
    if l<0:
        dy=dy+l
        l=-l
    if w<0:
        dx=dx+w
        w=-w
    
    if ischar(dw):
        isright = strcmp(dw, 'r')
        xywh_d = [xy(1) xy(2) 0 0]
        xywh_p = [dx+w dy -w l]
    else:
        isright = dw>0
        if dw<0:
            xy(1) = xy(1)+dw
            dw = -dw
        xywh_d = [xy(1) xy(2) dw 0]
        xywh_p = [dx+w dy -w l]
    if ~isright:
        lut = flipud(lut)
    qgimage(xywh_d, xywh_p, reshape(lut,[1 C 3]))
    
    idx = qi.idx
    global qdata
    qdata.figs[fn].cbar.xywh_d = xywh_d
    qdata.figs[fn].cbar.xywh_p = xywh_p
    qdata.figs[fn].cbar.orient = 'x'
    qdata.figs[fn].cbar.rev = ~isright
    qdata.figs[fn].cbar.clim = qdata.figs[fn].clim
    

# ------------------------------------------------------
#  function qclf 
def qclf():
    '''QCLF - Clear current QPlot figure
  QCLF clears the current QPlot figure. '''
    global qdata
    fd = qi.fd(1)
    fn = qdata.curfn
    fclose(fd)
    fd = fopen(fn, 'r')
    l0 = fgets(fd)
    fclose(fd)
    fd = fopen(fn, 'w')
    fprintf(fd, '#s', l0)
    idx = strmatch(fn, qdata.fns, 'exact')
    qdata.figs[fn].fd = fd
    
    
    qi.reset(idx)
    
    qi.flush(fd)
    

# ------------------------------------------------------
#  function qclose(fn)
def qclose(fn):
    '''QCLOSE - Close a QPlot window
   QCLOSE closes the current window.
   QCLOSE(filename) closes the named window.
   QCLOSE('all') closes all windows.'''
    nargin = 1
    global qdata
    qi.ensure
    
    
    if nargin==0:
        fn = qdata.curfn
    elif strcmp(fn, 'all')
        fns = qdata.fns
        for k=1:length(fns):
            try
                qclose(fns{k})
            catch
                fprintf(1,'Note: #s\n', lasterr)
        qdata = []
        return
    
    if isempty(fn):
        warning('No open windows')
        return
    
    fn = qi.ensureqpt(fn)
    idx = strmatch(fn, qdata.fns, 'exact')
    if isempty(idx):
        warning('No such window')
        return
    
    if qdata.figs[fn].fd>=0:
        fd = qdata.figs[fn].fd
        qdata.figs[fn].fd=-1
        qunix(sprintf('qpclose #s', fn))
        if qdata.figs[fn].istemp:
            delete(fn)
    
        keep = [1:length(qdata.fns)]
        keep(idx) = []
        qdata.info = qdata.info(keep)
        qdata.fns = qdata.fns(keep)
    
        fclose(fd)
    
    if strcmp(fn, qdata.curfn):
        qdata.curfn = ''        for k=1:length(qdata.fns):
            if qdata.info(k).fd>=0:
                qdata.curfn = qdata.fns{k}
                break

# ------------------------------------------------------
#  function qcolorbar(xywh, lut, varargin)
def qcolorbar(xywh, lut, *args):    '''
QCOLORBAR - Adds a colorbar to the figure
   QCOLORBAR(xywh, lut) represents the LUT at location XYWH.
   QCOLORBAR(xywh, lut, tickvals) adds ticks. The first and last labels
   go at the ends of the colorbar.
   QCOLORBAR(xywh, lut, endvals, tickvals), where ENDVALS is a two-element
   vector explicitly specifies the values at the ends of the colorbar.
   QCOLORBAR(..., ticklabels) specifies the text of the labels.
   QCOLORBAR(..., caption) adds a caption.
   If LUT is given as [], QLUT is used to query the figure.

   This command is deprecated. Use QCBAR and QCAXIS instead.
'''
    nargin = 2 + len(args)
    if nargin<2:
        lut=[]
    if isempty(lut):
        lut = qlut
    
    
    if isempty(varargin):
        key=0
    else:
        key=1
        lblloc = varargin{1}
        varargin = varargin(2:end)
    
        clim = [lblloc(1) lblloc(end)]
        lbltxt = lblloc
        caption = ''        if ~isempty(varargin):
            if length(lblloc)==2 && isnvector(varargin{1}):
                lblloc = varargin{1}
                lbltxt = lblloc
                varargin = varargin(2:end)
                if length(lblloc)==2:
                    # This could be a mistake: Should we interpret as (lblloc, clbl) rather
                    # than (clim, lblloc)?
                    if isempty(varargin) || ischar(varargin{1}):
    	    lblloc = clim
    
        if ~isempty(varargin):
            if iscell(varargin{1}) || isnvector(varargin{1}):
                lbltxt = varargin{1}
                varargin = varargin(2:end)
    
        if ~isempty(varargin):
            if ischar(varargin{1}):
                caption = varargin{1}
                varargin = varargin(2:end)
    
        if ~isempty(varargin):
            error('qcolorbar: syntax error')
        if length(lblloc) ~= length(lbltxt):
            error('qcolorbar: mismatch b/w ticks and labels')
    
    C = size(lut,1)
    qimage(xywh, reshape(flipud(lut), [C 1 3]))
    
    if key:
        [lbl, ttl] = qtextdist
        if lbl<0:
            x0 = xywh(1) + xywh(3)
        else:
            x0 = xywh(1)
    
        qyaxis(x0, xywh(2)+[0 xywh(4)], ...
                (lblloc-clim(1))/(clim(2)-clim(1))*xywh(4) + xywh(2), ...
                lbltxt, caption)
    en

# ------------------------------------------------------
#  function qctext(x, y, varargin)
def qctext(x, y, *args):    '''
QCTEXT - Render text after previous text
  QCTEXT(ctext) renders text where previous text plotting left off.
  QCTEXT(dx, dy, ctext) modifies placement by the given number of points.
'''
    nargin = 2 + len(args)
    
    
    fd = qi.fd(1)
    
    if nargin==1:
        txt = x
        x = ''        y = ''
    else:
        if nargin<3:
            error('Usage: qctext [x y] ctext')
        if isnscalar(x) && isreal(x):
            x = sprintf('#g', x)
        elif isnan(str2double(x))
            error('Usage: qctext [x y] ctext')
        if isnscalar(y) && isreal(y):
            y = sprintf('#g', y)
        elif isnan(str2double(y))
            error('Usage: qctext [x y] ctext')
        txt = varargin{1}
        for k=2:length(varargin):
            txt = [ txt ' ' varargin{k} ]
    
    fprintf(fd,'ctext #s #s "#s"\n',x, y, txt)
    
    qi.flush(fd)

# ------------------------------------------------------
#  function fn = qcurrent
def qcurrent():    '''
QCURRENT - Filename of current QPlot figure
   QCURRENT returns the name of the current QPlot figure or an
   empty matrix if no QPlot figures are currently open.
'''
    
    
    qi.ensure
    global qdata
    if isempty(qdata.curfn):
        fn = []
    else:
        fn = qdata.curfn

# ------------------------------------------------------
#  function qdarrow(x, y, ang, l, w, dist, dimple)
def qdarrow(x, y, ang, l, w, dist, dimple):
    '''QDARROW - Draw an arrowhead
  QDARROW(x, y, ang) draws an arrow head pointing to (X,Y)
  in the direction ANG. ANG may be given in radians in paper (0: pointing
  right, pi/2: pointing down), or as a (DX,DY) pair of data coordinates.
  QDARROW(x, y, ang, l, w) specifies length and (full) width of the arrow
  head. These are specified in points, and default to L=8, W=5.
  QDARROW(x, y, ang, l, w, dist) specifies that the arrow is to be retracted
  a given distance from the point (X, Y).
  QDARROW(x, y, ang, l, w, dist, dimple) specifies that the back of the 
  arrow head is indented by DIMPLE points.'''
    nargin = 7
    
    
    
    if length(ang)==2:
        qat(x, y, ang(1), ang(2))
    else:
        qat(x, y, ang)
    
    if nargin<4 || isempty(l):
        l = 8
    if nargin<5 || isempty(w):
        w = .6*l
    if nargin<6 || isempty(dist):
        dist=0
    if nargin<7 || isempty(dimple):
        dimple=0
    
    qarea([0 -l dimple-l -l]-dist, [0 w 0 -w]/2)

# ------------------------------------------------------
#  function qecoplot(x0, dx, yy, N)
def qecoplot(x0, dx, yy, N):
    '''QECOPLOT - Economically plot large datasets
   QECOPLOT(xx, yy, N) plots the data (xx,yy) using SAMPLEMINMAX to
   reduce data length to the given number of points.
   The results are plotted as a QPATCH.
   It is mandatory that XX is uniformly spaced.
   QECOPLOT(x0, dx, yy, N) specifies x-coordinates in a more efficicient
   way: xx = (x0, x0+dx, x0+2*dx, ...).
   If N is omitted, it defaults to 100.
   Note: This is the kind of plot that MEABench calls "TrueBlue".'''
    nargin = 4
    
    
    if length(x0)>1:
        # Called as (xx, yy, ...)
        if nargin>=3:
            N = yy
        else:
            N = []
        yy = dx
        dx = mean(diff(x0))
        if any(abs(diff(x0) - dx) > .05*dx):
            error('qecoplot: XX vector must be uniformly spaced')
        x0 = x0(1)
    elif nargin<4
        N = []
    
    if isempty(N):
        N = 100
    
    K = length(yy)
    
    if N>K:
        N=K
    
    ii = 1 + ceil([0:N]/N * K)
    [ym, yM] = qi.sampleminmax(yy, ii)
    ii = ii(1:end-1) - .5
    
    qpatch(x0+dx*[ii fliplr(ii)], [ym fliplr(yM)])


# ------------------------------------------------------
#  function qerrorbar(xx, yy, dy, varargin)
def qerrorbar(xx, yy, dy, *args):
    '''QERRORBAR - Draw error bars
   QERRORBAR(xx, yy, dy) plots error bars at (XX,YY+-DY).
   Normally, XX, YY, and DY have the same shape. However, it is permissible
   for DY to be shaped Nx2, in which case lower and upper error bounds
   are different. (DY should always be positive).
   QERRORBAR(xx, yy, dy, w) adorns the error bars with horizontal lines of
   given width (W in points).
   QERRORBAR(..., 'up') only plots upward; QERRORBAR(..., 'down') only plots
   downward.'''
    
    
    dir = 'both'
    w = 0
    while ~isempty(varargin):
        if ischar(varargin{1}):
            dir = varargin{1}
        else:
            w = varargin{1}
        varargin=varargin(2:end)
    
    xx = xx(:)
    yy = yy(:)
    N = length(xx)
    if prod(size(dy))==2*N:
        dy_dn = -dy(:,1)
        dy_up = dy(:,2)
    else:
        dy_up = dy(:)
        dy_dn = -dy(:)
    
    switch dir
        case 'both'
            for n=1:N:
                qplot(xx(n)+[0 0],yy(n)+[dy_dn(n) dy_up(n)])
        case 'up'
            for n=1:N:
                qplot(xx(n)+[0 0],yy(n)+[0 dy_up(n)])
        case 'down'
            for n=1:N:
                qplot(xx(n)+[0 0],yy(n)+[dy_dn(n) 0])
        otherwise
            error([ 'Bad direction name: ' dir])
    
    if w>0 :
        if ~strcmp(dir, 'down'):
            # Draw top ticks
            for n=1:N:
                qat(xx(n), yy(n)+dy_up(n))
                qline([-1 1]*w/2,[0 0])
        if ~strcmp(dir, 'up'):
            # Draw down ticks
            for n=1:N:
                qat(xx(n), yy(n)+dy_dn(n))
                qline([-1 1]*w/2,[0 0])
    
    

# ------------------------------------------------------
#  function qerrorpatch(xx, yy, dy, dir)
def qerrorpatch(xx, yy, dy, dir):
    '''QERRORPATCH - Draw error patch
   QERRORPATCH(xx, yy, dy) plots an error patch at (XX,YY+-DY).
   Normally, XX, YY, and DY have the same shape. However, it is permissible
   for DY to be shaped Nx2, in which case lower and upper error bounds
   are different.
   QERRORPATCH(..., 'up') only plots upward; QERRORPATCH(..., 'down') only 
   plots downward.'''
    nargin = 4
    
    
    if nargin<4:
        dir = 'both'
    
    xx = xx(:)
    yy = yy(:)
    N = length(xx)
    if prod(size(dy))==2*N:
        dy_dn = -dy(:,1)
        dy_up = dy(:,2)
    else:
        dy_dn = -dy(:)
        dy_up = dy(:)
    
    switch dir
        case 'up'
            dy_dn = 0
        case 'down'
            dy_up = 0
    
    qpatch([xx; flipud(xx)], [yy+dy_dn; flipud(yy+dy_up)])


def qfont(*args):
    '''QFONT - Select font 
   QFONT family [bold] [italic] size  selects a new font for QPlot.
   The default font is Helvetica at 10 points.'''
    nargin = 0 + len(args)
    
    
    fd = qi.fd(1)
    
    if nargin<2 || nargin>4:
        qfont_usage
    if isnscalar(varargin{end}):
        varargin{end} = sprintf('#g', varargin{end})
    for k=1:nargin:
        if ~ischar(varargin{k}):
            qfont_usage
    for k=2:nargin-1:
        if isempty(strmatch(tolower(varargin{k}),strtoks('bold italic'), 'exact')):
            qfont_usage
    
    str = 'font'
    for k=1:nargin:
        str = [ str ' ' varargin{k} ]
    fprintf(fd, '#s\n', str)
    
    
    ######################################################################
    function str = tolower(str)
    for l=1:length(str):
        if str(l)>='A' && str(l)<='Z':
            str(l) = str(l) + 32
    
    
    function qfont_usage()
        error('Usage: qfont family [bold] [italic] size')
    
    

# ------------------------------------------------------
#  function qgarea(varargin)
def qgarea(*args):
    '''QGAREA - Generalized line drawing
  QGAREA(ptspec1, ptspec2, ...).
  A PTSPEC is a cell array containing a sequence of commands from the 
  following list:
     ABSDATA x y    - Absolute data coordinates 
     RELDATA dx dy  - Relative data coordinates 
     ABSPAPER x y   - Absolute paper coordinates (in pt)
     RELPAPER dx dy - Relative data coordinates (in pt)
     ROTDATA xi eta - Rotate by atan2(eta, xi) in data space.
                      (This affects subsequent relative positioning.) 
     ROTPAPER phi   - Rotate by phi radians. (This affects subsequent 
                      relative positioning.) 
     RETRACT l      - Retract preceding and following segments by L pt.
     RETRACT l1 l2  - Retract preceding and following segments by L1 and 
                      L2 pt respectively.

  Note: The rather cumbersome syntax of QGAREA makes QAREA and QPATCH more
  attractive for general usage. See also QGLINE.'''
    
    
    qi.gline('garea', varargin{:})

# ------------------------------------------------------
#  function qgarea2(varargin)
def qgarea2(*args):
    '''QGAREA2 - Generalized area drawing
  QGAREA(cmd1, args1, cmd2, args2, ...) specifies a area in mixed
  data and paper coordinates.
  Commands are given as (lower case) strings and are followed by
  zero or more vector arguments, depending on the command. All vectors
  must be the same length. However, scalars will be automatically converted
  to vectors of the appropriate length.
  Commands with their arguments are:

     ABSDATA x y    - Absolute data coordinates 
     RELDATA dx dy  - Relative data coordinates 
     ABSPAPER x y   - Absolute paper coordinates (in pt)
     RELPAPER dx dy - Relative data coordinates (in pt)
     ROTDATA xi eta - Rotate by atan2(eta, xi) in data space.
                      (This affects subsequent relative positioning.) 
     ROTPAPER phi   - Rotate by phi radians. (This affects subsequent 
                      relative positioning.) 
     RETRACT l      - Retract preceding and following segments by L pt.
     RETRACT l1 l2  - Retract preceding and following segments by L1 and 
                      L2 pt respectively.

  Note: The rather cumbersome syntax of QGAREA2 makes QAREA and QPATCH more
  attractive for general usage. See also QGLINE2 and QGAREA.'''
    
    
    qi.gline2('garea', varargin{:})

# ------------------------------------------------------
#  function qgimage(dxywh, pxywh, img)
def qgimage(dxywh, pxywh, img):
    '''QGIMAGE - Place an image with data and paper coordinates
  QGIMAGE(xywh_data, xywh_paper, img) places the image on a location in
  the graph specified by both data coordinates and image coordinates.
  For example: QGIMAGE([5 5 0 0],[0 0 36 72],img) creates an image of 0.5x1"
  at data location (5,5). QGIMAGE([5 nan 0 5],[0 36 72 0],img) creates an 
  image 1" wide, 5 data units high, at x=5, 1" below the top of the graph.
  Etc.'''
    
    
    [Y X C] = size(img)
    if C==1 || C==3 || C==4:
        ; # ok
    else:
        error('Image must have 1, 3, or 4 planes')
    
    if isempty(dxywh):
        dxywh = [ nan nan 0 0]
    if isempty(pxywh):
        pxywh = [ 0 0 0 0 ]
    
    if length(dxywh)~=4 || length(pxywh)~=4:
        error('Position must given as [x y w h]')
    
    str = 'image [ '
    str = [ str sprintf('#g ', dxywh) ]
    str = [ str ' ] [ ' ]
    str = [ str sprintf('#g ', pxywh) ]
    str = [ str sprintf(' ] [ #i #i #i ] *uc#i\n', X, Y, C, X*Y*C) ]
    
    img = permute(img,[3 2 1])
    if ~isa(img, 'uint8'):
        img = uint8(floor(255*img+.5))
    
    fd = qi.fd(1)
    fprintf(fd,'#s', str)
    fwrite(fd, img, 'uint8')
    qi.flush(fd)
    

# ------------------------------------------------------
#  function qgline(varargin)
def qgline(*args):
    '''QGLINE - Generalized line drawing
  QGLINE(ptspec1, ptspec2, ...).
  A PTSPEC is a cell array containing a sequence of commands from the 
  following list:

     ABSDATA x y    - Absolute data coordinates 
     RELDATA dx dy  - Relative data coordinates 
     ABSPAPER x y   - Absolute paper coordinates (in pt)
     RELPAPER dx dy - Relative data coordinates (in pt)
     ROTDATA xi eta - Rotate by atan2(eta, xi) in data space.
                      (This affects subsequent relative positioning.) 
     ROTPAPER phi   - Rotate by phi radians. (This affects subsequent 
                      relative positioning.) 
     RETRACT l      - Retract preceding and following segments by L pt.
     RETRACT l1 l2  - Retract preceding and following segments by L1 and 
                      L2 pt respectively.
     AT id          - Absolute paper coordinates of location set by AT.
     ATX id         - Absolute paper x-coordinate of location set by AT.
     ATY id         - Absolute paper y-coordinate of location set by AT.

  For instance,

      qgline({'absdata', 0, 1, 'relpaper', 5, 0}, ...
             {'absdata', 2, 3, 'relpaper', 0, 7})

  draws a line from 5 pt to the right of the point (0,1) in the graph to
  7 pt below the point (2, 3) in the graph. (Note that paper y-coordinates
  increase toward the bottom of the graph while data y-coordinates increase
  toward the top.)

  Note: The rather cumbersome syntax of QGLINE makes QLINE and QPLOT more
  attractive for general usage. The same applies to QGAREA versus QAREA 
  and QPATCH. See also QSHIFTEDLINE and QGLINE2.'''
    
    
    qi.gline('gline', varargin{:})

# ------------------------------------------------------
#  function qgline2(varargin)
def qgline2(*args):
    '''QGLINE2 - Generalized line drawing
  QGLINE(cmd1, args1, cmd2, args2, ...) specifies a line in mixed
  data and paper coordinates.
  Commands are given as (lower case) strings and are followed by
  zero or more vector arguments, depending on the command. All vectors
  must be the same length. However, scalars will be automatically converted
  to vectors of the appropriate length.
  Commands with their arguments are:

     ABSDATA x y    - Absolute data coordinates 
     RELDATA dx dy  - Relative data coordinates 
     ABSPAPER x y   - Absolute paper coordinates (in pt)
     RELPAPER dx dy - Relative data coordinates (in pt)
     ROTDATA xi eta - Rotate by atan2(eta, xi) in data space.
                      (This affects subsequent relative positioning.) 
     ROTPAPER phi   - Rotate by phi radians. (This affects subsequent 
                      relative positioning.) 
     RETRACT l      - Retract preceding and following segments by L pt.
     RETRACT l1 l2  - Retract preceding and following segments by L1 and 
                      L2 pt respectively.

  For instance,

       qgline2('absdata', [0 2], [1 3], 'relpaper', [5 0], [0 7])

  Draws a line from 5 pt to the right of the point (0, 1) in the graph
  to 7 pt below the point (2, 3) in the graph. (Note that paper 
  y-coordinates increase toward the bottom of the graph while data
  y-coordinates increase toward the top.)

  Note: The rather cumbersome syntax of QGLINE2 makes QLINE and QPLOT more
  attractive for general usage. The same applies to QGAREA versus QAREA 
  and QPATCH. See also QSHIFTEDLINE and QGLINE.'''
    
    qi.gline2('gline', varargin{:})

    

# ------------------------------------------------------
#  function qhairline(x)
def qhairline(x):
    '''QHAIRLINE - Select hairline 
   QHAIRLINE family [bold] [italic] size  selects a new hairline for QPlot.'''
    nargin = 1
    
    
    fd = qi.fd(1)
    
    if nargin~=1:
        qhairline_usage
    if ischar(x):
        x = str2double(x)
    if ~isnscalar(x):
        qhairline_usage
    
    fprintf(fd, 'hairline #g\n', x)
    
    ######################################################################
    function qhairline_usage()
    error('Usage: qhairline width')
    
    

# ------------------------------------------------------
#  function qhcbar(y0, x0, x1, w)
def qhcbar(y0, x0, x1, w):
    '''QHCBAR - Add a horizontal color bar to a figure
  QHCBAR(y0, x0, x1) adds a horizontal color bar to the figure between
  (X0, Y0) and (X1, Y0), expressed in data coordinates.
  If X1>X0, the color bar to the right, else: to the left.
  QHCBAR(..., w) specifies the width of the color bar in points (default:
  5 points). If W is positive, the bar extends down below Y0, otherwise 
  to the left.
  This only works after a preceding QIMSC and uses the lookup table (QLUT)
  used by that QIMSC.
  QHCBAR uses QAXSHIFT to create distance between Y0 and the color bar.
  Positive QAXSHIFT creates space, negative creates overlap.
  QHCBAR without arguments creates a color bar below the QIMSC.'''
    nargin = 4
    
    
    idx = qi.idx
    global qdata
    lut = qlut
    C = size(lut,1)
    
    if ~isfield(qdata.figs[fn], 'clim') ...:
                || ~isfield(qdata.figs[fn], 'imrect')
        error('qhcbar needs a preceding qimsc')
    
    if nargin==0:
        xywh = qdata.figs[fn].imrect
        x0 = xywh(1)
        y0 = xywh(2)
        x1 = xywh(1) + xywh(3)
        w = 5
        fprintf(1, 'qhcbar(#g, #g, #g, #g);\n', y0, x0, x1, w)
    elif nargin<4
        w = 5
    
    dy = qaxshift
    if w<0:
        dy = -dy
    
    isright = x1>x0
    
    if isright:
        xywh_d = [x0 y0 x1-x0 0]
    else:
        xywh_d = [x1 y0 x0-x1 0]
    
    xywh_p = [0 dy 0 w]
    
    if ~isright:
        lut = flipud(lut)
    
    qgimage(xywh_d, xywh_p, reshape(lut,[1 C 3]))
    
    idx = qi.idx
    global qdata
    qdata.figs[fn].cbar.xywh_d = xywh_d
    qdata.figs[fn].cbar.xywh_p = xywh_p
    qdata.figs[fn].cbar.orient = 'x'
    qdata.figs[fn].cbar.rev = ~isright
    qdata.figs[fn].cbar.clim = qdata.figs[fn].clim
    
    

# ------------------------------------------------------
#  function qimage(varargin)
def qimage(*args):
    '''QIMAGE - Plot an image
   QIMAGE(xywh, data) plots an image. XYWH specifies a rectangle in
   data coordinates. The image data must be YxXx1 or YxXx3 and may
   either be UINT8 or DOUBLE.
   QIMAGE(data) plots the image at (0,0)+(XxY). Note that that differs
   by 0.5 units from matlab conventions.
   QIMAGE(xx, yy, data) specifies bin centers. (Only the first and last
   elements of XX and YY actually matter).
   It is permissable for W or H to be negative; in that case, the
   image will be plotted upside down.'''
    nargin = 0 + len(args)
    
    
    fd = qi.fd(1)
    
    switch nargin
        case 1
            data = varargin{1}
            [Y X C] = size(data)
            xywh=[0 0 X Y]
        case 2
            xywh = varargin{1}
            data = varargin{2}
        case 3
            xx = varargin{1}
            yy = varargin{2}
            data = varargin{3}
            [Y X C] = size(data)
            if X==1:
                dx = 1
            else:
                dx = (xx(end)-xx(1))/(X-1)
            if Y==1:
                dy = 1
            else:
                dy = (yy(end)-yy(1))/(Y-1)
            xywh = [xx(1)-dx/2 yy(1)-dy/2 X*dx Y*dy]
            data = flipdim(data, 1)
        otherwise
            error('qimage takes 1 to 3 arguments')
    
    if ~isnvector(xywh) || ~isreal(xywh):
        error('xywh must be a real vector of length 4')
    if ~isnumeric(data) || ~isreal(data):
        error('data must be a real numeric array')
    
    if xywh(3)<0:
        data = flipdim(data, 2)
        xywh(3) = -xywh(3)
        xywh(1) = xywh(1) - xywh(3)
    if xywh(4)<0:
        data = flipdim(data, 1)
        xywh(4) = -xywh(4)
        xywh(2) = xywh(2) - xywh(4)
    
    [Y X C] = size(data)
    if C==1:
        data = repmat(data,[1 1 3])
        C=3
    elif C~=3
        error('data must be YxXx1 or YxXx3')
    
    idx = qi.idx(1)
    global qdata
    qdata.figs[fn].imrect = xywh
    
    data = permute(data,[3 2 1])
    fprintf(fd, 'image #g #g #g #g #i *uc#i\n', ...
            xywh(1), xywh(2), xywh(3), xywh(4), ...
            X, X*Y*C)
    if ~isa(data, 'uint8'):
        data = uint8(floor(255*data+.5))
    fwrite(fd, data, 'uint8')
    
    qi.flush(fd)
    

# ------------------------------------------------------
#  function qimsc(varargin)
def qimsc(*args):
    '''QIMSC - Plot 2D data as an image using lookup table
   QIMSC(xywh, data) plots the DATA as an image using a lookup previously
   set by QLUT. The color axis limits default to the min and max of the data.
   QIMSC(xywh, data, c0, c1) overrides those limits.
   QIMSC(xx, yy, data) or QIMSC(xx, yy, data, c0, c1) specifies bin centers.
   QIMSC(data) or QIMSC(data, c0, c1) sets XYWH to (0,0)+(X,Y) as in QIMAGE.'''
    nargin = 0 + len(args)
    
    
    switch nargin
        case 1
            data = varargin{1}
            c0 = min(data(:))
            c1 = max(data(:))
            [Y X] = size(data)
            xywh = [0 0 X Y]
        case 2
            xywh = varargin{1}
            data = varargin{2}
            [Y X] = size(data)
            c0 = min(data(:))
            c1 = max(data(:))
        case 3
            if isnscalar(varargin{3}):
                # So we have QIMSC(data, c0, c1)
                data = varargin{1}
                c0 = varargin{2}
                c1 = varargin{3}
                [Y X] = size(data)
                xywh = [0 0 X Y]
            else:
                # So we have QIMSC(xx, yy, data)
                xx = varargin{1}
                yy = varargin{2}
                data = varargin{3}
                [Y X] = size(data)
                if X==1:
    	dx = 1
                else:
    	dx = (xx(end)-xx(1))/(X-1)
                if Y==1:
    	dy = 1
                else:
    	dy = (yy(end)-yy(1))/(Y-1)
                xywh = [xx(1)-dx/2 yy(1)-dy/2 X*dx Y*dy]
                c0 = min(data(:))
                c1 = max(data(:))
                data = flipud(data)
        case 4
            xywh = varargin{1}
            data = varargin{2}
            [Y X] = size(data)
            c0 = varargin{3}
            c1 = varargin{4}
        case 5
            xx = varargin{1}
            yy = varargin{2}
            data = varargin{3}
            c0 = varargin{4}
            c1 = varargin{5}
            [Y X] = size(data)
            if X==1:
                dx = 1
            else:
                dx = (xx(end)-xx(1))/(X-1)
            if Y==1:
                dy = 1
            else:
                dy = (yy(end)-yy(1))/(Y-1)
            xywh = [xx(1)-dx/2 yy(1)-dy/2 X*dx Y*dy]
            data = flipud(data)
        otherwise
            error('qimsc takes 1 to 5 arguments')
    
    idx = qi.idx(1)
    global qdata
    lut = qdata.figs[fn].lut
    nanc = qdata.figs[fn].lut_nan
    qdata.figs[fn].clim = [c0 c1]
    
    [N C] = size(lut)
    data = floor(1+(N-.0001)*double(data-c0)/(c1-c0)); # normalize to color range
    data(data<1)=1
    data(data>N)=N
    
    isn = find(isnan(data))
    data(isn)=1
    imd = lut(reshape(data,[Y*X 1]),:)
    #imd(isn,:) = repmat(nanc(:)',length(isn),1)
    
    qimage(xywh, reshape(imd, [Y X C]))

# ------------------------------------------------------
#  function qlegend(str)
def qlegend(str):
    '''QLEGEND - Render legend element for plotted line
   QLEGEND(str) renders a sample of the most recently plotted line
   at the location set by QLEGOPT and writes the given string
   next to it.
   See also QMLEGEND and QPLEGEND.'''
    
    
    qlegopt; # ensure that we have options
    global qdata
    idx = qi.idx(1)
    opt = qdata.figs[fn].legopt
    
    qat(opt.x0, opt.y0)
    qline([0 1]*opt.width+opt.dx, opt.n*opt.skip + [0 0]+opt.dy)
    qgroup
    qpen(opt.color)
    qalign left base
    qtext(opt.width+opt.indent+opt.dx, opt.n*opt.skip + opt.drop+opt.dy, str)
    qendgroup
    
    qdata.figs[fn].legopt.n = opt.n + 1

# ------------------------------------------------------
#  function qlegopt(varargin)
def qlegopt(*args):
    '''QLEGOPT - Set options for QLEGEND and friends
   QLEGOPT(k1, v1, ...) specifies options for legend rendering.
   Options are specified as key, value pairs. Keys are:
     x0 - x position of left edge of legend, in data coordinates
     y0 - y position of middle of top legend element, in data coordinates
     skip - baselineskip (in points) between elements
     height - height (in points) of rendered patches
     width - width (in points) of rendered lines and patches
     indent - space between rendered samples and following text
     color - color for following text
     drop - vertical distance between middle of samples and text baseline
     dx, dy - additional horizontal and vertical displaced, in points
   All of sensible defaults, except X0 and Y0, which default to (0, 0).
   Legend elements are automatically rendered one below the other starting
   at Y0.'''
    kw = 'x0 y0 skip height width indent color drop dx dy'
    opt = getopt(kw, varargin)
    idx = qi.idx(1)
    global qdata
    if ~isfield(qdata.figs[fn],'legopt') || isempty(qdata.figs[fn].legopt):
        qdata.figs[fn].legopt.x0 = 0
        qdata.figs[fn].legopt.y0 = 0
        qdata.figs[fn].legopt.dx = 0
        qdata.figs[fn].legopt.dy = 0
        qdata.figs[fn].legopt.skip = 15
        qdata.figs[fn].legopt.n = 0
        qdata.figs[fn].legopt.drop = 3
        qdata.figs[fn].legopt.height = 9
        qdata.figs[fn].legopt.width = 18
        qdata.figs[fn].legopt.indent = 9
        qdata.figs[fn].legopt.color = 'k'
    
    
    kw = strtoks(kw)
    
    for a=1:length(kw):
        if ~isempty(opt.(kw{a})):
            qdata.figs[fn].legopt.(kw{a}) = opt.(kw{a})
            if strcmp(kw{a}, 'y0'):
                qdata.figs[fn].legopt.n = 0
    
    

# ------------------------------------------------------
#  function qline(xx, yy)
def qline(xx, yy):
    '''QLINE - Draw a line series in paper space
   QLINE(xx, yy) draws a line series between the points (XX,YY).
   XX and YY are given in postscript points. See also QPLOT and QGLINE.'''
    
    
    qi.plot(xx, yy, 'line')

# ------------------------------------------------------
#  function [lut, nanc] = qlut(lut, nanc) 
def qlut(lut, nanc):
    '''QLUT - Set lookup table for future QIMSC.
   QLUT(lut) where LUT is Nx3 sets a new lookup table for QIMSC.
   QLUT(lut, nanc) where NANC is 1x3 (or 3x1) sets a special color to use
   for NaN values. (The default is white.)
   [lut, nanc] = QLUT returns current values.'''
    nargin = 2
    
    
    if nargin<2:
        nanc=[1 1 1]
    
    idx = qi.idx
    global qdata
    
    if nargin>=1:
        qdata.figs[fn].lut = lut
        qdata.figs[fn].lut_nan = nanc
    
    clear nanc lut
    
    if nargout>=1:
        lut = qdata.figs[fn].lut
    if nargout>=2:
        nanc = qdata.figs[fn].nanc
    
    

# ------------------------------------------------------
#  function qmark(xx, yy)
def qmark(xx, yy):
    '''QMARK - Draw on the current graph with the current marker
  QMARK(xx, yy) draws marks at the given location in data space. See also
  QMARKER and QPMARK.'''
    fd = qi.fd(1)
    
    
    if isempty(xx):
        return
    
    if length(xx)~=prod(size(xx)) || ~isreal(xx):
        error('xx must be a real vector')
    if length(yy)~=prod(size(yy)) || ~isreal(yy):
        error('yy must be a real vector')
    if length(xx) ~= length(yy):
        error('xx and yy must be equally long')
    
    ok = ~isnan(xx(:)+yy(:))
    xx=xx(ok)
    yy=yy(ok)
    
    fprintf(fd, 'mark *#i *#i\n', length(xx), length(yy))
    fwrite(fd, xx, 'double')
    fwrite(fd, yy, 'double')
    
    qi.flush(fd)
    
    qi.updaterange(xx, yy)

# ------------------------------------------------------
#  function qmarker(varargin)
def qmarker(*args):
    '''QMARKER - Select a new marker for QMARK and QPMARK
   QMARKER open|solid|brush  +|x|-|||o|s|d|<|>|^|v|p|h  size
   selects a marker. An "open" mark is outlined with the current pen
   and filled with white; a "solid" mark is outlined with the current pen
   and filled with its color; a "brush" mark is outlined with the current
   pen and filled with the current brush (which may be "none").
   Marks are: o: circle/disk
              + x: horizontal+vertical or diagonal crosses
              - |: horizontal or vertical lines
              s d p h: square, diamond, pentagon, or hexagon
              < > ^ v: left / right / up / down pointing triangles
   The fill style has no effect on +|x|-|| marks.'''
    nargin = 0 + len(args)
    
    
    fd = qi.fd(1)
    
    for n=1:nargin:
        a = varargin{n}
        if ischar(a):
            if strmatch(a, strtoks('open solid brush'), 'exact'):
                ; # This is a known keyword, so good
            elif ~isempty(qi.mapmarker(a))
                ; # This is a good marker
                varargin{n} = qi.mapmarker(a)
            elif ~isnan(str2double(a))
                ; # This is a number: size
            else:
                error([ 'Cannot interpret ' a ' as an argument for qmarker' ])
        elif isnscalar(a) && isreal(a)
            ; # This is size
            varargin{n} = sprintf('#g', a)
        else:
            error([ 'Cannot interpret ' disp(a) ' as an argument for qmarker' ])
    
    str = 'marker'
    for n=1:nargin:
        str = [ str ' ' varargin{n}]
    
    fprintf(fd, '#s\n', str)
    qi.flush(fd)
    
    ######################################################################
    function str = qi.mapmarker(str)
    switch str
        case 'o'
            str = 'circle'
        case 's'
            str = 'square'
        case 'd'
            str = 'diamond'
        case '<'
            str = 'left'
        case '>'
            str = 'right'
        case '^'
            str = 'up'
        case 'v'
            str = 'down'
        case 'p'
            str = 'penta'
        case 'h'
            str = 'hexa'
        case '+'
            str = 'plus'
        case 'x'
            str = 'cross'
        case '-'
            str = 'hbar'
        case '|'
            str = 'vbar'
        otherwise
            str = []
    
    

# ------------------------------------------------------
#  function qmlegend(str)
def qmlegend(str):
    '''QMLEGEND - Render legend element for marks
   QMLEGEND(str) renders a sample of the most recently rendered 
   mark at the location set by QLEGOPT and writes the given string
   next to it.
   QMLEGEND without a string renders the most recently used mark
   over a previously rendered (line) legend.
   See also QLEGEND and QPLEGEND.'''
    nargin = 1
    
    
    qlegopt; # ensure that we have options
    global qdata
    idx = qi.idx(1)
    opt = qdata.figs[fn].legopt
    
    qat(opt.x0, opt.y0)
    
    if nargin==0:
        qpmark(.5*opt.width+opt.dx, (opt.n-1)*opt.skip+opt.dy)
    else:
        qpmark(.5*opt.width+opt.dx, opt.n*opt.skip+opt.dy)
        qgroup
        qpen(opt.color)
        qalign left base
        qtext(opt.width+opt.indent+opt.dx, opt.n*opt.skip + opt.drop+opt.dy, str)
        qendgroup
    
        qdata.figs[fn].legopt.n = opt.n + 1

# ------------------------------------------------------
#  function y = qmm
def qmm():
    '''QMM - Equivalent to 1 mm in postscript points
   QMM returns the number of postscript points in a millimeter. This
   makes it easy to write things like

      qtext(2 * qmm, 0, 'Label');'''
    
    
    y = 72/25.4

# ------------------------------------------------------
#  function qmticks(xx)
def qmticks(xx):
    '''QMTICKS - Add more ticks to an existing axis'''
    
    
    idx = qi.idx(1)
    global qdata
    
    if isempty(qdata.figs[fn].lastax):
        error('No previous axis')
    
    kv = qdata.figs[fn].lastax
    kv.lim_d=[]
    kv.lim_p=[]
    kv.tick_d = xx
    kv.tick_p = []
    kv.tick_lbl = {}
    kv.ttl = []
    kv.ticklen = qticklen
    if strcmp(kv.orient,'y'):
        kv.ticklen = -kv.ticklen
    if ~isempty(kv.cbar):
        kv.tick_d = qca_ctodat(kv.tick_d, kv.cbar)
    
    qi.axis(kv)

# ------------------------------------------------------
#  function pt = qnumfmt(pt)
def qnumfmt(pt):
    '''QNUMFMT - Specifies the format of numbers as tick labels
   QNUMFMT(fmt) specifies the format of numeric axis tick labels.
   FMT may be anything that SPRINTF understands, for instance: "%.1f".
   The default is "".'''
    nargin = 1
    
    
    idx = qi.idx
    global qdata
    
    if nargin==0:
    
        pt = qdata.figs[fn].numfmt
    
    else:
    
        qdata.figs[fn].numfmt = pt
        clear pt
    
    en

# ------------------------------------------------------
#  function qpanel(varargin)
def qpanel(*args):
    '''QPANEL - Define a new subpanel or reenter a previous one
   QPANEL(id, x, y, w, h) or QPANEL(id, xywh) defines a new panel.
   QPANEL(id) revisits a previously defined panel. ID must be a single
   capital or a dash ('-') to revert to the top level.
   Coordinates are in points from top left.
   See also QSUBPLOT.'''
    nargin = 0 + len(args)
    
    
    fd = qi.fd(1)
    
    ok=0
    if nargin==1:
        ok=1
    elif nargin==5
        ok=1
    elif nargin==2
        if length(varargin{2})==4:
            xywh = varargin{2}
            varargin{2} = xywh(1)
            varargin{3} = xywh(2)
            varargin{4} = xywh(3)
            varargin{5} = xywh(4)
            ok=1
    
    if ~ok:
        error('Usage: qpanel ID [x y w h] | -')
    id = varargin{1}
    if ~ischar(id) :
        error('Usage: qpanel ID [x y w h] | -')
    if strcmp(id,'-') && length(varargin)>1:
        error('Usage: qpanel ID [x y w h] | -')
    
    str = sprintf('panel #s', id)
    xywh = []
    for k=2:length(varargin):
        a = varargin{k}
        if ischar(a) && ~isnan(str2double(a)):
            xywh(end+1) = str2double(a)
            str = sprintf('#s #s', str, a)
        elif isnscalar(a) && isreal(a)
            xywh(end+1) = a
            str = sprintf('#s #g', str, a)
        else:
            error('Cannot interpret arguments')
    
    fprintf(fd, '#s\n', str)
    
    idx = qi.idx
    global qdata
    oldidx = strmatch(id, qdata.figs[fn].panels, 'exact')
    if isempty(oldidx):
        qdata.figs[fn].panels{end+1} = id
        oldidx = length(qdata.figs[fn].panels)
    if ~isempty(xywh):
        n = 1 + id-'A'
        qdata.figs[fn].panelextent{oldidx} = xywh
    qdata.figs[fn].panel = id
    
    qdata.figs[fn].datarange = [nan nan nan nan]


    
    

# ------------------------------------------------------
#  function qplegend(str)
def qplegend(str):
    '''QPLEGEND - Render legend element for patch
   QPLEGEND(str) renders a sample of the most recently rendered 
   patch at the location set by QLEGOPT and writes the given string
   next to it.
   See also QLEGEND and QMLEGEND.'''
    
    
    qlegopt; # ensure that we have options
    global qdata
    idx = qi.idx(1)
    opt = qdata.figs[fn].legopt
    
    qat(opt.x0, opt.y0)
    qarea([0 1 1 0]*opt.width+opt.dx, opt.n*opt.skip + [-.5 -.5 .5 .5]*opt.height+opt.dy)
    qgroup
    qpen(opt.color)
    qalign left base
    qtext(opt.width+opt.indent+opt.dx, opt.n*opt.skip + opt.drop+opt.dy, str)
    qendgroup
    
    qdata.figs[fn].legopt.n = opt.n + 1

# ------------------------------------------------------
#  function qplot(xx, yy)
def qplot(xx, yy):
    '''QPLOT - Draw a line series in data space
   QPLOT(xx, yy) plots the data YY vs XX. XX and YY are given in data
   coordinates. See also QLINE and QGLINE.'''
    nargin = 2
    
    
    if nargin==1:
        yy = xx
        xx = [1:length(yy)]
    
    qi.plot(xx, yy, 'plot')

# ------------------------------------------------------
#  function qpmark(xx, yy)
def qpmark(xx, yy):
    '''QPMARK - Draw on the current graph with the current marker
  QPMARK(xx, yy) draws marks at the given location in paper space. See also
  QMARKER and QMARK.'''
    fd = qi.fd(1)
    
    
    if ~isnvector(xx) || ~isreal(xx):
        error('xx must be a real vector')
    if ~isnvector(yy) || ~isreal(yy):
        error('yy must be a real vector')
    if length(xx) ~= length(yy):
        error('xx and yy must be equally long')
    
    fprintf(fd, 'pmark *#i *#i\n', length(xx), length(yy))
    fwrite(fd, xx, 'double')
    fwrite(fd, yy, 'double')
    
    qi.flush(fd)
    

# ------------------------------------------------------
#  function qprint(nowait)
def qprint(nowait):
    '''QPRINT - Print current QPlot figure to the default printer
   QPRINT prints the current QPlot figure using qplotml and lpr after
   waiting for confirmation from the user.
   QPRINT(1) does not wait.'''
    nargin = 1
    
    
    if nargin<1:
        nowait=0
    
    qi.ensure
    global qdata
    ifn = qdata.curfn
    if isempty(ifn):
        error('No window')
    qselect(ifn)
    
    ofn = sprintf('#s.ps', tempname)
    
    s = qunix(sprintf('qplotml #s #s', ifn, ofn))
    if s:
        error('qplot failed')
    
    if ~nowait:
        input('Press Enter to print to lpr, or Ctrl-C to cancel...')
    unix(sprintf('lpr #s', ofn))
    fprintf(1,'\nPostscript file sent to printer.\n')
    
    delete(ofn)

# ------------------------------------------------------
#  function qreftext(varargin)
def qreftext(*args):
    '''QREFTEXT - Set reference text
   QREFTEXT(text) sets the reference text used for vertical alignment
   of subsequent QTEXT commands.'''
    nargin = 0 + len(args)
    fd = qi.fd(1)
    
    
    if nargin<1:
        fprintf(fd, 'reftext\n')
    else:
        txt = varargin{1}
        for k=2:length(varargin):
            txt = [ txt ' ' varargin{k} ]
        fprintf(fd,'reftext "#s"\n', txt)

# ------------------------------------------------------
#  function qsave(ofn, reso)
def qsave(ofn, reso):
    '''QSAVE - Saves a qplot figure
   QSAVE(ofn) saves the current qplot figure to the named file.
   QSAVE(ext), where EXT is just a filename extension (without the dot),
   uses the name of the current figure.
   QSAVE(ofn, reso) specifies bitmap resolution for png/jpeg output.
   QSAVE without arguments saves to pdf.'''
    nargin = 2
    
    
    if nargin<2:
        reso = []
    
    qi.ensure
    global qdata
    ifn = qdata.curfn
    if isempty(ifn):
        error('No window')
    
    if nargin<1:
        ofn='pdf'
    
    if isempty(find(ofn=='.')):
        # Extension only
        idx = find(ifn=='.')
        ofn = [ifn(1:idx(end)) ofn]
    
    if ischar(reso):
        reso = atoi(reso)
    
    if isempty(reso):
        cmd = sprintf('qplotml #s #s', ifn, ofn)
    else:
        if ischar(reso):
            cmd = sprintf('qplotml -r#s #s #s', reso, ifn, ofn)
        else:
            cmd = sprintf('qplotml -r#i #s #s', floor(reso), ifn, ofn)
    
    s = qunix(cmd)
    if s:
        error('qplot failed')
    
    

# ------------------------------------------------------
#  function qselect(fn)
def qselect(fn):
    '''QSELECT - Select a QPlot figure by name
   QSELECT(fn) makes the named QPlot figure current'''
    
    
    global qdata
    qi.ensure
    
    dotidx = find(fn=='.')
    slashidx = find(fn=='/')
    if ~isempty(slashidx):
        dotidx = dotidx(dotidx>slashidx(end))
    if isempty(dotidx):
        fn = [ fn '.qpt' ]
    
    idx = strmatch(fn, qdata.fns, 'exact')
    
    if isempty(idx):
        # Let's see if we can match on partial file names
        F = length(qdata.fns)
        leaf=cell(F,1)
        for f=1:F:
            leaf{f} = basename(qdata.fns{f})
        idx = strmatch(fn, leaf, 'exact');
    
    if isempty(idx):
        for f=1:F:
            idx = find(leaf{f}=='.')
            if ~isempty(idx):
                leaf{f} = leaf{f}(1:idx(end)-1)
        idx = strmatch(fn, leaf, 'exact');
    
    if isempty(idx):
        idx = strmatch(fn, leaf);
    
    if isempty(idx):
        error('No such figure')
    elif length(idx)>1
        error('Ambiguous figure name')
    
    qdata.curfn = qdata.fns{idx}
    
    qunix(sprintf('touch #s', qdata.curfn)); # Bring to front

# ------------------------------------------------------
#  function qsharelim(varargin)
def qsharelim(*args):
    '''QSHARELIM - Share axis limits between QPlot panels
   QSHARELIM [x|y] ID ... shares x and/or y-axis limits with the other named
   panels.'''
    nargin = 0 + len(args)
    
    
    fd = qi.fd(1)
    
    if nargin<1:
        error('Usage: qsharelim [x|y] ID ...')
    
    str = 'sharelim'
    for k=1:nargin:
        a = varargin{k}
        if ischar(a) :
            if k==1 && (strcmp(a, 'x') || strcmp(a, 'y')):
                str = sprintf('#s #s', str, a)
            elif a(1)>='A' && a(1)<='Z'
                str = sprintf('#s #s', str, a)
            else:
                error('Cannot interpret arguments')
        else:
            error('Cannot interpret arguments');
    
    fprintf(fd, '#s\n', str)
    qi.flush(fd)
    

# ------------------------------------------------------
#  function qshiftedline(xx, yy, dx, dy)
def qshiftedline(xx, yy, dx, dy):
    '''QSHIFTEDLINE - Renders a line displaced from data points
  QSHIFTEDLINE(xx, yy, dx, dy) is like QPLOT(xx, yy) except that the 
  plot is displaced by (dx, dy) points on the graph.
  XX, YY, DX, DY may be vectors or scalars. Any scalars are automatically
  converted to vectors of the appropriate length. All vectors must be
  the same length.
  See also QGLINE.'''
    
    
    N = max([length(xx), length(yy), length(dx), length(dy)])
    
    if length(xx)==1:
        xx = repmat(xx, N, 1)
    if length(yy)==1:
        yy = repmat(yy, N, 1)
    if length(dx)==1:
        dx = repmat(dx, N, 1)
    if length(dy)==1:
        dy = repmat(dy, N, 1)
    
    ar = cell(N, 1)
    
    for n=1:N:
        ar{n} = { 'absdata', xx(n), yy(n), 'relpaper', dx(n), dy(n) }
    
    qgline(ar{:})
    
    

# ------------------------------------------------------
#  function qshrink(varargin)
def qshrink(*args):
    '''QSHRINK - Add margin to QPlot panel
   QSHRINK adds 1 point of margin to the current QPlot panel.
   QSHRINK(margin) adds the given margin (in points).
   QSHRINK(margin, ratio) forces a given aspect ratio on the data units.'''
    nargin = 0 + len(args)
    
    
    fd = qi.fd(1)
    
    if nargin>2:
        error('Usage: qshrink [margin] [ratio]')
    
    str = 'shrink'
    for k=1:nargin:
        a = varargin{k}
        if strcmp(a, '-') && k<nargin:
            str = sprintf('#s -', str)
        elif ischar(a) && ~isnan(str2double(a))
            str = sprintf('#s #s', str, a)
        elif isnscalar(a) && isreal(a)
            str = sprintf('#s #g', str, a)
        else:
            error('Cannot interpret arguments')
    
    fprintf(fd, '#s\n', str)
    qi.flush(fd)
    

# ------------------------------------------------------
#  function qskyline(xx, yy, y0)
def qskyline(xx, yy, y0):
    '''QSKYLINE - Skyline plot (bar plot)
   QSKYLINE(xx, yy) draws a bar plot of YY vs XX with bars touching.
   QSKYLINE(xx, yy, y0) specifies the baseline of the plot; default is 0.'''
    nargin = 3
    
    
    xx=xx(:)'
    yy=yy(:)'
    if nargin<3:
        y0=0
    
    if length(xx)==1:
        xxx = [-.5; .5] + xx
        yyy = [yy; yy]
    else:
        dx = diff(xx)
        dx = [dx(1) dx dx(end)]
        xxx = [xx-dx(1:end-1)/2; xx+dx(2:end)/2]
        xxx = xxx(:)
        yyy = [yy; yy]
        yyy = yyy(:)
    
    if isnan(y0):
        qplot([xxx(1); xxx; xxx(end)],[yyy(1); yyy; yyy(end)])
    else:
        qpatch([xxx(1); xxx; xxx(end)],[y0; yyy; y0])

# ------------------------------------------------------
#  function id = qsubplot(x, y, w, h)
def qsubplot(x, y, w, h):
    '''QSUBPLOT - Define a new subpanel in relative units
   QSUBPLOT(x, y, w, h) defines a new subpanel. X, Y, W, H are specified
   as fractions of the figure size.
   QSUBPLOT(rows, cols, idx) defines a new subpanel in Matlab style.
   id = QSUBPLOT(...) returns the ID of the subpanel, for use with QPANEL.'''
    nargin = 4
    
    
    if nargin==1:
        xywh = x
        x = xywh(1)
        y = xywh(2)
        w = xywh(3)
        h = xywh(4)
    if ischar(x):
        x = str2double(x)
    if ischar(y):
        y = str2double(y)
    if ischar(w):
        w = str2double(w)
    if nargin>=4 && ischar(h):
        h = str2double(h)
    if nargin==3:
        rows = x
        cols = y
        idx = w
        h=1/rows
        w=1/cols
        x=w*mod(idx-1, cols)
        y=h*floor((idx-1)/cols)
    
    idx = qi.idx(1)
    global qdata
    extent = qdata.figs[fn].extent
    
    x = extent(1) + extent(3)*x
    y = extent(2) + extent(4)*y
    w = extent(3)*w
    h = extent(4)*h
    
    subno = 1
    while 1:
        id = qi.id(subno)
        oldidx = strmatch(id, qdata.figs[fn].panels, 'exact')
        if isempty(oldidx):
            break
        else:
            subno = subno + 1
    
    qpen none
    qbrush none
    qpanel(id, x, y, w, h)
    qpen solid
    
    if nargout==0:
        clear id

# ------------------------------------------------------
#  function qtext(x, y, varargin)
def qtext(x, y, *args):
    '''QTEXT - Render text 
  QTEXT(text) renders text at the current anchor point.
  QTEXT(dx, dy, text) renders text displaced by the given number of points.'''
    nargin = 2 + len(args)
    
    
    fd = qi.fd(1)
    
    if nargin==1:
        txt = x
        x = ''        y = ''
    else:
        if nargin<3:
            error('Usage: qtext [x y] text')
        if isnscalar(x) && isreal(x):
            x = sprintf('#g', x)
        elif isnan(str2double(x))
            error('Usage: qtext [x y] text')
        if isnscalar(y) && isreal(y):
            y = sprintf('#g', y)
        elif isnan(str2double(y))
            error('Usage: qtext [x y] text')
        txt = varargin{1}
        for k=2:length(varargin):
            txt = [ txt ' ' varargin{k} ]
    
    fprintf(fd,'text #s #s "#s"\n',x, y, txt)
    
    qi.flush(fd)

# ------------------------------------------------------
#  function [lbl, ttl] = qtextdist(lbl, ttl)
def qtextdist(lbl, ttl):    '''
QTEXTDIST - Specifies distance to text labels for QXAXIS and QYAXIS
   QTEXTDIST(lbldist, ttldist) specifies distance between ticks and
   tick labels and between tick labels and axis title, in points.
   QTEXTDIST(dist) uses DIST for both distances.
   Positive numbers are to the left and down; negative numbers are to the
   right and up.
   [lbl, ttl] = QTEXTDIST returns current settings.
'''
    nargin = 2
    
    
    idx = qi.idx
    global qdata
    
    if nargin==0:
    
        lbl = qdata.figs[fn].textdist(1)
        ttl = qdata.figs[fn].textdist(2)
    
    else:
    
        if nargin==1:
            ttl = lbl
    
        if ischar(lbl):
            lbl = str2double(lbl)
        if ischar(ttl):
            ttl = str2double(ttl)
    
        qdata.figs[fn].textdist = [lbl ttl]
    
        clear lbl ttl
    
    

# ------------------------------------------------------
#  function qtextoncurve(xx, yy, dy, txt)
def qtextoncurve(xx, yy, dy, txt):    ''''''
    nargin = 4
    if nargin==3:
        txt = dy
        dy = 0
    elif nargin~=4
        error('Usage: qtextoncurve xx yy [dy] text')
    
    if ~isnvector(xx) || ~isreal(xx):
        error('xx must be a real vector')
    elif ~isnvector(yy) || ~isreal(yy)
        error('yy must be a real vector')
    elif length(xx) ~= length(yy)
        error('xx and yy must be equally long')
    elif ~isscalar(dy) || ~isreal(dy)
        error('dy must be a real scalar')
    
    idx = find(~isnan(xx+yy))
    xx = xx(idx)
    yy = yy(idx)
    N = length(xx)
    
    fd = qi.fd(1)
    
    fprintf(fd, 'textoncurve *#i *#i #g "#s"\n', N, N, dy, txt)
    fwrite(fd, xx, 'double')
    fwrite(fd, yy, 'double')
    
    qi.flush(fd)

# ------------------------------------------------------
#  function qtextonpath(xx, yy, dx, dy, txt)
def qtextonpath(xx, yy, dx, dy, txt):
    '''QTEXTONPATH - Place text along a path
   QTEXTONPATH(xx, yy, text) places the TEXT along a path (XX, YY)
   defined in data coordinates.
   QTEXTONPATH(xx, yy, dy, text) shifts the text down by DY pts in its 
   local vertical direction.
   QTEXTONPATH(xx, yy, dx, dy, text) shifts the text right by DX and
   down by DY pts in its local direction.
   QTEXTONPATH does not use coordinates set by QAT, but it does respect
   alignment set by QALIGN.
   In the present version, QTEXTONPATH only accepts plain Unicode; not
   any of the special characters sequences accepted by QTEXT.'''
    nargin = 5
    
    if nargin==3:
        txt = dx
        dx = 0
        dy = 0
    elif nargin==4
        txt = dy
        dy = dx
        dx = 0
    elif nargin~=5
        error('Usage: qtextonpath xx yy [[dx] dy] text')
    
    if ~isnvector(xx) || ~isreal(xx):
        error('xx must be a real vector')
    elif ~isnvector(yy) || ~isreal(yy)
        error('yy must be a real vector')
    elif length(xx) ~= length(yy)
        error('xx and yy must be equally long')
    elif ~isscalar(dx) || ~isreal(dx)
        error('dx must be a real scalar')
    elif ~isscalar(dy) || ~isreal(dy)
        error('dy must be a real scalar')
    
    idx = find(~isnan(xx+yy))
    xx = xx(idx)
    yy = yy(idx)
    N = length(xx)
    
    fd = qi.fd(1)
    
    fprintf(fd, 'textonpath *#i *#i #g #g "#s"\n', N, N, dx, dy, txt)
    fwrite(fd, xx, 'double')
    fwrite(fd, yy, 'double')
    
    qi.flush(fd)

# ------------------------------------------------------
#  function qvcbar(x0, y0, y1, w)
def qvcbar(x0, y0, y1, w):
    '''QVCBAR - Add a vertical color bar to a figure
  QVCBAR(x0, y0, y1) adds a vertical color bar to the figure between
  (X0, Y0) and (X0, Y1), expressed in data coordinates.
  If Y1>Y0, the color bar runs up, else: down.
  QVCBAR(..., w) specifies the width of the color bar in points (default:
  5 points). If W is positive, the bar extends to the right of X0,
  otherwise to the left.
  This only works after a preceding QIMSC and uses the lookup table (QLUT)
  used by that QIMSC.
  QVCBAR uses QAXSHIFT to create distance between X0 and the color bar.
  Positive QAXSHIFT creates space, negative creates overlap.
  QVCBAR without arguments creates a color bar to the right of the QIMSC.'''
    nargin = 4
    
    
    idx = qi.idx
    global qdata
    lut = qlut
    C = size(lut,1)
    
    if ~isfield(qdata.figs[fn], 'clim') ...:
                || ~isfield(qdata.figs[fn], 'imrect')
        error('qvcbar needs a preceding qimsc')
    
    if nargin==0:
        xywh = qdata.figs[fn].imrect
        x0 = xywh(1) + xywh(3)
        y0 = xywh(2)
        y1 = xywh(2) + xywh(4)
        w = 5
        fprintf(1, 'qvcbar(#g, #g, #g, #g);\n', x0, y0, y1, w)
    elif nargin<4
        w = 5
    
    dx = qaxshift
    if w<0:
        dx = -dx; + w
    
    isup = y1>y0
    
    if isup:
        xywh_d = [x0 y0 0 y1-y0]
    else:
        xywh_d = [x0 y1 0 y0-y1]
    
    xywh_p = [dx 0 w 0]
    
    if isup:
        lut = flipud(lut)
    
    
    qgimage(xywh_d, xywh_p, reshape(lut,[C 1 3]))
    
    idx = qi.idx
    global qdata
    qdata.figs[fn].cbar.xywh_d = xywh_d
    qdata.figs[fn].cbar.xywh_p = xywh_p
    qdata.figs[fn].cbar.orient = 'y'
    qdata.figs[fn].cbar.rev = ~isup
    qdata.figs[fn].cbar.clim = qdata.figs[fn].clim
    

# ------------------------------------------------------
#  function qxaxis(y0, varargin)
def qxaxis(y0, *args):
    '''QXAXIS - Plot x-axis
   QXAXIS(y0, [x0 x1], xx) plots an x-axis with ticks at XX. (XX may be
   empty.)
   QXAXIS(y0, xx) calculates X0 and X1 from XX.
   QXAXIS(y0, [], xx) only draws ticks, not an axis line.
   QXAXIS(..., lbls) where LBLS is either a cell array or numeric vector
   the same size as XX overrides the default tick labels. Labels are
   suppressed if LBLS is empty.
   QXAXIS(..., ttl) adds a title to the axis.

   QXAXIS obeys settings from QTICKLEN, QTEXTDIST, and QAXSHIFT.
   QXAXIS('t', ...) inverts the sign of these settings.

   Either LBLS or XX (but not both) may be a function handle in which case
   the labels are calculated from the tick positions (or vice versa). For
   example:
     QXAXIS(0, @(x) (x/100), [0:25:100], 'Value (%)')

   Without any arguments or with just a title as an argument, QXAXIS tries
   to determine sensible defaults based on previous calls to QPLOT. Your
   mileage may vary.'''
    nargin = 1 + len(args)
    
    
    
    err = 'Usage: qxaxis Y0 [xlim] xpts [lbls] [title]'
    
    if nargin<2:
        # All automatic
        if nargin==1:
            ttl = y0
        else:
            ttl = ''        global qdata
        idx = qi.idx
        dr = qdata.figs[fn].datarange
        if any(isnan(dr)):
            error('QXAXIS needs previous plot for automatic operation')
        yy = sensibleticks(dr(3:4), 1)
        xx = sensibleticks(dr(1:2), 1)
        tk_t = ''
        for k=1:length(xx):
            tk_t = [ tk_t sprintf(' #g', xx(k))]
        fprintf(1,'qxaxis(#g, [#s], ''#s'');\n', yy(1), tk_t(2:end), ttl)
        qxaxis(yy(1), xx, ttl)
        return
    
    if ischar(y0):
        if strcmp(y0, 't'):
            flip = 1
            y0 = varargin{1}
            varargin = varargin(2:end)
        else:
            error(err)
    else:
        flip = 0
    
    [xlim, xpts, lbls, ttl] = qi.axargs(err, varargin{:})
    
    ticklen = qticklen
    axshift = qaxshift
    [lbldist, ttldist] = qtextdist
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
    
    qi.axis('orient', 'x', 'lim_d', xlim, 'tick_d', xpts, 'tick_lbl', lbls, ...
            'ttl', ttl, ...
            'ticklen', ticklen, 'lbldist', lbldist, 'ttldist', ttldist, ...
            'coord_d', y0, 'coord_p', axshift)

# ------------------------------------------------------
#  function qxcaxis(y0, varargin)
def qxcaxis(y0, *args):    '''
QXCAXIS - Plot x-axis with labels between ticks
  QXCAXIS(y0, xx, xl) places labels XL at locations XX, but places
  ticks between labels rather than at the labels. First and last ticks
  are extrapolated.
  QXCAXIS(y0, [x0 x1], xx, xl) specifies those end ticks explicitly.
  QXCAXIS(..., ttl) adds a title to the axis.

   QXAXIS obeys settings from QTICKLEN, QTEXTDIST, and QAXSHIFT.
   QXAXIS('t', ...) inverts the sign of these settings.
'''
    
    
    err = 'Usage: qxcaxis Y0 [xlim] xpts lbls [title]'
    
    if ischar(y0):
        if strcmp(y0, 't'):
            flip = 1
            y0 = varargin{1}
            varargin = varargin(2:end)
        else:
            error(err)
    else:
        flip = 0
    
    [xlim, xpts, lbls, ttl] = qi.axargs(err, varargin{:})
    
    ticklen = qticklen
    axshift = qaxshift
    [lbldist, ttldist] = qtextdist
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
    
    if xlim(1)==xpts(1):
        # Automatic xlims: must override
        inbtwn = (xpts(1:end-1) + xpts(2:end))/2
        xl0 = inbtwn(1)-(xpts(2)-xpts(1))
        xl1 = inbtwn(end)+(xpts(end)-xpts(end-1))
        xlim = [xl0 xl1]
        inbtwn = [xl0; inbtwn(:); xl1]
    
    # First, place labels
    qi.axis('orient', 'x', 'lim_d', [], 'tick_d', xpts, 'tick_lbl', lbls, ...
            'ttl', ttl, ...
            'ticklen', 0, 'lbldist', lbldist+ticklen, 'ttldist', ttldist, ...
            'coord_d', y0, 'coord_p', axshift)
    
    # Then, place ticks
    qi.axis('orient', 'x', 'lim_d', xlim, 'tick_d', inbtwn, 'tick_lbl', {}, ...
            'ticklen', ticklen, 'coord_d', y0, 'coord_p', axshift)


# ------------------------------------------------------
#  function qyaxis(y0, varargin)
def qyaxis(y0, *args):
    '''QYAXIS - Plot y-axis
   QYAXIS(x0, [y0 y1], yy) plots an y-axis with ticks at YY. (YY may be
   empty.)
   QYAXIS(x0, yy) calculates Y0 and Y1 from YY.
   QYAXIS(x0, [], yy) only draws ticks, not an axis line.
   QYAXIS(..., lbls) where LBLS is either a cell array or numeric vector
   the same size as YY overrides the default tick labels. Labels are
   suppressed if LBLS is empty.
   QYAXIS(..., ttl) adds a title to the axis.

   QYAXIS obeys settings from QTICKLEN, QTEXTDIST, and QAXSHIFT.
   QYAXIS('r', ...) inverts the sign of these settings.
   QYAXIS('R', ...) additionally orients the title the other way.

   Either LBLS or YY (but not both) may be a function handle in which case
   the labels are calculated from the tick positions (or vice versa). For
   example:
     QYAXIS(0, [0:0.2:1], @(y) (y*100), 'Value (%)')

   Without any arguments or with just a title as an argument, QYAXIS tries
   to determine sensible defaults based on previous calls to QPLOT. Your
   mileage may vary.'''
    nargin = 1 + len(args)
    
    
    # Note that we use variable names from qxaxis, which may be confusing.
    
    err = 'Usage: qyaxis X0 [ylim] ypts [lbls] [title]'
    
    if nargin<2:
        # All automatic
        if nargin==1:
            ttl = y0
        else:
            ttl = ''
        global qdata
        idx = qi.idx
        dr = qdata.figs[fn].datarange
        if any(isnan(dr)):
            error('QYAXIS needs previous plot for automatic operation')
        yy = sensibleticks(dr(3:4), 1)
        xx = sensibleticks(dr(1:2), 1)
        tk_t = ''
        for k=1:length(yy):
            tk_t = [ tk_t sprintf(' #g', yy(k))]
        fprintf(1,'qyaxis(#g, [#s], ''#s'');\n', xx(1), tk_t(2:end), ttl)
        qyaxis(xx(1), yy, ttl)
        return
    
    if ischar(y0):
        if strcmp(y0, 'r') || strcmp(y0, 'R'):
            flip = 1
            if y0=='R':
                rot = 1
            else:
                rot = 0
            y0 = varargin{1}
            varargin = varargin(2:end)
        else:
            error(err)
    else:
        flip = 0
    
    [xlim, xpts, lbls, ttl] = qi.axargs(err, varargin{:})
    
    ticklen = qticklen
    axshift = qaxshift
    [lbldist, ttldist] = qtextdist
    lblrot = qytitlerot
    
    if flip:
        ticklen = -ticklen
        axshift = -axshift
        lbldist = -lbldist
        ttldist = -ttldist
        if rot:
            lblrot = -lblrot
    
    qi.axis('orient', 'y', 'lim_d', xlim, 'tick_d', xpts, 'tick_lbl', lbls, ...
            'ttl', ttl, ...
            'ticklen', -ticklen, 'lbldist', -lbldist, 'ttldist', -ttldist, ...
            'coord_d', y0, 'coord_p', -axshift, 'ttlrot', lblrot)

    


