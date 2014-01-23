ALL: SRC DOC

SRC: src/Makefile
	$(MAKE) -C src

DOC:; $(MAKE) -C doc

#DIST: clean
#	tar cf ../qplot.tgz -C.. qplot/src qplot/matlab qplot/qpclient qplot/qpclose qplot/qplotml qplot/doc qplot/Makefile

src/Makefile: src/qplot.pro
	cd src;	qmake qplot.pro

#clean:
#	$(MAKE) -C src clean
##	rm src/Makefile

deb:	ALL
	debuild -us -uc -Isrc/debug -Isrc/release -Ifoo -Isrc/Makefile.Release -Isrc/Makefile.Debug -INOTES -Iqplot -Iqplot_debug -I.bzr -I*.mexglx -I.matlabdoc

