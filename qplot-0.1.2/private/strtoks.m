function y=strtoks(x,s,needle)
% y = STRTOKS(x) returns a cell array of strings consisting of the
% space delimited parts of X.
% y = STRTOKS(x,s) uses S instead of space.
% y = STRTOKS(...,needle) only returns those tokens that contain NEEDLE
% as a substring.

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
  s=[];
end

if iscell(x)
  y=x;
  return
end

n=1;
y=cell(0,1);
while length(x)>0
  if ~isempty(s)
    [ z, x ] = strtok(x,sprintf(s));
  else
    [ z, x ] = strtok(x);
  end
  if length(z)
    y{n}=z;
    n=n+1;
  end
end

if nargin>=3
  z=cell(0,1);
  m=1;
  for n=1:length(y)
    if strfind(y{n},needle)
      z{m}=y{n};
      m=m+1;
    end
  end
  y=z;
end
