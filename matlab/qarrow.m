function qarrow(l, w, dl, dimple, dw)
% QARROW - Draw an arrowhead
%   QARROW draws an arrow head pointing to the current anchor set by QAT.
%   QARROW(l, w) specifies length and (full) width of the arrow head
%   These are specified in points, and default to L=8, W=5.
%   QARROW(l, w, dl) specifies that the arrow is to be displaced from the
%   anchor by a distance DL along the arrow's axis.
%   QARROW(l, w, dl, dimple) specifies that the back of the arrow head is
%   indented by DIMPLE points.
%   QARROW(l, w, dl, dimple, dw) specifies that the arrow is to be displaced
%   from the anchor by DW points in the orthogonal direction of the arrow's
%   axis.

if nargin<1 || isempty(l)
  l = 8;
end
if nargin<2 || isempty(w)
  w = 0.6 * l;
end
if nargin<3 || isempty(dl)
  dl = 0;
end
if nargin<4 || isempty(dimple)
  dimple = 0;
end
if nargin<5 || isempty(dw)
  dw = 0;
end

qarea([0 -l dimple-l -l]-dl, [0 w 0 -w]/2+dw);
