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

ALL: QPLOT # DOCS WEB

ifdef DESTDIR
  # Debian uses this
  INSTALLPATH = $(DESTDIR)/usr
  SHAREPATH = $(DESTDIR)/usr/share
else
  INSTALLPATH = /usr/local
  SHAREPATH = /usr/local/share
endif

OCTPKGVSN=0.3
OCTPKG=qplot-$(OCTPKGVSN)
OCTPATH=$(SHAREPATH)/octave/packages/$(OCTPKG)
PYPATH=$(INSTALLPATH)/lib/python3/dist-packages/pyqplot

QMAKE=qmake
SELECTQT="-qt=qt5"

DEB_HOST_MULTIARCH ?= $(shell dpkg-architecture -qDEB_HOST_MULTIARCH)
export QPLOT_BINARY = $(PWD)/build/qplot
$(echo $(QPLOT_BINARY)

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

clean:; rm -rf build build-dbg build-doc build-web

# Build WEB
WEB: build-web/Makefile DOCS
	make -C build-web

build-web/Makefile: web/Makefile.web
	mkdir -p build-web
	cp web/Makefile.web build-web/Makefile

# Build DOCS
DOCS: build-doc/Makefile QPLOT
	make -C build-doc
	make -C build-doc cleanup

build-doc/Makefile: doc/Makefile.doc
	mkdir -p build-doc
	cp doc/Makefile.doc build-doc/Makefile

DOCSRC=build-doc/html
DOCPATH=$(SHAREPATH)/doc/qplot

install: install-qplot # install-doc

install-qplot: ALL
# Install QPLOT:
	install -d $(INSTALLPATH)/bin
	install build/qplot      $(INSTALLPATH)/bin
	install scripts/qpclient $(INSTALLPATH)/bin
	install scripts/qpclose  $(INSTALLPATH)/bin
	install scripts/qplotml  $(INSTALLPATH)/bin
# Install OCTAVE:
	install -d $(OCTPATH)/private
	install -m644 $(wildcard octave/$(OCTPKG)/*.m) $(OCTPATH)
	install -m644 $(wildcard octave/$(OCTPKG)/private/*.m) $(OCTPATH)/private
	install -d $(OCTPATH)/packinfo
	install -m644 octave/$(OCTPKG)/packinfo/DESCRIPTION $(OCTPATH)/packinfo
# Install PYTHON
	install -d $(PYPATH)
	install -m644 $(wildcard pyqplot/*.py) $(PYPATH)
# Install PLACEQPT:
	install -d $(SHAREPATH)/qplot
	install placeqpt/placeqpt.pl $(SHAREPATH)/qplot
	install placeqpt/placeqpt $(INSTALLPATH)/bin
# Install OTHER THINGS
	install -d $(SHAREPATH)/pixmaps
	install -m644 tools/qplot.svg $(SHAREPATH)/pixmaps
	install -d $(SHAREPATH)/applications
	install tools/qplot.desktop $(SHAREPATH)/applications
# I should create a mimetype entry for .qpt

install-docs: DOCS
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
