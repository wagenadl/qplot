ALL: PYREFS OCTREFS CSS REST

PYREFS: PYEGS
	code/pyrefs

PYEGS:
	mkdir -p build/pyref
	code/pyegs

OCTREFS: OCTEGS
	code/octrefs

OCTEGS:
	mkdir -p build/octref
	code/octegs

CSS:
	/bin/cp -r source/css build/

REST: build/index.html build/installation.html build/gallery/index.html


build/index.html: source/index.html
	code/rehtml $< $@ "QPlot 0.6.0 documentation"


build/installation.html: source/installation.rst
	code/restruct $< $@ "Installation"

build/gallery/index.html: source/gallery.rst
	mkdir -p build/gallery
	code/restruct $< $@ "Gallery"
