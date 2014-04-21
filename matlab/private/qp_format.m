function txt=qp_format(xx)
% txt = QP_FORMAT(xx) performs num2str for a matrix of numbers.
% Each input value is stored in a cell of the output.

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

idx = qp_idx;
global qp_data;
fmt = qp_data.info(idx).numfmt;

[X Y]=size(xx);
txt=cell(X,Y);

if isempty(fmt)
  for x=1:X
    for y=1:Y
      txt{x,y} = num2str(xx(x,y));
    end
  end
else
  for x=1:X
    for y=1:Y
      txt{x,y} = sprintf(fmt, xx(x,y));
    end
  end
end

