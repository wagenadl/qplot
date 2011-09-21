function n = qp_revid(str)
n=0;
while ~isempty(str)
  n = 26*n + str(1)-'A';
  str=str(2:end);
end
n = n+1;