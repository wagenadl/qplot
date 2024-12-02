ALL: PYREFS OCTREFS CSS REST

PYREFS: PYEGS
	code/pyrefs

PYEGS:
	code/pyegs

OCTREFS: OCTEGS
	code/octrefs

OCTEGS:
	code/octegs

CSS:
	/bin/cp -r source/css build/

REST: build/index.html build/installation.html


build/index.html: source/index.rst
	code/restruct $< $@ "QPlot 0.6.0 documentation"


build/installation.html: source/installation.rst
	code/restruct $< $@ "Installation"
