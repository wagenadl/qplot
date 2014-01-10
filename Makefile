ALL: SRC DOC

SRC: src/Makefile
	make -C src

DOC:; make -C doc

DIST: clean
	tar cf ../qplot.tgz -C.. qplot/src qplot/matlab qplot/qpclient qplot/qpclose qplot/qplotml qplot/doc qplot/Makefile

src/Makefile: src/qplot.pro
	cd src;	qmake qplot.pro

clean:
	make -C src clean
	rm src/Makefile
