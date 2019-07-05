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

import sys
import os
import re
import pyqplot as qp

ofn = sys.argv[1]
dr, fn = os.path.split(sys.argv[1])
func, xt = os.path.splitext(fn)

def writeheader(f, func):
    f.write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" href="../css/doc.css" type="text/css">
<title>QPlot: %s</title>
</head>
<body class="mloct"><div class="main">
''' % func)

def writetrailer(f):
    f.write('''</div>
<div class="tail">
QPlot Documentation — (C) <a href="http://www.danielwagenaar.net">Daniel Wagenaar</a>, 2019
</div>
</body>
</html>
''')

def indextext(f):
    f.write('''<div class="toindex">
<span class="toidx"><a href="alpha.html">Alphabetical list</a></span>
<span class="toidx"><a href="catg.html">Categories</a></span>
</div>
''')


def extracttitle(func, doc):
    lines = doc.split('\n')
    title = lines[0]
    if title.startswith(func.upper()):
        title = title[len(func):]
        if title.startswith(' - '):
            title = title[3:]
    else:
        print('Unexpected title line for %s: %s', func, title)
        os.exit(1)
    return title

def extractbody(doc):
    lines = doc.split('\n')
    lines.pop(0)
    return '\n'.join(lines)

def pydoc(doc, func, funcs):
    r = re.compile(r'(\W+)')
    wrd = re.compile(r'\w+')
    nl = re.compile(r'\n')
    paren = re.compile(r'\(')
    parenc = re.compile(r'\)')
    bits = r.split(doc)
    out = ['<p>']
    gotfunc = False
    depth = 0
    inargs = False
    for bit in bits:
        if wrd.match(bit):
            if bit==bit.upper() and bit.lower() in funcs:
                if bit.lower()==func:
                    out.append('<b>%s</b>' % bit.lower())
                else:
                    out.append('<a class="tmlink" href="%s.html">%s</a>'
                               % (bit.lower(), bit.lower()))
                gotfunc = True
            else:
                gotfunc = False
                if bit==bit.upper() or inargs:
                    out.append('<i>%s</i>' % bit.lower())
                else:
                    out.append(bit)
        else:
            if bit.startswith('(') and gotfunc:
                inargs = True
            depth += len(paren.findall(bit)) - len(parenc.findall(bit))
            if depth==0:
                inargs = False
                
            sub = nl.split(bit)
            lst = sub.pop(0)
            out.append(lst)
            for sbit in sub:
                if sbit=='':
                    out.append('\n<p>')
                else:
                    if lst.endswith('.') or lst.endswith(':') \
                       or sbit.startswith('     '):
                        out.append('<br>\n')
                    else:
                        out.append(' ')
                    if not sbit.startswith('    '):
                        print('Expected spaces at start of line, not: %s', sbit)
                    sbit = sbit[4:]
                    while sbit.startswith(' '):
                        out.append('&nbsp;')
                        sbit = sbit[1:]
                    out.append(sbit)
    return ''.join(out)

def splitout(line, funcs):
    return line

def titletext(f, func, tagline, funcs):
    f.write('''<div class="titlehead">
<span class="title">%s</span>
<span class="tagline">%s</span>
</div>''' % (func, splitout(tagline, funcs)))

def bodytext(f, body, func, funcs):
    f.write('''<div class="dochead">
Help text:
</div>
<div class="doc">''')
    f.write(pydoc(body, func, funcs))
    f.write('''</div>
''')

def egimage(f, func):
    pass

def egtext(f, func, example):
    pass

doc = qp.__dict__[func].__doc__
funcs = {k for k,v in qp.__dict__.items() if callable(v)}
title = extracttitle(func, doc)
body = extractbody(doc)
example = None
    
with open(ofn, 'w') as f:
    writeheader(f, func)
    indextext(f)
    titletext(f, func, title, funcs)
    bodytext(f, body, func, funcs)
    if os.path.exists('html/pyref/%s.png' % func):
        egimage(f, func)
    if example is not None:
        egtext(f, func, example)
    writetrailer(f)

sys.exit(1)
'''
use strict;

my $here = $0;
$here =~ s{/[^/]+$}{};

system("$here/matlabdoc -f $here/../octave/qplot-0.2 /tmp/qplotml 'QPlot' .") and die;

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
  if (open IN, "html/ref/${f}_eg.m") {
    while (<IN>) {
      s/^\s+$//;
      if (s/^( +)//) {
	$_ = "&nbsp;" x (2*length($1)) . $_;
      }
      push @example, $_;
    }
    close IN;
  }
  while ($#example>0 && $example[$#example] =~ /^$/) {
    pop @example;
  }

  output($f, $title, \@body, \@example);
}

######################################################################

sub output {
  my ($fn, $title, $body, $example) = @_;
  open OUT, ">html/ref/$fn.html" or die;
  header($fn);

  print OUT "<body class=\"mloct\"><div class=\"main\">\n";
  indextext();
  ttltext($fn, $title);
  bodytext($fn, $body);
  egimage($fn) if -f "html/ref/$fn.png";
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
    <link rel="stylesheet" href="../css/doc.css" type="text/css">
EOF
  print OUT "    <title>QPlot: $fn</title>\n";
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

sub ttltext {
  my $fn = shift;
  my $title = shift;
  print OUT "<div class=\"titlehead\">\n";
  print OUT "<span class=\"title\">$fn</span>\n";
  if ($title =~ s/^.*?:\s*//) {
    chomp $title;
    $title =~ s/\.$//;
    print OUT "<span class=\"tagline\">";
    splitout($fn, $title, 0);
    print OUT "</span>\n";
  }
  print OUT "</div>\n";
}  

sub egtext {
  my $fn = shift;
  my $example = shift;
  print OUT "<div class=\"egcontainer\">\n";
  print OUT "<div class=\"eghead\">\n";
  print OUT "Example:\n";
  print OUT "</div>\n";
  print OUT "<div class=\"example\">\n";
    
  for my $line (@$example) {
    if ($line =~ /^\s*$/) {
      print OUT "<p class=\"empty\"></p>\n";
    } else {
      print OUT "<p class=\"eg\">";
      splitout($fn, $line, 0);
      print OUT "</p>\n";
    }
  }
  print OUT "</div>\n";
  print OUT "<div class=\"eglink\">\n";
  print OUT "Download <a href=\"${fn}_eg.m\">source</a>.\n";
  print OUT "</div>\n";
  print OUT "</div>\n";
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
    splitout($fn, $line, 1);
  }

  print OUT "</div>\n";
}

sub splitout {
  my $fn = shift;
  my $line = shift;
  my $useit = shift;
  
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
	if ($useit) {
	  print OUT "<i>$word</i>";
	} else {
	  print OUT "$word";
	}
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
<span class="toidx"><a href="alpha.html">Alphabetical list</a></span>
<span class="toidx"><a href="catg.html">Categories</a></span>
</div>
EOF
}
'''
