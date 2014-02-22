#!/usr/bin/perl -w

use strict;

my $FONTPACKAGE;
my $FONTSIZE="10pt";
my $FONTSTYLE="\\rm";
my $STARTED=0;
my $X=0;
my $Y=0;
my $W=0;
my $H=0;
my $LASTLINE;
my $PDFNO = 1;
my $TEMPPFX = "/tmp/placeqpt-$$";

while (<>) {
  chomp;
  $LASTLINE = $_;
  my @bits = split(/\s+/, $_);
  next unless @bits;
  my $k = uc(shift @bits);
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
    my $x = shift @bits;
    if (uc($x) eq "SAME") {
      ;
    } elsif (uc($x) eq "RIGHT") {
      $X += $W;
    } else {
      $X = interpretDim($x);
    }
    my $y = shift @bits;
    if (uc($y) eq "SAME") {
      ;
    } elsif (uc($y) eq "BELOW") {
      $Y += $H;
    } else {
      $Y = interpretDim($y);
    }
    while (@bits) {
      my $k1 = uc(shift @bits);
      if ($k1 eq "SHIFTED") {
	$X += interpretDim(shift @bits);
	$Y += interpretDim(shift @bits);
      } else {
	syntax();
      }
    }
  } elsif ($k eq "LABEL") {
    my $txt = shift @bits or syntax();
    my $dx = 0;
    my $dy = 0;
    while (@bits) {
      my $k1 = uc(shift @bits);
      if ($k1 eq "SHIFTED") {
	$dx += interpretDim(shift @bits);
	$dy += interpretDim(shift @bits);
      } else {
	syntax();
      }
    }
    syntax() if @bits;
    writeText($txt, $X+$dx, $Y+$dy);
  } elsif ($k eq "GRAPHICS") {
    my $fn = shift @bits or syntax();
    my $w = 0;
    my $h = 0;
    my $dx = 0;
    my $dy = 0;
    while (@bits) {
      my $k1 = uc(shift @bits);
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
    if ($w>0 && $h>0) {
      $W = $w;
      $H = $h;
    } elsif ($w>0) {
      $W = $w;
      my $wh = getSize($fn);
      $H = $w * $wh->[1]/$wh->[0];
    } elsif ($h>0) {
      $H = $h;
      my $wh = getSize($fn);
      $W = $h * $wh->[0]/$wh->[1];
    } else {
      my $wh = getSize($fn);
      $W = $wh->[0];
      $H = $wh->[1];
    }
  } else {
    syntax();
  }
}

ensureEnded();

exit 0;

######################################################################
sub syntax {
  print STDERR "Syntax error: $LASTLINE\n";
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
  print "\\tikzstyle{every node}=[inner sep=1pt, below right, font=$FONTSTYLE]\n";
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
  my $pdf = "$TEMPPFX-$PDFNO.pdf";
  $PDFNO ++;
  if ($fn =~ /qpt$/) {
    print STDERR "width = $w height = $h\n";
    system("qplot -w$w -h$h $fn $pdf") and die;
    print "\\path (${x}pt,${y}pt) node {\\includegraphics{$pdf}};\n";
  } else {
    system("cp $fn $pdf") and die;
    my @cmt;
    push @cmt, "width=${w}pt" if $w;
    push @cmt, "height=${h}pt" if $h;
    my $cmt = "";
    $cmt = "[" . join(",", @cmt) . "]" if @cmt;
    print "\\path (${x}pt,${y}pt) node {\\includegraphics${cmt}{$pdf}};\n";
  }
}

sub getSize {
  my $fn = shift;
  my @wh = (0, 0);
  if ($fn =~ /qpt$/) {
    open IN, "<$fn" or die;
    while (<IN>) {
      /figsize\s+([0-9.]+)\s+([0-9.]+)/ or next;
      @wh = ($1, $2);
      close IN;
      return \@wh;
    }
  } elsif ($fn =~ /pdf$/) {
    my $id = `identify $fn`;
    $id =~ / (\d+)x(\d+) / or die;
    @wh = ($1, $2);
  }
  return \@wh;
}
