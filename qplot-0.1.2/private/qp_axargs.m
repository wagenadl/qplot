function [xlim, xpts, lbls, ttl] = qp_axargs(err, varargin)
% QP_AXARGS - Regularize arguments for qxaxis and qyaxis

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

if nargin<2
  error(err);
end
xlim = varargin{1};
varargin=varargin(2:end);

if isempty(xlim)
  xlim=[nan nan];
end
if ~isa(xlim, 'function_handle') && ~isnvector(xlim)
  error(err);
end

if length(xlim)~=2
  if isa(xlim, 'function_handle')
    if isempty(varargin)
      error(err);
    else
      xpts = xlim(varargin{1});
    end
  else
    xpts = xlim;
  end
  xlim = [xpts(1) xpts(end)];
elseif ~isempty(varargin) && isnvector(varargin{1})
  xpts = varargin{1};
  varargin = varargin(2:end);
elseif ~isempty(varargin) && isnumeric(varargin{1}) && isempty(varargin{1})
  xpts = [];
  varargin = varargin(2:end);
elseif length(varargin)>=2 && isa(varargin{1}, 'function_handle') ...
      && isnvector(varargin{2})
  xpts = varargin{1}(varargin{2});
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
  elseif isa(varargin{1}, 'function_handle') && ~isempty(xpts)
    lbls = cell(size(xpts));
    for k=1:length(xpts)
      lb = varargin{1}(xpts(k));
      if isnumeric(lb)
	lb = qp_format(lb);
	lbls{k} = lb{1};
      else
	lbls{k} = lb;
      end
    end
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

