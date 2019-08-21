#!/usr/bin/perl -w

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
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

use strict;

my $src = shift;
my $dst = shift;

my @files = ();
my %files = ();
opendir DIR, "$src";

for (sort { cfnoq($a,$b) } readdir DIR) {
  s/.m$// or next;
  push @files, $_;
  $files{$_} = 1;
}
closedir DIR;

open OUT, ">$dst" or die;
header("QPlot: Alphabetical list of functions");

print OUT <<'EOF';
<body>
<div class="main">
<div class="index">
<span class="toidx"><a href="catg.html">Categories</a></span>
</div>
<h1 class="tight">QPlot: Alphabetical list of functions</h1>
EOF


my $letter = "";
print OUT "<div class=\"list\">\n";
for my $fn (@files) {
  $fn =~ /^q?(.)/;
  my $let = $1;
  if ($let ne $letter) {
    if ($letter ne "") {
      print OUT "</table>\n";
    }
    print OUT "<table class=\"funcs\">\n";
    print OUT "<tr><td  class=\"letter\"><span class=\"letterspan\">" . uc($let) . "</span></td>";
    print OUT "<td class=\"regular\"><a class=\"mlink\" href=\"$fn.html\">$fn</a></td></tr>\n";
    $letter = $let;
  } else {
    print OUT "<tr><td></td><td><a class=\"mlink\" href=\"$fn.html\">$fn</a></td></tr>\n";
  }
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
    <link rel="stylesheet" href="../css/alpha.css" type="text/css">
EOF
  print OUT "    <title>$fn</title>\n";
  print OUT "  </head>\n";
}

sub trailer {
  print OUT <<'EOF';
</div>
<div class="tail">
(C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2014–2019.  This web page is licensed under the <a href="http://www.gnu.org/copyleft/fdl.html">GNU Free Documentation License</a>.
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
