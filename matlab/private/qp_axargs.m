function [xlim, xpts, lbls, ttl] = qp_axargs(err, varargin)
% QP_AXARGS - Regularize arguments for qxaxis and qyaxis

if nargin<2
  error(err);
end
xlim = varargin{1};
varargin=varargin(2:end);

if isempty(xlim)
  xlim=[nan nan];
end
if ~isnvector(xlim)
  error(err);
end

if length(xlim)~=2
  xpts = xlim;
  xlim = [xlim(1) xlim(end)];
elseif ~isempty(varargin) && isnvector(varargin{1})
  xpts = varargin{1};
  varargin = varargin(2:end);
elseif ~isempty(varargin) && isnumeric(varargin{1}) && isempty(varargin{1})
  xpts = [];
  varargin = varargin(2:end);
else
  xpts = xlim;
end

if length(xlim)~=2
  error(err);
end

lbls = qp_format(xpts);
if ~isempty(varargin)
  if isnumeric(varargin{1})
    lbls = qp_format(varargin{1});
    varargin = varargin(2:end);
  elseif iscell(varargin{1})
    lbls = varargin{1};
    varargin = varargin(2:end);
  end
end

ttl = '';
if ~isempty(varargin)
  if ischar(varargin{1})
    ttl = varargin{1};
    varargin = varargin(2:end);
  end
end

if isempty(lbls)
  ;
elseif length(lbls) ~= length(xpts)
  error(err);
end

