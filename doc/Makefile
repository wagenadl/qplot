# -*- Makefile -*-

# DO NOT RUN THIS MAKEFILE IN PLACE. Use toplevel Makefile instead.

ALL: qplot-directuse.pdf

# Direct use
qplot-directuse.pdf: ../doc/qplot-directuse.tex directuse-eg.pdf
	pdflatex $<

directuse-eg.pdf: ../doc/directuse-eg.qpt
	DISPLAY=`../tools/ensurexvfb` ../build/qplot $< $@

clean:
	rm -f *.aux *.dvi *.log
	rm -f html/*/*.qpt
	rm -f html/*/.*.pid
	rm -f directuse-eg.pdf

dist-clean: clean
	rm -f qplot-directuse.pdf

.PHONY: clean dist-clean ALL
