#!/usr/bin/perl -w

use strict;

open IN, "../matlab-org.txt" or die;
open OUT, ">html/catg.html" or die;
header("QPlot: Categorized list of functions");

print OUT <<'EOF';
<body>
<div class="main">
<div class="index">
<span class="toidx"><a href="alpha.html">Alphabetical list</a></span>
</div>
<h1 class="tight">QPlot: Categorized List of Functions</h1>
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
    <link rel="stylesheet" href="doc.css" type="text/css">
    <link rel="stylesheet" href="catg.css" type="text/css">
EOF
  print OUT "    <title>$fn</title>\n";
  print OUT "  </head>\n";
}

sub trailer {
  print OUT <<'EOF';
</div>
<div class="tail">
QPlot Documentation — (C) Daniel Wagenaar, 2012
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
