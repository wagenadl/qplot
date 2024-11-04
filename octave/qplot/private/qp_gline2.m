function qp_gline2(cmd, varargin)

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

% We will convert to ptspecs for qgline

ptspec = {};
N = []; % Number of points, currently unknown

args = varargin;
if length(args)==1 && iscell(args)
  args = args{:};
end
K = length(args);
k = 1; % index into args
while k<=K
  subcmd = args{k};
  if ~ischar(subcmd)
    error('Expecting a command');
  end
  narg = [];
  if any(strcmp(tolower(subcmd), strtoks('absdata reldata abspaper relpaper')))
    narg = 2;
  elseif any(strcmp(tolower(subcmd), strtoks('rotdata rotpaper')))
    narg = 1;
  elseif strcmp(tolower(subcmd), 'retract')
    if k+2 <= K && isnvector(args{k+2})
      narg = 2;
    else
      narg = 1;
    end
  end
  if isempty(narg)
    error(sprintf('Unknown command: %s', subcmd));
  elseif k+narg > K
    error(sprintf('Missing arguments to %s', subcmd));
  else
    for i=1:narg
      if ~isnvector(args{k+i})
	error(sprintf('Wrong arguments to %s', subcmd));
      end
    end
  end

  if isempty(N) && narg>0 
    N = length(args{k+1});
    ptspec = cell(N, 1);
    for n=1:N
      ptspec{n} = {};
    end
  end
  
  for i=1:narg
    if isscalar(args{k+i})
      args{k+i} = repmat(args{k+i}, N, 1);
    end
  end
    
  for n=1:N
    ptspec{n}{end+1} = subcmd;
    for i=1:narg
      ptspec{n}{end+1} = args{k+i}(n);
    end
  end

  k = k + 1 + narg;
end

qp_gline(cmd, ptspec);
