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

QPLOT:
	+cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
	+cmake --build build --config=Release

debug:
	+cmake -S . -B build-dbg -DCMAKE_BUILD_TYPE=Debug
	+cmake --build build-dbg --config=Debug

clean:; rm -rf build build-dbg build-doc

DOCS: build-doc/Makefile QPLOT
	+make -C build-doc
	make -C build-doc cleanup

build-doc/Makefile: doc/Makefile.doc
	mkdir -p build-doc
	cp doc/Makefile.doc build-doc/Makefile

.PHONY: ALL QPLOT DOCS clean debug
