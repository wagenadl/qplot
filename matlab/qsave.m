function qsave(ofn, reso)
% QSAVE - Saves a qplot figure
%    QSAVE(ofn) saves the current qplot figure to the named file.
%    QSAVE(ext), where EXT is just a filename extension (without the dot),
%    uses the name of the current figure.
%    QSAVE(ofn, reso) specifies bitmap resolution for png/jpeg output.
%    QSAVE without arguments saves to pdf.

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

if nargin<2
  reso = [];
end

qp_ensure;
global qp_data;
ifn = qp_data.curfn;
if isempty(ifn)
  error('No window');
end

if nargin<1
  ofn='pdf';
end

if isempty(find(ofn=='.'))
  % Extension only
  idx = find(ifn=='.');
  ofn = [ifn(1:idx(end)) ofn];
end

if ischar(reso)
  reso = atoi(reso);
end

if isempty(reso)
  cmd = sprintf('qplotml %s %s', ifn, ofn);
else
  cmd = sprintf('qplotml -r%i %s %s', floor(reso), ifn, ofn);
end

s = unix(cmd);
if s
  error('qplot failed');
end


