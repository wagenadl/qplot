qfigure('qline', 3, 3);

xx=[-pi:.1:pi];
yy=sin(xx);

qplot(xx, yy);

for n=4:5:length(xx)-1
  qat(xx(n), yy(n), xx(n+1)-xx(n), yy(n+1)-yy(n));
  qline([0 0],[-5 5]);
end
