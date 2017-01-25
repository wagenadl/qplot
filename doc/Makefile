ALL: qplot-directuse.pdf HTML

HTML: REF TUT CSS HOME

OCTAVE=../tools/octavex

# Reference material
REFEGMS=$(subst ../doc/ref,html/ref,$(wildcard ../doc/ref/*_eg.m))
REFEGPDFS=$(patsubst %_eg.m,%.pdf,$(REFEGMS))
REFEGPNGS=$(patsubst %_eg.m,%.png,$(REFEGMS))
REFEGHTMLS=$(patsubst %_eg.m,%.html,$(REFEGMS))

REF: $(REFEGMS) $(REFEGPDFS) $(REFEGPNGS) $(REFEGHTMLS) \
	html/ref/alpha.html html/ref/catg.html

html/ref/alpha.html: ../tools/mkalpha.pl
	$< ../octave/qplot-0.2 $@

html/ref/catg.html: ../tools/mkcatg.pl ../doc/matlab-org.txt
	$< ../doc/matlab-org.txt $@

$(REFEGPDFS) $(REFEGPNGS): $(REFEGMS) ../tools/alleg.m
	(cd html/ref; ../../$(OCTAVE) ../../../tools/alleg.m ) && touch $@

html/ref/%_eg.m: ../doc/ref/%_eg.m
	mkdir -p html/ref
	cp $^ $@

$(REFEGHTMLS): ../tools/m2html.pl $(REFEGMS) $(REFEGPNGS)
	$<

# Tutorial material
TUTHTMLS=$(subst ../doc/tut,html/tut,$(wildcard ../doc/tut/tut-*.html))
TUTMS=$(subst ../doc/tut,html/tut,$(wildcard ../doc/tut/tut-*.m))
TUTPNGS=$(subst tut,html/tut/tut,tut-01-01.png tut-02-01.png tut-02-02.png tut-02-03.png tut-03-01.png tut-03-02.png tut-03-03.png)

TUT: $(TUTHTMLS) $(TUTMS) $(TUTPNGS)

html/tut/%.html: ../doc/tut/%.html
	mkdir -p html/tut
	cp $^ $@

html/tut/%.m: ../doc/tut/%.m
	mkdir -p html/tut
	cp $^ $@

html/tut/tut-01-01.png: ../doc/tut/tut-01-01.png
	mkdir -p html/tut
	cp $^ $@

html/tut/tut-02-01.png html/tut/tut-02-02.png html/tut-02-03.png: html/tut/tut-01.m
	(cd html/tut; ../../$(OCTAVE) ../../$< )

html/tut/tut-03-01.png html/tut/tut-03-02.png html/tut-03-03.png: html/tut/tut-03.m
	(cd html/tut; ../../$(OCTAVE) ../../$< )

# Style files
CSSS=$(subst ../doc/css,html/css,$(wildcard ../doc/css/*.css))

CSS: $(CSSS)

html/css/%.css: ../doc/css/%.css
	mkdir -p html/css
	cp $^ $@

# HOME folder
HOMEMS=$(subst ../doc/home,html/home,$(wildcard ../doc/home/eg_*.m))
HOMEPDFS=$(patsubst %.m,%.pdf,$(HOMEMS))
HOMEPNGS=$(patsubst %.m,%.png,$(HOMEMS))
HOMEHTML=$(subst ../doc/home,html,$(wildcard ../doc/home/*.html))

HOME: $(HOMEPNGS) $(HOMEPDFS) $(HOMEHTML) $(HOMEMS)

html/home/%.m: ../doc/home/%.m
	mkdir -p html/home
	cp $^ $@

html/%.html: ../doc/home/%.html
	mkdir -p html
	cp $^ $@

html/home/eg_ephys.png: ../doc/home/eg_ephys.png
	mkdir -p html/home
	cp $^ $@

html/home/eg_ephys.pdf: ../doc/home/eg_ephys.pdf
	mkdir -p html/home
	cp $^ $@

html/home/%.png html/home/%.pdf: html/home/%.m
	( cd html/home; ../../$(OCTAVE) ../../$^ )


# Direct use
qplot-directuse.pdf: ../doc/qplot-directuse.tex directuse-eg.pdf
	pdflatex $<

directuse-eg.pdf: ../doc/directuse-eg.qpt
	DISPLAY=`../tools/ensurexvfb` ../build/qplot $< $@

clean:;	rm -f *.aux *.dvi *.log
	rm -f html/tut/*.qpt

