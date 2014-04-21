function qgimage(dxywh, pxywh, img)
% QGIMAGE - Place an image with data and paper coordinates
%   QGIMAGE(xywh_data, xywh_paper, img) places the image on a location in
%   the graph specified by both data coordinates and image coordinates.
%   For example: QGIMAGE([5 5 0 0],[0 0 36 72],img) creates an image of 0.5x1"
%   at data location (5,5). QGIMAGE([5 nan 0 5],[0 36 72 0],img) creates an 
%   image 1" wide, 5 data units high, at x=5, 1" below the top of the graph.
%   Etc.

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

[Y X C] = size(img);
if C==1 || C==3 || C==4
  ; % ok
else
  error('Image must have 1, 3, or 4 planes');
end

if isempty(dxywh)
  dxywh = [ nan nan 0 0];
end
if isempty(pxywh)
  pxywh = [ 0 0 0 0 ];
end

if length(dxywh)~=4 || length(pxywh)~=4
  error('Position must given as [x y w h]');
end 

str = 'image [ ';
str = [ str sprintf('%g ', dxywh) ];
str = [ str ' ] [ ' ];
str = [ str sprintf('%g ', pxywh) ];
str = [ str sprintf(' ] [ %i %i %i ] *uc%i\n', X, Y, C, X*Y*C) ];

img = permute(img,[3 2 1]);
if ~isa(img, 'uint8')
  img = uint8(floor(255*img+.5));
end

fd = qp_fd(1);
fprintf(fd,'%s', str);
fwrite(fd, img, 'uint8');
qp_flush(fd);

