function qlegopt(varargin)
% QLEGOPT - Set options for QLEGEND and friends
%    QLEGOPT(k1, v1, ...) specifies options for legend rendering.
%    Options are specified as key, value pairs. Keys are:
%      x0 - x position of left edge of legend, in data coordinates
%      y0 - y position of middle of top legend element, in data coordinates
%      skip - baselineskip (in points) between elements
%      height - height (in points) of rendered patches
%      width - width (in points) of rendered lines and patches
%      indent - space between rendered samples and following text
%      color - color for following text
%      drop - vertical distance between middle of samples and text baseline
%      dx, dy - additional horizontal and vertical displaced, in points
%    All of sensible defaults, except X0 and Y0, which default to (0, 0).
%    Legend elements are automatically rendered one below the other starting
%    at Y0.
kw = 'x0 y0 skip height width indent color drop dx dy';
opt = getopt(kw, varargin);
idx = qp_idx(1);
global qp_data;
if ~isfield(qp_data.info(idx),'legopt') || isempty(qp_data.info(idx).legopt)
  qp_data.info(idx).legopt.x0 = 0;
  qp_data.info(idx).legopt.y0 = 0;
  qp_data.info(idx).legopt.dx = 0;
  qp_data.info(idx).legopt.dy = 0;
  qp_data.info(idx).legopt.skip = 15;
  qp_data.info(idx).legopt.n = 0;
  qp_data.info(idx).legopt.drop = 3;
  qp_data.info(idx).legopt.height = 9;
  qp_data.info(idx).legopt.width = 18;
  qp_data.info(idx).legopt.indent = 9;
  qp_data.info(idx).legopt.color = 'k';
end

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

kw = strtoks(kw);

for a=1:length(kw)
  if ~isempty(opt.(kw{a}))
    qp_data.info(idx).legopt.(kw{a}) = opt.(kw{a});
    if strcmp(kw{a}, 'y0')
      qp_data.info(idx).legopt.n = 0;
    end
  end
end

  