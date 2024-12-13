ALL: PYREFS CSS REST HOMEEGS

PYREFS: PYEGS
	code/pyrefs

PYEGS: PREP
	mkdir -p build/html/pyref
	code/pyegs

OCTREFS: OCTEGS
	code/octrefs

OCTEGS: PREP
	mkdir -p build/html/octref
	code/octegs

CSS: PREP
	/bin/cp -r source/css build/html/

HOMEEGS: PREP
	code/homepageegs


REST: PREP build/html/index.html \
	build/html/installation.html \
	build/html/gallery/index.html

PREP:
	mkdir -p build/html/pyref
	mkdir -p build/html/gallery
	mkdir -p build/html/home
	mkdir -p build/html/octref


build/html/index.html: source/index.html
	code/rehtml $< $@ "QPlot 0.6.0 documentation"


build/html/installation.html: source/installation.rst
	code/restruct $< $@ "Installation"

build/html/gallery/index.html: source/gallery.rst
	code/restruct $< $@ "Gallery"

dist-clean:; rm -rf build

clean:; rm -f build/*.*
