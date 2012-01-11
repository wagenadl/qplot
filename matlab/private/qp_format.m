function txt=qp_format(xx)
% txt = QP_FORMAT(xx) performs num2str for a matrix of numbers.
% Each input value is stored in a cell of the output.

idx = qp_idx;
global qp_data;
fmt = qp_data.info(idx).numfmt;

[X Y]=size(xx);
txt=cell(X,Y);

if isempty(fmt)
  for x=1:X
    for y=1:Y
      txt{x,y} = num2str(xx(x,y));
    end
  end
else
  for x=1:X
    for y=1:Y
      txt{x,y} = sprintf(fmt, xx(x,y));
    end
  end
end

