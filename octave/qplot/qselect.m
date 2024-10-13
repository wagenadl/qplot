function qselect(fn)
% QSELECT - Select a QPlot figure by name
%    QSELECT(fn) makes the named QPlot figure current

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

global qp_data;
qp_ensure;

dotidx = find(fn=='.');
slashidx = find(fn=='/');
if ~isempty(slashidx)
  dotidx = dotidx(dotidx>slashidx(end));
end
if isempty(dotidx)
  fn = [ fn '.qpt' ];
end

idx = find(strcmp(fn, qp_data.fns));

if isempty(idx)
  % Let's see if we can match on partial file names
  F = length(qp_data.fns);
  leaf=cell(F,1);
  for f=1:F
    leaf{f} = basename(qp_data.fns{f});
  end
  idx = find(strcmp(fn, leaf));
end

if isempty(idx)
  for f=1:F
    idx = find(leaf{f}=='.');
    if ~isempty(idx)
      leaf{f} = leaf{f}(1:idx(end)-1);
    end
  end
  idx = find(strcmp(fn, leaf));
end

if isempty(idx)
  idx = find(strncmp(fn, leaf, length(fn)));  
end

if isempty(idx)
  error('No such figure');
elseif length(idx)>1
  error('Ambiguous figure name');
end

qp_data.curfn = qp_data.fns{idx};

qunix(sprintf('touch %s', qp_data.curfn)); % Bring to front
