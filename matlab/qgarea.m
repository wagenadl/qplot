function qgarea(varargin)
% QGAREA - Generalized line drawing
%   QGAREA(ptspec1, ptspec2, ...).
%   A PTSPEC is a cell array containing a sequence of commands from the 
%   following list:
%      ABSDATA x y    - Absolute data coordinates 
%      RELDATA dx dy  - Relative data coordinates 
%      ABSPAPER x y   - Absolute paper coordinates (in pt)
%      RELPAPER dx dy - Relative data coordinates (in pt)
%      ROTDATA xi eta - Rotate by atan2(eta, xi) in data space.
%                       (This affects subsequent relative positioning.) 
%      ROTPAPER phi   - Rotate by phi radians. (This affects subsequent 
%                       relative positioning.) 
%      RETRACT l      - Retract preceding and following segments by L pt.
%      RETRACT l1 l   - Retract preceding and following segments by L1 and 
%                     - L2 pt respectively.
%
%   Note: The rather cumbersome syntax of QGAREA makes QAREA and QPATCH more
%   attractive for general usage. See also QGLINE.

fd = qp_fd(1);

args = varargin;
if length(args)==1 && iscell(args)
  args = args{:};
end

cmd = 'garea';
for k=1:length(args)
  cmd = [ cmd ' (' ];
  for q=1:length(args{k})
    x = args{k}{q};
    if ischar(x)
      cmd = [ cmd ' ' x ];
    else
      cmd = [ cmd ' ' sprintf('%g', x) ];
    end
  end
  cmd = [ cmd ' )' ];
end

fprintf(fd, '%s\n', cmd);

qp_flush(fd);

