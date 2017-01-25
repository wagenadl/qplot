# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014-2017  Daniel Wagenaar
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

ALL: QPLOT DOCS


ifdef DESTDIR
  # Debian uses this
  INSTALLPATH = $(DESTDIR)/usr
  SHAREPATH = $(DESTDIR)/usr/share
else
  INSTALLPATH = /usr/local
  SHAREPATH = /usr/local/share
endif

OCTPKGVSN=0.2
OCTPKG=qplot-$(OCTPKGVSN)
OCTPATH=$(SHAREPATH)/share/octave/packages/$(OCTPKG)

QMAKE=qmake
SELECTQT="-qt=qt5"

DEB_HOST_MULTIARCH ?= $(shell dpkg-architecture -qDEB_HOST_MULTIARCH)

# Build QPLOT (release and debug)
COMMON=src/qplot.pro

QPLOT: build/Makefile
	+make -C build release

QPLOTDBG: build-dbg/Makefile
	+make -C build-dbg debug

build/Makefile: $(COMMON)
	mkdir -p build
	(cd build; $(QMAKE) $(SELECTQT) ../src/qplot.pro )

build-dbg/Makefile: $(GENERATED) $(COMMON) FORCE
	mkdir -p build-dbg
	( cd build-dbg; $(QMAKE) $(SELECTQT) ../src/qplot.pro )

clean:; rm -rf build build-dbg build-doc

# Build DOCS
DOCS: build-doc/Makefile
	+make -C build-doc

build-doc/Makefile: doc/Makefile
	mkdir -p build-doc
	cp doc/Makefile build-doc/

DOCSRC=build-doc/html
DOCPATH=$(SHAREPATH)/doc/qplot

install: ALL
# Install QPLOT:
	install -d $(INSTALLPATH)/bin
	install build/qplot      $(INSTALLPATH)/bin
	install scripts/qpclient $(INSTALLPATH)/bin
	install scripts/qpclose  $(INSTALLPATH)/bin
	install scripts/qplotml  $(INSTALLPATH)/bin
# Install OCTAVE:
	install -d $(SHAREPATH)/octave/packages/$(OCTPKG)/private
	install -m644 $(wildcard octave/$(OCTPKG)/*.m) $(OCTPATH)
	install -m644 $(wildcard octave/$(OCTPKG)/private/*.m) $(OCTPATH)/private
	install -d $(SHAREPATH)/octave/packages/$(OCTPKG)/packinfo
	install -m644 octave/$(OCTPKG)/packinfo/DESCRIPTION $(OCTPATH)/packinfo
# Install DOCS:
	install -d $(DOCPATH)
	install -m644 $(wildcard $(DOCSRC)/*.html) $(DOCPATH)
	install -d $(DOCPATH)/css
	install -m644 $(wildcard $(DOCSRC)/css/*.css) $(DOCPATH)/css
	install -d $(DOCPATH)/ref
	install -m644 $(wildcard $(DOCSRC)/ref/*.html) $(DOCPATH)/ref
	install -m644 $(wildcard $(DOCSRC)/ref/*.m) $(DOCPATH)/ref
	install -m644 $(wildcard $(DOCSRC)/ref/*.png) $(DOCPATH)/ref
	install -m644 $(wildcard $(DOCSRC)/ref/*.pdf) $(DOCPATH)/ref
	install -d $(DOCPATH)/tut
	install -m644 $(wildcard $(DOCSRC)/tut/*.html) $(DOCPATH)/tut
	install -m644 $(wildcard $(DOCSRC)/tut/*.m) $(DOCPATH)/tut
	install -m644 $(wildcard $(DOCSRC)/tut/*.png) $(DOCPATH)/tut
	install -d $(DOCPATH)/home
	install -m644 $(wildcard $(DOCSRC)/home/*.m) $(DOCPATH)/home
	install -m644 $(wildcard $(DOCSRC)/home/*.png) $(DOCPATH)/home
	install -m644 $(wildcard $(DOCSRC)/home/*.pdf) $(DOCPATH)/home
# Install placeqpt
	install -d $(SHAREPATH)/qplot
	install placeqpt/placeqpt.pl $(SHAREPATH)/qplot
	install placeqpt/placeqpt $(INSTALLPATH)/bin
