function [lut, nanc] = qlut(lut, nanc) 
% QLUT - Set lookup table for future QIMSC.
%    QLUT(lut) where LUT is Nx3 sets a new lookup table for QIMSC.
%    QLUT(lut, nanc) where NANC is 1x3 (or 3x1) sets a special color to use
%    for NaN values. (The default is white.)
%    [lut, nanc] = QLUT returns current values.

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
  nanc=[1 1 1];
end

idx = qp_idx;
global qp_data;

if nargin>=1
  qp_data.info(idx).lut = lut;
  qp_data.info(idx).lut_nan = nanc;
end

clear nanc lut

if nargout>=1
  lut = qp_data.info(idx).lut;
end
if nargout>=2
  nanc = qp_data.info(idx).nanc;
end


