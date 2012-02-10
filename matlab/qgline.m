function qgline(varargin)
% QGLINE - Generalized line drawing
%   QGLINE(ptspec1, ptspec2, ...).
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
%      RETRACT l1 l2  - Retract preceding and following segments by L1 and 
%                       L2 pt respectively.
%   For instance,
%
%       qgline({'absdata', 0, 1, 'relpaper', 5, 0}, ...
%              {'absdata', 0, 1, 'relpaper', 0, 5})
%
%   draws a line from 5 pt to the right of the point (0,1) in the graph to
%   5 pt above the point (1,0) on the graph.
%
%   Note: The rather cumbersome syntax of QGLINE makes QLINE and QPLOT more
%   attractive for general usage. The same applies to QGAREA versus QAREA 
%   and QPATCH.

fd = qp_fd(1);

args = varargin;
if length(args)==1 && iscell(args)
  args = args{:};
end

cmd = 'gline';
for k=1:length(args)
  cmd = [ cmd ' (' ];
  for q=1:length(args{k})
    x = args{k}{q};
    if ischar(x)
      cmd = [ cmd ' ' x ];
    elseif isnan(x)
      cmd = [ cmd ' -' ];
    else
      cmd = [ cmd ' ' sprintf('%g', x) ];
    end
  end
  cmd = [ cmd ' )' ];
end

fprintf(fd, '%s\n', cmd);

qp_flush(fd);

