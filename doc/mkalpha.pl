#!/usr/bin/perl -w

use strict;

my @files = ();
my %files = ();
opendir DIR, "../matlab";
for (sort { cfnoq($a,$b) } readdir DIR) {
  s/.m$// or next;
  push @files, $_;
  $files{$_} = 1;
}
closedir DIR;

open OUT, ">html/ref/alpha.html" or die;
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
QPlot Documentation — (C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2014
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