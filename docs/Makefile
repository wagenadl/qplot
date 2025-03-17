ALL: PYREFS CSS REST HOMEEGS LUTS JS

PYREFS: PYEGS
	code/pyrefs

PYEGS: PREP
	mkdir -p build/html/pyref
	QT_QPA_PLATFORM=offscreen code/pyegs

OCTREFS: OCTEGS
	code/octrefs

OCTEGS: PREP
	mkdir -p build/html/octref
	QT_QPA_PLATFORM=offscreen code/octegs

CSS: PREP
	/bin/cp -r source/css build/html/

HOMEEGS: PREP
	QT_QPA_PLATFORM=offscreen code/homepageegs

JS: PREP
	/bin/cp -r source/js build/html/


REST: PREP build/html/index.html \
	build/html/installation.html \
	build/html/examples/tutorial1.html \
	build/html/examples/tutorial1.ipynb \
	build/html/examples/eg_ephys.html \
	build/html/examples/eg_ephys.ipynb \
	build/html/examples/eg_circ.html \
	build/html/examples/eg_circ.ipynb \
	build/html/examples/eg_bars.html \
	build/html/examples/eg_bars.ipynb \
	build/html/examples/eg_gline.html \
	build/html/examples/eg_gline.ipynb \
	build/html/examples/eg_imsc.html \
	build/html/examples/eg_imsc.ipynb \
	build/html/octref/index.html

LUTS: PREP build/html/luts/index.html

PREP:
	mkdir -p build/html/pyref
	mkdir -p build/html/gallery
	mkdir -p build/html/home
	mkdir -p build/html/octref
	mkdir -p build/html/luts
	mkdir -p build/html/images
	mkdir -p build/html/examples

build/html/examples/%.ipynb: source/notebooks/%.ipynb
	/bin/cp -r $< $@


build/html/examples/tutorial1.html: build/tutorial1.html code/rehtml_eg
	code/rehtml_eg $< $@

build/html/examples/eg_%.html: build/eg_%.html code/rehtml_eg
	code/rehtml_eg $< $@

build/%.html: source/notebooks/%.ipynb code/ipynb2html
	code/ipynb2html $< $@ build/html/images


build/html/index.html: source/index.html
	code/rehtml $< $@ "QPlot 0.6.0 documentation"

build/html/luts/index.html: code/lutdemo.py
	code/lutdemo.py


build/html/installation.html: source/installation.rst
	code/restruct $< $@ "Installation"

#build/html/gallery/index.html: source/gallery.rst
#	code/restruct $< $@ "Gallery"

build/html/octref/index.html: source/octave.rst
	code/restruct $< $@ "Octave functions"

dist-clean:; rm -rf build

clean:; rm -f build/*.*
