function qprint(nowait)
% QPRINT - Print current QPlot figure to the default printer
%    QPRINT prints the current QPlot figure using qplotml and lpr after
%    waiting for confirmation from the user.
%    QPRINT(1) does not wait.

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

if nargin<1
  nowait=0;
end

qp_ensure;
global qp_data;
ifn = qp_data.curfn;
if isempty(ifn)
  error('No window');
end
qselect(ifn);

ofn = sprintf('%s.ps', tempname);

s = qunix(sprintf('qplotml %s %s', ifn, ofn));
if s
  error('qplot failed');
end

if ~nowait
  input('Press Enter to print to lpr, or Ctrl-C to cancel...');
end
unix(sprintf('lpr %s', ofn));
fprintf(1,'\nPostscript file sent to printer.\n');

delete(ofn);
