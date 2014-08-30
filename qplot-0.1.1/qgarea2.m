function qgarea2(varargin)
% QGAREA2 - Generalized area drawing
%   QGAREA(cmd1, args1, cmd2, args2, ...) specifies a area in mixed
%   data and paper coordinates.
%   Commands are given as (lower case) strings and are followed by
%   zero or more vector arguments, depending on the command. All vectors
%   must be the same length. However, scalars will be automatically converted
%   to vectors of the appropriate length.
%   Commands with their arguments are:
%
%      ABSDATA x y    - Absolute data coordinates 
%      RELDATA dx dy  - Relative data coordinates 
%      ABSPAPER x y   - Absolute paper coordinates (in pt)
%      RELPAPER dx dy - Relative data coordinates (in pt)
%      ROTDATA xi eta - Rotate by atan2(eta, xi) in data space.
%                       (This affects subsequent relative positioning.) 
%      ROTPAPER phi   - Rotate by phi radians. (This affects subsequent 
%                       relative positioning.) 
%      RETRACT l      - Retract preceding and following segments by L pt.
%      RETRACT l1 l2  - Retract preceding and following segments by L1 and 
%                       L2 pt respectively.
%
%   Note: The rather cumbersome syntax of QGAREA2 makes QAREA and QPATCH more
%   attractive for general usage. See also QGLINE2 and QGAREA.

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

qp_gline2('garea', varargin{:});
