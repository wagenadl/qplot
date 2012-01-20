qfigure('eg_axis.qpt', 5, 3.5);

xx = [-pi:.001:pi]*3;

qpen b 1
qplot(xx, cos(xx))
qpen r 1
qplot(xx, sin(xx))

lbl = '-3π -2π -π 0 π 2π 3π';
lbls={};
while ~isempty(lbl)
  [lbls{end+1}, lbl] = strtok(lbl);
end

qpen k 0
qxaxis(-1.1, pi*[-3:3], lbls, 'Angle (rad)');
qyaxis(-3.1*pi, [-1:1]);

qticklen 2.5
qmticks([-.5 .5])
qticklen 1.5
qmticks([-1:.1:1])

qtitle 'Cosine and sine'
qylim -1 1.2

qfudge
