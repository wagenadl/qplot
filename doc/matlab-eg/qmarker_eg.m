qfigure('qmarker', 3, 3);

sty = { 'open', 'solid', 'brush' };
shp = '+x-|osd<>^vph';

qpen k
qbrush r

for x=1:length(shp)
  for y=1:length(sty)

    qmarker(shp(x), sty{y});
    
    qmark(x, y);
  end
end

qshrink
