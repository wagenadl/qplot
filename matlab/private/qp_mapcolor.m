function str = qp_mapcolor(str)
switch str
  case 'r'
    str = 'red';
  case 'g'
    str = 'green';
  case 'b'
    str = 'blue';
  case 'm'
    str = 'magenta';
  case 'y'
    str = 'yellow';
  case 'c'
    str = 'cyan';
  case 'k'
    str = 'black';
  case 'w'
    str = 'white';
  otherwise
    str = [];
end

