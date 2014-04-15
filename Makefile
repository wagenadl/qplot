ALL: SRC DOC

SRC: src/Makefile
	$(MAKE) -C src

DOC:; $(MAKE) -C doc

DIST: clean
	tar czf ../qplot.tgz -C.. --transform s/trunk/qplot/ trunk/src trunk/matlab trunk/qpclient trunk/qpclose trunk/qplotml trunk/doc trunk/Makefile
	tar czf ../qplot-web.tgz --transform s/web/qplot/ -h web

src/Makefile: src/qplot.pro
	cd src;	qmake qplot.pro

clean:
	$(MAKE) -C src clean
##	rm src/Makefile
	rm -f matlab/*~ matlab/private/*~
	$(MAKE) -C doc clean

deb:	ALL
	debuild -us -uc -Isrc/debug -Isrc/release -Ifoo -Isrc/Makefile.Release -Isrc/Makefile.Debug -INOTES -Iqplot -Iqplot_debug -I.bzr -I*.mexglx -I.matlabdoc

