function fn = qfigure(fn, w, h)
% QFIGURE - Open a QPLOT figure
%    QFIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
%    in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
%    W defaults to 5 inches.
%    fn = QFIGURE(w, h) opens a new QPLOT figure of given size (in inches) with
%    a temporary filename.

global qp_data
qp_ensure;

istmp = 0;

if nargin<1
  fn = tempname;
  istmp = 1;
end
if ~ischar(fn)
  if nargin<2
    w = fn;
    h = w*3/4;
  else
    h = w;
    w = fn;
  end
  fn = tempname;
  istmp = 1;
else
  if nargin<2
    w=5;
  end
  if nargin<3
    h=w*3/4;
  end
end

idx = strmatch(fn, qp_data.fns, 'exact');
if ~isempty(idx)
  if qp_data.info(idx).fd>=0
    fclose(qp_data.info(idx).fd);
    qp_data.info(idx).fd=-1;
  end
end

fd = fopen(fn, 'w');
if fd<0
  error('Cannot create figure');
end

w=w*72;
h=h*72;

fprintf(fd, 'figsize %g %g\n', w, h);

qp_data.curfn = fn;

if isempty(idx)
  qp_data.fns{end+1} = fn;
  idx = length(qp_data.fns);
end

qp_data.info(idx).fd = fd;
qp_data.info(idx).istemp = istmp;
qp_data.info(idx).extent = [0 0 w h];
qp_data.info(idx).ticklen = 3;
qp_data.info(idx).textdist = [3 3];
qp_data.info(idx).lastax = '';
qp_data.info(idx).lut = repmat([0:.01:1]',[1 3]);
qp_data.info(idx).lut_nan = [1 1 1];
qp_data.info(idx).panels = {'-'};
qp_data.info(idx).panelextent = { };
qp_data.info(idx).panel = '-';

unix(sprintf('qpclient %s', fn));

if nargout<1
  clear fn
end
