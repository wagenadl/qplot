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

ALL: SRC DOC

SRC: src/Makefile
	$(MAKE) -C src

DOC:; $(MAKE) -C doc

DIST: clean
	tar czf ../qplot.tgz -C.. --transform s/trunk/qplot/ trunk/src trunk/matlab trunk/qpclient trunk/qpclose trunk/qplotml trunk/doc trunk/Makefile

src/Makefile: src/qplot.pro
	cd src;	qmake qplot.pro

clean:
	$(MAKE) -C src clean
##	rm src/Makefile
	rm -f matlab/*~ matlab/private/*~
	$(MAKE) -C doc clean

deb:	ALL
	updatechangelog
	debuild -us -uc -Isrc/debug -Isrc/release -Ifoo -Isrc/Makefile.Release -Isrc/Makefile.Debug -INOTES -Iqplot -Iqplot_debug -I.bzr -I*.mexglx -I.matlabdoc

intra:	deb
	sudo cp -u ../qqplot_*.deb /usr/local/dw/apt/archive/
	sudo /usr/local/dw/apt/update.sh
