ALL: directuse.pdf HTML

HTML: html/ref/catg.html html/ref/alpha.html \
	html/ref/qylim.html html/ref/qylim_eg.png

html/ref/alpha.html: mkalpha.pl
	./mkalpha.pl

html/ref/catg.html: mkcatg.pl
	./mkcatg.pl

html/ref/qylim.html: m2html.pl
	./m2html.pl

html/ref/qylim_eg.png: alleg.m
	PATH=`pwd/..:$PATH` octave --eval alleg

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
