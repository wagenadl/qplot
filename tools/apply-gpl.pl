#!/usr/bin/perl -w

use strict;

my $FN = shift @ARGV;

system("grep -q 'This program is free software' $FN") or exit 0;

if ($FN =~ /\.m$/) {
  system("/bin/mv $FN $FN~");
  open IN, "<$FN~" or die;
  open OUT, ">$FN" or die;
  while (<IN>) {
    print OUT $_;
    /^\s*$/ and last;
  }
  print OUT <<"EOF";
% QPlot - Publication quality 2D graphs with dual coordinate systems
% Copyright (C) 2014  Daniel Wagenaar
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

EOF
  while (<IN>) {
    print OUT $_;
  }

  close IN;
  close OUT;
} elsif ($FN =~ /\.H$/ || $FN =~ /\.cpp$/) {
  system("/bin/mv $FN $FN~");
  open IN, "<$FN~" or die;
  open OUT, ">$FN" or die;

  print OUT "// $FN - This file is part of QPlot\n";
  print OUT <<"EOF";

/* QPlot - Publication quality 2D graphs with dual coordinate systems
   Copyright (C) 2014  Daniel Wagenaar
  
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
  
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

EOF

  while (<IN>) {
    print OUT $_;
  }

  close IN;
  close OUT;
}
