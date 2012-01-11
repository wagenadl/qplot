function yes=isnvector(x)
% ISNVECTOR  True if array is a numeric vector.
%    ISNVECTOR(x) returns True if X is an 1xN or Nx1 numeric array, 
%    False if not.
yes = isnumeric(x) & length(size(x))==2 & sum(size(x))==max(size(x))+1;
