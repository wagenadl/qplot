function qerrorbar(xx, yy, dy, varargin)
% QERRORBAR - Draw error bars
%    QERRORBAR(xx, yy, dy) plots error bars at (XX,YY+-DY).
%    Normally, XX, YY, and DY have the same shape. However, it is permissible
%    for DY to be shaped Nx2, in which case lower and upper error bounds
%    are different. (DY should always be positive).
%    QERRORBAR(xx, yy, dy, w) adorns the error bars with horizontal lines of
%    given width (W in points).
%    QERRORBAR(..., 'up') only plots upward; QERRORBAR(..., 'down') only plots
%    downward.

dir = 'both';
w = 0;
while ~isempty(varargin)
  if ischar(varargin{1})
    dir = varargin{1};
  else
    w = varargin{1};
  end
  varargin=varargin(2:end);
end

xx = xx(:);
yy = yy(:);
N = length(xx);
if prod(size(dy))==2*N
  dy_dn = -dy(:,1);
  dy_up = dy(:,2);
else
  dy_up = dy(:);
  dy_dn = -dy(:);
end

switch dir
  case 'both'
    for n=1:N
      qplot(xx(n)+[0 0],yy(n)+[dy_dn(n) dy_up(n)]);
    end
  case 'up'
    for n=1:N
      qplot(xx(n)+[0 0],yy(n)+[0 dy_up(n)]);
    end
  case 'down'
    for n=1:N
      qplot(xx(n)+[0 0],yy(n)+[dy_dn(n) 0]);
    end
  otherwise
    error([ 'Bad direction name: ' dir]);
end

if w>0 
  if ~strcmp(dir, 'down')
    % Draw top ticks
    for n=1:N
      qat(xx(n), yy(n)+dy_up(n));
      qline([-1 1]*w/2,[0 0]);
    end
  end
  if ~strcmp(dir, 'up')
    % Draw down ticks
    for n=1:N
      qat(xx(n), yy(n)+dy_dn(n));
      qline([-1 1]*w/2,[0 0]);
    end
  end
end

     