function qp_gline(cmd, varargin)

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

args = varargin;
if length(args)==1 && iscell(args) && iscell(args{1})
  args = args{:};
end

for k=1:length(args)
  cmd = [ cmd ' (' ];
  for q=1:length(args{k})
    x = args{k}{q};
    if ischar(x)
      cmd = [ cmd ' ' x ];
    else
      cmd = [ cmd ' ' sprintf('%g', x) ];
    end
  end
  cmd = [ cmd ' )' ];
end

fd = qp_fd(1);
fprintf(fd, '%s\n', cmd);
qp_flush(fd);

