function str = qp_id(n)
str = '';
while n>0
  x = mod(n,26);
  n = div(n,26);
  str = [ char(x-1+'A') str ];
end
