#!/usr/bin/perl -w

use strict;

system("matlabdoc -f ../../matlab /tmp/qplotml 'QPlot' .") and die;

my @files = ();
my %files = ();
opendir DIR, "/tmp/qplotml";
for (sort readdir DIR) {
  /index.html/ and next;
  s/.html// or next;
  push @files, $_;
  $files{$_} = 1;
}
closedir DIR;

for my $f (@files) {
  print ": $f\n";
  my $title;
  my @body;
  open IN, "/tmp/qplotml/$f.html" or die;
  while (<IN>) {
    /<\/h1>/ and last;
  }
  $title = <IN>;
  while (<IN>) {
    /<hr>/ and last;
    push @body, $_;
  }
  close IN;

  my @example;
  if (open IN, "../matlab-eg/${f}_eg.m") {
    while (<IN>) {
      s/ /&nbsp;/g;
      push @example, $_;
    }
    close IN;
  }

  output($f, $title, \@body, \@example);
}

######################################################################

sub output {
  my ($fn, $title, $body, $example) = @_;
  open OUT, ">html/$fn.html" or die;
  header($fn);

  print OUT "<body class=\"mloct\">\n";
  indextext();
  ttltext($fn, $title);
  bodytext($fn, $body);

  egimage($fn) if -f "html/$fn.png";
  egtext($fn, $example) if @$example;

  trailer();
}

sub header {
  my $fn = shift;
  print OUT <<'EOF';
  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="doc.css" type="text/css">
EOF
  print OUT "    <title>$fn</title>\n";
  print OUT "  </head>\n";
}

sub trailer {
  print OUT "</body>\n";
  print OUT "</html>\n";
}

sub ttltext {
  my $fn = shift;
  my $title = shift;
  print OUT "<div class=\"titlehead\">\n";
  print OUT "<span class=\"title\">$fn</span>\n";
  if ($title =~ s/^.*?:\s*//) {
    chomp $title;
    $title =~ s/\.$//;
    print OUT "<span class=\"tagline\">";
    splitout($fn, $title);
    print OUT "</span>\n";
  }
  print OUT "</div>\n";
}  

sub egtext {
  my $fn = shift;
  my $example = shift;
  print OUT "<div class=\"eghead\">\n";
  print OUT "Example:\n";
  print OUT "</div>\n";
  print OUT "<div class=\"example\">\n";
  for my $line (@$example) {
    if ($line =~ /^\s*$/) {
      print OUT "<p>\n";
    } else {
      splitout($fn, $line);
      print OUT "<br>\n";
    }
  }
  print OUT "</div>\n";
  print OUT "<div class=\"eglink\">\n";
  print OUT "Download <a href=\"${fn}_eg.m\">source</a>.\n";
  print OUT "</div>\n";

  system("cp ../matlab-eg/${fn}_eg.m html/") and die;
}

sub egimage {
  my $fn = shift;
  print OUT "<div class=\"egimage\">\n";
  print OUT "<image class=\"egimg\" src=\"$fn.png\">\n";
  print OUT "<div class=\"eglink\">\n";
  print OUT "Download <a href=\"${fn}.pdf\">pdf</a>.\n";
  print OUT "</div>\n";
  print OUT "</div>\n";
}

sub bodytext {
  my $fn = shift;
  my $body = shift;
  print OUT "<div class=\"dochead\">\n";
  print OUT "Help text:\n";
  print OUT "</div>\n";
  print OUT "<div class=\"doc\">\n";
  for my $line (@$body) {
    splitout($fn, $line);
  }

  print OUT "</div>\n";
}

sub splitout {
  my $fn = shift;
  my $line = shift;
  
  my @bits = split(/(\W+)/, $line);
  while (@bits) {
    my $word = shift @bits;
    my $sep = shift @bits;
    if ($word =~ /^[A-Z]+$/) {
      if (exists $files{lc($word)}) {
	$word = lc $word;
	if ($word eq $fn) {
	  print OUT "<b>$word</b>";
	} else {
	  print OUT "<a class=\"tmlink\" href=\"$word.html\">$word</a>";
	}
      } else {
	print OUT "<i>$word</i>";
      }
    } else {
      if (exists($files{$word}) && !(defined $sep && $sep =~ /^'/)) {
	if ($word eq $fn) {
	  print OUT "<b>$word</b>";
	} else {
	  print OUT "<a class=\"mlink\" href=\"$word.html\">$word</a>";
	}
      } else {
	print OUT $word;
      }
    }
    print OUT $sep if defined $sep;
  }
}

sub indextext {
  print OUT <<'EOF';
<div class="toindex">
<span class="toidx"><a href="alpha.html">Alphabetic list</a></span>
<span class="toidx"><a href="catg.html">Categories</a></span>
</div>
EOF
}  
