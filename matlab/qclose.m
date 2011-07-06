function qclose(fn)
global qp_data
qp_ensure;

if nargin==0
  fn = qp_data.curfn;
elseif strcmp(fn, 'all')
  fns = qp_data.fns;
  for k=1:length(fns)
    try
      qclose(fns{k});
    catch
      fprintf(1,'Note: %s\n', lasterr);
    end
  end
  qp_data = [];
  return
end

if isempty(fn)
  warning('No open windows');
  return;
end

idx = strmatch(fn, qp_data.fns, 'exact');
if isempty(idx)
  warning('No such window');
  return;
end

if qp_data.info(idx).fd>=0
  fd = qp_data.info(idx).fd;
  qp_data.info(idx).fd=-1;
  unix(sprintf('qpclose %s', fn));
  if qp_data.info(idx).istemp
    delete(fn);
  end

  keep = [1:length(qp_data.fns)];
  keep(idx) = [];
  qp_data.info = qp_data.info(keep);
  qp_data.fns = qp_data.fns(keep);

  fclose(fd);
end

if strcmp(fn, qp_data.curfn)
  qp_data.curfn = '';
  for k=1:length(qp_data.fns)
    if qp_data.info(k).fd>=0
      qp_data.curfn = qp_data.fns{k};
      break;
    end
  end
end
