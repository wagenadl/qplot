function qselect(fn)
% QSELECT - Select a QPLOT figure by name
%    QSELECT(fn) makes the names QPLOT figure current

global qp_data;
qp_ensure;

idx = strmatch(fn, qp_data.fns, 'exact');

if isempty(idx)
  % Let's see if we can match on partial file names
  F = length(qp_data.fns);
  leaf=cell(F,1);
  for f=1:F
    leaf{f} = basename(qp_data.fns{f});
  end
  idx = strmatch(fn, leaf, 'exact');  
end

if isempty(idx)
  for f=1:F
    idx = find(leaf{f}=='.');
    if ~isempty(idx)
      leaf{f} = leaf{f}(1:idx(end)-1);
    end
  end
  idx = strmatch(fn, leaf, 'exact');  
end

if isempty(idx)
  idx = strmatch(fn, leaf);  
end

if isempty(idx)
  error('No such figure');
elseif length(idx)>1
  error('Ambiguous figure name');
end

qp_data.curfn = qp_data.fns{idx};

unix(sprintf('touch %s', qp_data.curfn)); % Bring to front
