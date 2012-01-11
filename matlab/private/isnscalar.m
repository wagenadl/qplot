function yes=isnscalar(x)
% ISNSCALAR  True if array is a numeric scalar.
%   ISNSCALAR(x) returns True if X is a scalar numeric array, False if not.

yes = isnumeric(x) & prod(size(x))==1;