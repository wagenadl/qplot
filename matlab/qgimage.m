function qgimage(dxywh, pxywh, img)
% QGIMAGE - Place an image with data and paper coordinates
%   QGIMAGE(xywh_data, xywh_paper, img) places the image on a location in
%   the graph specified by both data coordinates and image coordinates.
%   For example: QGIMAGE([5 5 0 0],[0 0 36 72],img) creates an image of 0.5x1"
%   at data location (5,5). QGIMAGE([5 nan 0 5],[0 36 72 0],img) creates an 
%   image 1" wide, 5 data units high, at x=5, 1" below the top of the graph.
%   Etc.

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

