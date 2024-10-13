function qclose(fn)
% QCLOSE - Close a QPlot window
%    QCLOSE closes the current window.
%    QCLOSE(filename) closes the named window.
%    QCLOSE('all') closes all windows.
global qp_data
qp_ensure;

% QPlot - Publication quality 2D graphs with dual coordinate systems
% Copyright (C) 2014  Daniel Wagenaar
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

fn = qp_ensureqpt(fn);
idx = find(strcmp(fn, qp_data.fns));
if isempty(idx)
  warning('No such window');
  return;
end

if qp_data.info(idx).fd>=0
  fd = qp_data.info(idx).fd;
  qp_data.info(idx).fd=-1;
  qunix(sprintf('qpclose %s', fn));
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
