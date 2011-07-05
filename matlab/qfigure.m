function fn = qfigure(fn, w, h)
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

idx = strmatch(fn, qp_data.fn, 'exact');
if ~isempty(idx)
  if qp_data.fd(idx)>=0
    fclose(qp_data.fd(idx));
    qp_data.fd(idx)=-1;
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
  qp_data.fn{end+1} = fn;
  qp_data.fd(end+1) = fd;
  qp_data.istemp(end+1) = istmp;
  qp_data.extent{end+1} = [0 0 w h];

  qp_data.ticklen{end+1} = 3;
  qp_data.textdist{end+1} = [3 3];
  qp_data.lastax{end+1} = '';
  qp_data.lut{end+1} = repmat([0:.01:1]',[1 3]);
else
  qp_data.fd(idx) = fd;
  qp_data.istemp(idx) = istmp;
  qp_data.extent{idx} = [0 0 w h];
  qp_data.ticklen{idx} = 3;
  qp_data.textdist{idx} = [3 3];
  qp_data.lastax{idx} = '';
  qp_data.lut{idx} = repmat([0:.01:1]',[1 3]);
end

unix(sprintf('qpclient %s', fn));

if nargout<1
  clear fn
end
