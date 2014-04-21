function qpen(varargin)
% QPEN - Selects a new pen for QPlot
%    QPEN id | join | cap | pattern | color | width | -alpha | 'none'
%    selects a new pen.
%    ID must be a single capital letter
%    JOIN must be one of: miterjoin beveljoin roundjoin
%    CAP must be one of: flatcap squarecap roundcap
%    PATTERN must be one of: solid dash dot none
%       dash may optionally be followed by a vector of stroke and space lengths
%       dot may optionally be followed by a vector of space lengths
%    COLOR may be a single character matlab color, or a 3- or 6-digit RGB
%    specification. 
%    WIDTH is linewidth in points, or 0 for hairline.
%    ALPHA specifies transparency between 0 and 1.
fd = qp_fd(1);

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

cmd = 'pen';

n=1;
while n<=nargin
  a = varargin{n};
  if ischar(a)
    if length(a)==1 && a>='A' && a<='Z' && n==1
      cmd = [ cmd ' ' a ];
    elseif strmatch(a, strtoks('miterjoin beveljoin roundjoin flatcap squarecap roundcap solid none'), 'exact')
      cmd = [ cmd ' ' a ];
    elseif strmatch(a, strtoks('dash dot'), 'exact')
      cmd = [ cmd ' ' a ];
      vec=[];
      while n<nargin
	if isnvector(varargin{n+1})
	  vec = [ vec; varargin{n+1}(:); ];
	elseif ischar(varargin{n+1}) && ~isnan(str2double(varargin{n+1}))
	  vec = [ vec; str2double(varargin{n+1}) ];
	else
	  break;
	end
	n=n+1;
      end
      if isempty(vec)
	vec = 3;
      end
      cmd = [ cmd ' [' sprintf(' %g', vec) ' ]'];
    elseif ~isempty(qp_mapcolor(a))
      ; % This is a good color
      cmd = [ cmd ' ' qp_mapcolor(a) ];
    elseif ~isnan(str2double(a)) 
      % This is a number
      if length(a)==3  && all(a>='0') && all(a<='9')
	% This is a three-digit color
	cmd = [ cmd ' ' sprintf('#%02x%02x%02x', ...
	    floor(255.999*atoi(a(1))/9), ...
	    floor(255.999*atoi(a(2))/9), ...
	    floor(255.999*atoi(a(3))/9))];
      elseif length(a)==6 && all(a>='0') && all(a<='9')
	% This is a six-digit color
	cmd = [ cmd ' ' sprintf('#%02x%02x%02x', ...
	    floor(255.999*atoi(a(1:2))/99), ...
	    floor(255.999*atoi(a(3:4))/99), ...
	    floor(255.999*atoi(a(5:6))/99))];
      else
	; % This is pen width
	cmd = [ cmd ' ' a ];
      end
    else
      error([ 'Cannot interpret ' a ' as an argument for qpen' ]);
    end
  elseif isnscalar(a) && isreal(a)
    ; % This is a pen width
    cmd = [ cmd ' ' sprintf('%g', a)];
  elseif isnvector(a) && isreal(a) && length(a)==3
    % This is a color
    cmd = [ cmd ' ' sprintf('#%02x%02x%02x', ...
	  floor(255.999*a))];
  else
    error([ 'Cannot interpret ' disp(a) ' as an argument for qpen' ]);
  end
  n=n+1;
end

fprintf(fd, '%s\n', cmd);



