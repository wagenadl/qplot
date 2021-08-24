function qclf 
% QCLF - Clear current QPlot figure
%   QCLF clears the current QPlot figure. 
global qp_data
fd = qp_fd(1);
fn = qp_data.curfn;
fclose(fd);
fd = fopen(fn, 'r');
l0 = fgets(fd);
fclose(fd);
fd = fopen(fn, 'w');
fprintf(fd, '%s', l0);
idx = strmatch(fn, qp_data.fns, 'exact');
qp_data.info(idx).fd = fd;

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

qp_reset(idx);

qp_flush(fd);

