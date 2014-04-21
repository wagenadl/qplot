function qalign(varargin)
% QALIGN - Set alignment for following text
%   QALIGN left|right|center|top|bottom|middle|base sets alignment for
%   subsequent QTEXT commands.
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

if nargin<1
  error('Usage: qalign left|right|center|top|bottom|middle|base ...');
end

txt = 'align';
for k=1:nargin
  if isempty(strmatch(varargin{k}, ...
	strtoks('left right center top bottom middle base')))
    error('Usage: qalign left|right|center|top|bottom|middle|base ...');
  end
  txt = [ txt ' ' varargin{k} ];
end

fprintf(fd, '%s\n', txt);


qp_flush(fd);

