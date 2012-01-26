function str = qp_id(n)
str = '';
n=n-1;
while n>0 || isempty(str)
  x = mod(n,26);
  n = div(n,26);
  str = [ char(x+'A') str ];
end
