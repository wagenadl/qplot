#!/usr/bin/perl -w

use strict;

my $FONTPACKAGE;
my $FONTSIZE="10pt";
my $FONTSTYLE="\\rm";
my $STARTED=0;
my $X=0;
my $Y=0;
my $LASTLINE;
my $PDFNO = 1;
my $TEMPPFX = "/tmp/placeqpt-$$";

while (<>) {
  chomp;
  $LASTLINE = $_;
  my @bits = split(/\s+/, $_);
  next unless @bits;
  my $k = shift @bits;
  if ($k eq "PREFIX") {
    $TEMPPFX = shift @bits or syntax();
    syntax() if @bits;
  } elsif ($k eq "FONTPACKAGE") {
    $FONTPACKAGE = shift @bits or syntax();
    syntax() if @bits;
  } elsif ($k eq "FONTSIZE") {
    $FONTSIZE = shift @bits or syntax();
    syntax() if @bits;
  } elsif ($k eq "FONTSTYLE") {
    $FONTSTYLE = shift @bits or syntax();
    syntax() if @bits;
  } elsif ($k eq "PANEL") {
    $X = interpretDim(shift @bits);
    $Y = interpretDim(shift @bits);
    syntax() if @bits;
  } elsif ($k eq "LABEL") {
    my $txt = shift @bits or syntax();
    my $dx = 0;
    my $dy = 0;
    while (@bits) {
      my $k1 = shift @bits;
      if ($k1 eq "SHIFTED") {
	$dx += interpretDim(shift @bits);
	$dy += interpretDim(shift @bits);
      } else {
	syntax();
      }
    }
    syntax() if @bits;
    writeText($txt, $X+$dx, $Y+$dy);
  } elsif ($k eq "INCLUDE") {
    my $fn = shift @bits or syntax();
    my $w = 0;
    my $h = 0;
    my $dx = 0;
    my $dy = 0;
    while (@bits) {
      my $k1 = shift @bits;
      if ($k1 eq "SIZE") {
	$w = interpretDim(shift @bits);
	$h = interpretDim(shift @bits);
      } elsif ($k1 eq "SHIFTED") {
	$dx += interpretDim(shift @bits);
	$dy += interpretDim(shift @bits);
      } else {
	syntax();
      }
    }
    syntax() if @bits;
    writeInclude($fn, $X+$dx, $Y+$dy, $w, $h);
  } else {
    syntax();
  }
}

ensureEnded();

exit 0;

######################################################################
sub syntax {
  print "Syntax error: $LASTLINE\n";
  exit 1;
}

sub interpretDim {
  my $arg = shift;
  syntax() unless defined $arg;
  syntax() unless $arg =~ s/(mm|cm|pt|in|)$//;
  my $unit = $1;
  $arg = 1.0 * $arg;
  $arg *= 72 if $unit eq "in";
  $arg *= 72/2.54 if $unit eq "cm";
  $arg *= 72/25.4 if $unit eq "mm";
  return int($arg*10)/10;
}

sub ensureStarted {
  return if $STARTED;
  print "\\documentclass[$FONTSIZE]{standalone}\n";
  print "\\usepackage{$FONTPACKAGE}\n" if defined $FONTPACKAGE;
  print "\\usepackage{tikz}\n";
  print "\\begin{document}\n";
  print "\\begin{tikzpicture}\n";
  print "\\tikzstyle{every node}=[inner sep=0pt, below right, font=$FONTSTYLE]\n";
  $STARTED = 1;
}

sub ensureEnded {
  ensureStarted();
  print "\\end{tikzpicture}\n";
  print "\\end{document}\n";
}

sub writeText {
  my $txt = shift;
  my $x = shift;
  my $y = shift;
  $y = -$y;

  ensureStarted();
  print "\\path (${x}pt,${y}pt) node {$txt};\n";
}

sub writeInclude {
  my $fn = shift;
  my $x = shift;
  my $y = shift;
  my $w = shift;
  my $h = shift;
  $y = -$y;

  ensureStarted();
  if ($fn =~ /qpt$/) {
    my $pdf = "$TEMPPFX-$PDFNO.pdf";
    $PDFNO ++;
    $pdf =~ s/qpt$/pdf/;
    print STDERR "width = $w height = $h\n";
    system("qplot -w$w -h$h $fn $pdf") and die;
    print "\\path (${x}pt,${y}pt) node {\\includegraphics{$pdf}};\n";
  } else {
    print "\\path (${x}pt,${y}pt) node {\\includegraphics[width=$w,height=$h]{$fn}};\n";
  }
}

