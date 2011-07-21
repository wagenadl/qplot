function qcolorbar(xywh, lut, varargin)
% QCOLORBAR - Adds a colorbar to the figure
%    QCOLORBAR(xywh, lut) represents the LUT at location XYWH.
%    QCOLORBAR(xywh, lut, lblloc) adds labels. The first and last labels
%    go at the ends of the colorbar.
%    QCOLORBAR(xywh, lut, clim, lblloc), where CLIM is a two-element vector
%    explicitly specifies the ends if ticks at the ends are not desired.
%    QCOLORBAR(..., labels) specifies the text of the labels.
%    QCOLORBAR(..., caption) adds a caption.

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
    if length(lblloc)==2 & isnvector(varargin{1})
      lblloc = varargin{1};
      lbltxt = lblloc;
      varargin = varargin(2:end);
      if length(lblloc)==2
        % This could be a mistake: Should we interpret as (lblloc, clbl) rather 
        % than (clim, lblloc)?
        if isempty(varargin) | ischar(varargin{1})
	  lblloc = clim;
        end	
      end
    end
  end
  
  if ~isempty(varargin)
    if iscell(varargin{1}) | isnvector(varargin{1})
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