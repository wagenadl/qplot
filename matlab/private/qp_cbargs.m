function [dh,dx,dy] = qp_cbargs(dflt, varargin)

switch length(varargin)
case 0
  dh = dflt;
  dx = 0;
  dy = 0;
case 1
  dh = varargin{1};
  dx = 0;
  dy = 0;
case 2
  dx = varargin{1};
  dy = varargin{2};
  dh = dflt;
case 3
  dx = varargin{1};
  dy = varargin{2};
  dh = varargin{3};
otherwise
  error('QCBAR: syntax error');
end
