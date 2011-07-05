function qclose(fn)
global qp_data
qp_ensure;

if nargin==0
  fn = qp_data.curfn;
elseif strcmp(fn, 'all')
  fns = qp_data.fn;
  for k=1:length(fns)
    try
      qclose(fns{k});
    catch
      fprintf(1,'Note: %s\n', lasterr);
    end
  end
  return
end

if isempty(fn)
  warning('No open windows');
  return;
end

idx = strmatch(fn, qp_data.fn, 'exact');
if isempty(idx)
  warning('No such window');
  return;
end

if qp_data.fd(idx)>=0
  fd = qp_data.fd(idx);
  qp_data.fd(idx)=-1;
  unix(sprintf('qpclose %s', fn));
  if qp_data.istemp(idx)
    delete(fn);
  end

  keep = [1:length(qp_data.fn)];
  keep(idx) = [];
  qp_data.fn = qp_data.fn(keep);
  qp_data.fd = qp_data.fd(keep);
  qp_data.istemp = qp_data.istemp(keep);

  fclose(fd);
end

if strcmp(fn, qp_data.curfn)
  qp_data.curfn = '';
  for k=1:length(qp_data.fn)
    if qp_data.fd(k)>=0
      qp_data.curfn = qp_data.fn{k};
      break;
    end
  end
end
