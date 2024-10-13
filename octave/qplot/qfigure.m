function fn = qfigure(fn, w, h)
% QFIGURE - Open a QPlot figure
%    QFIGURE(fn, w, h) opens a new QPLOT figure with given filename and size
%    in inches. If H is omitted, H defaults to 3/4 W. If W is also omitted,
%    W defaults to 5 inches.
%    fn = QFIGURE(w, h) opens a new QPlot figure of given size (in inches) with
%    a temporary filename.

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

fn = qp_ensureqpt(fn);

THRESH = 36; % If attempting to make >36", treat dimensions as points

if w>THRESH || h>THRESH
  w=w/72;
  h=h/72;
end

idx = find(strcmp(fn, qp_data.fns));
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
qp_reset(idx);

qunix(sprintf('qpclient %s', fn));

if nargout<1
  clear fn
end

qp_flush(fd);

