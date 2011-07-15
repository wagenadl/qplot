function n = qp_revid(str)
n=0;
while ~isempty(str)
  n = 26*n + str(1)-'A'+1;
  str=str(2:end);
end
