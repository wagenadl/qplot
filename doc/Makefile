ALL: directuse.pdf HTML

HTML: html/ref/catg.html html/ref/alpha.html html/ref/qylim.html

html/ref/qylim.html: alleg.m
	octave --eval alleg

html/ref/alpha.html: mkalpha.pl
	./mkalpha.pl

html/ref/catg.html: mkcatg.pl
	./mkcatg.pl

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
