# This must be the first this in Makefile.common
TOP := $(dir $(lastword $(MAKEFILE_LIST)))

# Main web file
WEB = proxyfeed
# Main procedure
MAIN = $(WEB)
TESTS = tests
PY = python3
#PY = /home/file13/anaconda3/bin/python
all: tangle basic weave

tangle:
	nuweb -rl $(WEB).w
	chmod +x $(MAIN).py
	chmod +x $(TESTS).py

weave: tangle
	pdflatex '\scrollmode \input $(WEB).tex'
	nuweb -rl $(WEB).w
	pdflatex '\scrollmode \input $(WEB).tex'

release: tangle weave

basic:
	$(PY) $(TESTS).py
#	$(PY) $(MAIN).py

clean: clean-doc

clean-doc:
	rm -f *.log *.aux *.tex *.out *.dvi *.toc

fresh: clean
	rm -rf *.pdf *.py *.xml __pycache__

dist: tangle basic clean
	rm -rf __pycache__
