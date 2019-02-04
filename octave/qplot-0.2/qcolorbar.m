function qcolorbar(xywh, lut, varargin)
% QCOLORBAR - Adds a colorbar to the figure
%    QCOLORBAR(xywh, lut) represents the LUT at location XYWH.
%    QCOLORBAR(xywh, lut, tickvals) adds ticks. The first and last labels
%    go at the ends of the colorbar.
%    QCOLORBAR(xywh, lut, endvals, tickvals), where ENDVALS is a two-element
%    vector explicitly specifies the values at the ends of the colorbar.
%    QCOLORBAR(..., ticklabels) specifies the text of the labels.
%    QCOLORBAR(..., caption) adds a caption.
%    If LUT is given as [], QLUT is used to query the figure.
%
%    This command is deprecated. Use QCBAR and QCAXIS instead.

if nargin<2
  lut=[];
end
if isempty(lut)
  lut = qlut;
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

if isempty(varargin)
  key=0;
else
  key=1;
  lblloc = varargin{1};
  varargin = varargin(2:end);
  
  clim = [lblloc(1) lblloc(end)];
  lbltxt = lblloc;
  caption = '';
  if ~isempty(varargin)
    if length(lblloc)==2 && isnvector(varargin{1})
      lblloc = varargin{1};
      lbltxt = lblloc;
      varargin = varargin(2:end);
      if length(lblloc)==2
        % This could be a mistake: Should we interpret as (lblloc, clbl) rather 
        % than (clim, lblloc)?
        if isempty(varargin) || ischar(varargin{1})
	  lblloc = clim;
        end	
      end
    end
  end
  
  if ~isempty(varargin)
    if iscell(varargin{1}) || isnvector(varargin{1})
      lbltxt = varargin{1};
      varargin = varargin(2:end);
    end
  end
  
  if ~isempty(varargin)
    if ischar(varargin{1})
      caption = varargin{1};
      varargin = varargin(2:end);
    end
  end
  
  if ~isempty(varargin)
    error('qcolorbar: syntax error');
  end
  if length(lblloc) ~= length(lbltxt)
    error('qcolorbar: mismatch b/w ticks and labels');
  end
end

C = size(lut,1);
qimage(xywh, reshape(flipud(lut), [C 1 3]));

if key
  [lbl, ttl] = qtextdist;
  if lbl<0
    x0 = xywh(1) + xywh(3);
  else
    x0 = xywh(1);
  end
  
  qyaxis(x0, xywh(2)+[0 xywh(4)], ...
      (lblloc-clim(1))/(clim(2)-clim(1))*xywh(4) + xywh(2), ...
      lbltxt, caption);
end