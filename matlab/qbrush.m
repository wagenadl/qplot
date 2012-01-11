function qbrush(varargin)
% QBRUSH - Set brush for QPLOT
%    QBRUSH id | color | 'none' | opacity  chooses or changes a brush for
%    QPLOT. ID must be a single capital letter. COLOR may be a named color
%    (i.e., one of krgbcmyw), or a 3-digit or a 6-digit string. 
%    OPACITY must be a number between 0 and 1.

fd = qp_fd(1);

for n=1:nargin
  a = varargin{n};
  if ischar(a)
    if length(a)==1 && a>='A' && a<='Z' && n==1
      ; % This is ID, so good
    elseif strmatch(a, strtoks('none'), 'exact')
      ; % This is a known keyword, so good
    elseif ~isempty(qp_mapcolor(a))
      ; % This is a good color
      varargin{n} = qp_mapcolor(a);
    elseif ~isnan(str2double(a)) 
      % This is a number
      if length(a)==3  && all(a>='0') && all(a<='9')
	% This is a three-digit color
	varargin{n} = sprintf('#%02x%02x%02x', ...
	    floor(255.999*atoi(a(1))/9), ...
	    floor(255.999*atoi(a(2))/9), ...
	    floor(255.999*atoi(a(3))/9));
      elseif length(a)==6 && all(a>='0') && all(a<='9')
	% This is a six-digit color
	varargin{n} =  sprintf('#%02x%02x%02x', ...
	    floor(255.999*atoi(a(1:2))/99), ...
	    floor(255.999*atoi(a(3:4))/99), ...
	    floor(255.999*atoi(a(5:6))/99));
      else
	; % This is opacity
      end
    else
      error([ 'Cannot interpret ' a ' as an argument for qbrush' ]);
    end
  elseif isnscalar(a) && isreal(a)
    ; % This is opacity
    varargin{n} = sprintf('%g', a);
  elseif isnvector(a) && isreal(a) && length(a)==3
    % This is a color
    varargin{n} =  sprintf('#%02x%02x%02x', ...
	floor(255.999*a));
  else
    error([ 'Cannot interpret ' disp(a) ' as an argument for qbrush' ]);
  end
end

str = 'brush';
for n=1:nargin
  str = [ str ' ' varargin{n}];
end

fprintf(fd, '%s\n', str);

qp_flush(fd);

