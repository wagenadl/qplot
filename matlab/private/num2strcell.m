function txt=num2strcell(xx,fmt)
% txt = NUM2STRCELL(xx) performs num2str for a matrix of numbers.
% Each input value is stored in a cell of the output.
% txt = NUM2STRCELL(fmt,xx) uses sprintf with given format string.

if nargin>=2
  fmt_=xx;
  xx=fmt;
end

[X Y]=size(xx);
txt=cell(X,Y);

if nargin>=2
  for x=1:X
    for y=1:Y
      txt{x,y} = sprintf(fmt_,xx(x,y));
    end
  end
else
  for x=1:X
    for y=1:Y
      txt{x,y} = num2str(xx(x,y));
    end
  end
end
