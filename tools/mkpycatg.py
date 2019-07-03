#!/usr/bin/python3

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014-2019  Daniel Wagenaar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
use strict;

my $src = shift;
my $dst = shift;

open IN, "<$src" or die;
open OUT, ">$dst" or die;

header("QPlot: Categorized list of functions");

print OUT <<'EOF';
<body>
<div class="main">
<div class="index">
<span class="toidx"><a href="alpha.html">Alphabetical list</a></span>
</div>
<h1 class="tight">QPlot: Categorized list of functions</h1>
EOF

my $first = 1;
print OUT "<div class=\"list\">\n";
while (<IN>) {
  chomp;
  if (s/://) {
    print OUT "</table>\n" unless $first;
    print OUT "<table class=\"funcs\">\n";
    print OUT "<tr><td class=\"letter\"><span class=\"letterspan\">$_</span></td></tr>";
    $_ = <IN>;
    chomp;
    $first=0;
  }
  print OUT "<tr><td class=\"regular\"><a class=\"mlink\" href=\"$_.html\">$_</a></td></tr>\n";
}
print OUT "</table></div>\n";
trailer();
close OUT;


sub header {
  my $fn = shift;
  print OUT <<'EOF';
  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="../css/doc.css" type="text/css">
    <link rel="stylesheet" href="../css/catg.css" type="text/css">
EOF
  print OUT "    <title>$fn</title>\n";
  print OUT "  </head>\n";
}

sub trailer {
  print OUT <<'EOF';
</div>
<div class="tail">
(C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2014. This web page is licensed under the <a href="http://www.gnu.org/copyleft/fdl.html">GNU Free Documentation License</a>.
</div>
</body>
</html>
EOF
}

sub cfnoq {
  my $a = shift;
  my $b = shift;
  $a =~ s/^q//;
  $b =~ s/^q//;
  return $a cmp $b;
}
'''
