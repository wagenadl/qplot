ALL: directuse.pdf HTML

HTML: html/ref/catg.html html/ref/alpha.html \
	html/ref/qylim.html html/ref/qylim.png

html/ref/alpha.html: mkalpha.pl html/ref/qylim.html
	./mkalpha.pl

html/ref/catg.html: mkcatg.pl html/ref/qylim.html
	./mkcatg.pl

html/ref/qylim.html: m2html.pl html/ref/qylim.png
	./m2html.pl

SERVERNUM=79

html/ref/qylim.png: alleg.m html/ref/qylim_eg.m
	PATH=`pwd`/..:$$PATH xvfb-run octave --eval alleg

html/ref/qylim_eg.m: matlab-eg/qylim_eg.m
	mkdir -p html/ref
	/bin/cp matlab-eg/*_eg.m html/ref

directuse.pdf: directuse.tex directuse-eg.pdf
	pdflatex $<

directuse-eg.pdf: directuse-eg.qpt
	qplot $< $@

clean:;	rm -f *~
	rm -f *.aux *.dvi *.log
	rm -f examples/*~
	rm -f matlab-eg/*~
	rm -f html/css/*~
	rm -f html/tut/*~
