function qfont(varargin)
% QFONT - Select font 
%    QFONT family [bold] [italic] size  selects a new font for QPlot.
%    The default font is Helvetica at 10 points.

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

fd = qp_fd(1);

if nargin<2 || nargin>4
  qfont_usage;
end
if isnscalar(varargin{end})
  varargin{end} = sprintf('%g', varargin{end});
end
for k=1:nargin
  if ~ischar(varargin{k})
    qfont_usage;
  end
end
for k=2:nargin-1
  if ~any(strcmp(tolower(varargin{k}), strtoks('bold italic')))
    qfont_usage;
  end
end

str = 'font';
for k=1:nargin
  str = [ str ' ' varargin{k} ];
end
fprintf(fd, '%s\n', str);

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function str = tolower(str)
for l=1:length(str)
  if str(l)>='A' && str(l)<='Z'
    str(l) = str(l) + 32;
  end
end


function qfont_usage()
  error('Usage: qfont family [bold] [italic] size');


