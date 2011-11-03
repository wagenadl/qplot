function [y_min,y_max] = sampleminmax(xx,ii)
% SAMPLEMINMAX - Find minima and maxima in bins of sampled data
%    [y_min,y_max] = SAMPLEMINMAX(xx,ii) finds the minima and the maxima
%    of the data XX in the intervals [ii_1,ii_2), [ii_2,ii_3), ...,
%    [ii_n-1,ii_n). Note that xx(ii_n) is never used. 
%    Usage note: This is useful for plotting an electrode trace at just
%    the resolution of the screen, without losing spikes.
