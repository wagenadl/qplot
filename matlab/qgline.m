function qgline(varargin)
% QGLINE - Generalized line drawing
%   QGLINE(ptspec1, ptspec2, ...).
%   A PTSPEC is a cell array containing a sequence of commands from the 
%   following list:
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
%      AT id          - Absolute paper coordinates of location set by AT.
%      ATX id         - Absolute paper x-coordinate of location set by AT.
%      ATY id         - Absolute paper y-coordinate of location set by AT.
%
%   For instance,
%
%       qgline({'absdata', 0, 1, 'relpaper', 5, 0}, ...
%              {'absdata', 2, 3, 'relpaper', 0, 7})
%
%   draws a line from 5 pt to the right of the point (0,1) in the graph to
%   7 pt below the point (2, 3) in the graph. (Note that paper y-coordinates
%   increase toward the bottom of the graph while data y-coordinates increase
%   toward the top.)
%
%   Note: The rather cumbersome syntax of QGLINE makes QLINE and QPLOT more
%   attractive for general usage. The same applies to QGAREA versus QAREA 
%   and QPATCH. See also QSHIFTEDLINE and QGLINE2.

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

qp_gline('gline', varargin{:});
