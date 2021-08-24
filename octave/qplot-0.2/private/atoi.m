function x=atoi(s)
% ATOI  Extract an integer from a string
%   x = ATOI(s) is like the libc version, except in that it returns nan if
%   S does not start with a digit (or -).
%   Exception: spaces are removed from beginning

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

while ~isempty(s) && (s(1)==' ' || s(1)=='	')
  s=s(2:end);
end

if length(s)==0
  x=nan;
  return;
end
  
if s(1)=='-'
  sgn=-1;
  s=s(2:end);
elseif s(1)=='+'
  sgn=1;
  s=s(2:end);
else
  sgn=1;
end

if length(s)==0 
  x=nan;
  return;
end

ok = isdigit(s);
idx=find(~ok);
if ~isempty(idx)
  s=s(1:idx(1)-1);
end

x=str2num(s) * sgn;

if isempty(x)
  x=nan;
end
